"""Produce a new audited presentation release without altering historical edits."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path, PurePosixPath

from robofrontier.task_families import ROOT,RELEASE,read,sha
from robofrontier.station_edit import build
from robofrontier.run_setup import write_json

MOSAIC_VIDEO_INDEX = 'outputs/oracle/mosaic-continuation-20261026/videos/video-index.json'


def historical_edit(row, root=ROOT):
    """Resolve a pinned edit directly or through its unchanged historical index."""
    root = Path(root)
    reference = row.get('historical_edit', row['edit'])
    expected = row.get('historical_edit_sha256', row['edit_sha256'])
    if isinstance(reference, dict):
        if (set(reference) != {'kind', 'path', 'sha256'}
                or reference['kind'] != 'mosaic_video_index'
                or reference['path'] != MOSAIC_VIDEO_INDEX):
            raise ValueError('Unknown historical edit index reference')
        index = root/reference['path']
        if not index.resolve().is_relative_to(root.resolve()) or sha(index) != reference['sha256']:
            raise ValueError('Historical video index differs or escapes the checkout')
        prefix = PurePosixPath(MOSAIC_VIDEO_INDEX).parent
        candidates = set()
        for entry in read(index)['videos']:
            if entry['case_id'] != row['id']:
                continue
            value = PurePosixPath(entry['motion_edit_timeline'])
            if '..' in value.parts or '\\' in str(value):
                raise ValueError('Invalid historical timeline path')
            if value.is_absolute():
                for anchor in (PurePosixPath(str(root.absolute())), PurePosixPath(str(root.resolve())),
                               PurePosixPath('/Users/fanchangxuan/Repos/roomscript2')):
                    if value.is_relative_to(anchor):
                        value = value.relative_to(anchor)
                        break
                else:
                    raise ValueError('Unknown historical timeline root')
            path = root.joinpath(*value.parts)
            if (not value.is_relative_to(prefix) or value.name != row['id']+'.json'
                    or not path.resolve().is_relative_to((root/str(prefix)).resolve())
                    or not path.resolve().is_relative_to(root.resolve())):
                raise ValueError('Historical timeline escapes its registered video directory')
            if entry['motion_edit_timeline_sha256'] != expected:
                raise ValueError('Historical timeline checksum disagrees with the release')
            candidates.add(path)
        if len(candidates) != 1:
            raise ValueError('Historical case must identify one timeline')
        path = candidates.pop()
    elif isinstance(reference, str):
        path = root/reference
    else:
        raise ValueError('Invalid historical edit reference')
    if sha(path) != expected:
        raise ValueError('Historical edit bytes differ from the release')
    return path, expected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,choices=range(1,5),default=2)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    release=deepcopy(read(ROOT/RELEASE))
    work=[(name,f,row) for name,f in release['families'].items() for row in f['oracle']]
    def one(entry):
        name,family,row=entry;destination=args.output/row['id']
        row.setdefault('historical_edit',row['edit']);row.setdefault('historical_edit_sha256',row['edit_sha256'])
        edit, checksum = historical_edit(row)
        original=dict(row,edit=str(edit),edit_sha256=checksum)
        result=build(original,destination)
        row['edit']=str((destination/'edit.json').resolve());row['edit_sha256']=sha(row['edit'])
        row.pop('derived_track',None)
        print(row['id'],'additional removed states',result['additional_removed_frames'],flush=True)
        return dict(case_id=row['id'],**{k:result[k]for k in ('retained_frames','removed_frames','additional_removed_frames','restored_event_context_frames')})
    with ThreadPoolExecutor(max_workers=args.workers)as pool:results=list(pool.map(one,work))
    write_json(args.output/'release.json',release)
    write_json(args.output/'summary.json',dict(cases=results,physics_steps=0,original_edits_overwritten=False))


if __name__=='__main__':main()
