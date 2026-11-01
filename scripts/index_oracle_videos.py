"""Index and validate existing reference videos, without running simulation."""
import concurrent.futures
import html
import json
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/generated/frontier-suite/oracle-videos-20261024'


def candidate(path):
    text = str(path.relative_to(ROOT)).lower()
    return ('oracle' in text or 'reference' in text or
            '/program-transport-' in text or '/beam-handoff-grasp-' in text)


def inspect(path):
    relative = str(path.relative_to(ROOT))
    record = dict(path=relative, bytes=path.stat().st_size)
    probe = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height',
                            '-of','json',str(path)], capture_output=True, text=True)
    if probe.returncode:
        return dict(record, playable=False, error=probe.stderr.strip()[:500])
    metadata = json.loads(probe.stdout)
    streams = [s for s in metadata.get('streams',[]) if s.get('codec_type')=='video']
    if not streams:
        return dict(record, playable=False, error='No video stream')
    decode = subprocess.run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-f','null','-'], capture_output=True,text=True)
    record.update(playable=decode.returncode==0 and not decode.stderr.strip(),
                  duration_s=float(metadata.get('format',{}).get('duration',0)),
                  width=streams[0].get('width'),height=streams[0].get('height'))
    if decode.stderr.strip():record['error']=decode.stderr.strip()[:500]
    for parent in path.parents:
        if parent == ROOT:break
        report = parent/'report.json'
        if report.exists():
            try:
                data=json.loads(report.read_text())
                record.update(report=str(report.relative_to(ROOT)),
                              reported_passed=data.get('passed'),scope=data.get('scope'),
                              task_success=data.get('task_success'))
                break
            except (ValueError,OSError):pass
    if 'frontier-v1' in relative:record['group']='Selected 36-scene series'
    elif 'transport' in relative or 'autonomous-loop' in relative:record['group']='Historical Transport / serial and parallel references'
    elif 'beam-handoff' in relative:record['group']='Historical Relay'
    elif 'floating-crank' in relative:record['group']='Historical floating crank'
    elif 'floating' in relative:record['group']='Historical floating gear / support comparisons'
    else:record['group']='Historical tabletop dial / crank'
    return record


def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'files').mkdir(exist_ok=True)
    paths=sorted(p for p in (ROOT/'runs').rglob('*') if p.suffix.lower() in ('.mp4','.mov','.mkv','.webm') and candidate(p))
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for i, record in enumerate(pool.map(inspect,paths),1):
            records.append(record)
            print(i,len(paths),record['path'],record['playable'],flush=True)
    for i,r in enumerate(records,1):
        if r['playable']:
            link=OUT/'files'/f'{i:03d}.mp4'
            if not link.exists():link.symlink_to(ROOT/r['path'])
            r['url']=f'files/{i:03d}.mp4'
    (OUT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    playable=[r for r in records if r['playable']]
    with zipfile.ZipFile(OUT/'oracle-videos-all.zip','w',compression=zipfile.ZIP_STORED,allowZip64=True) as archive:
        for r in playable:archive.write(ROOT/r['path'],r['path'])
        archive.write(OUT/'manifest.json','manifest.json')
    groups=[]
    for group in dict.fromkeys(r['group'] for r in playable):
        cards=[]
        for r in [v for v in playable if v['group']==group]:
            state='Reported failure / diagnostic comparison' if r.get('reported_passed') is False else 'Reported pass; see the report scope' if r.get('reported_passed') is True else 'No explicit passing verdict'
            cards.append(f'<article data-search="{html.escape(r["path"])}"><h3>{html.escape(r["path"])}</h3><p>{state} · {r["duration_s"]:.1f} s · {r["width"]}×{r["height"]}</p><video controls preload="none" src="{r["url"]}"></video><p><a href="{r["url"]}" target="_blank">Open video</a> · <a href="{r["url"]}" download="{Path(r["path"]).name}">Download video</a></p></article>')
        groups.append(f'<section><h2>{group} · {len(cards)} items</h2><div class="grid">'+''.join(cards)+'</div></section>')
    bad=''.join('<li>'+html.escape(r['path'])+'</li>' for r in records if not r['playable'])
    page=f'''<!doctype html><meta charset="utf-8"><title>Oracle video gallery</title><style>body{{font:16px system-ui;color:#182631;background:#f1f5f7;max-width:1500px;margin:32px auto;padding:0 24px}}h1{{font-size:36px}}p{{line-height:1.7}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,1fr));gap:20px}}article{{background:white;padding:18px;border-radius:12px}}h3{{font-size:15px;overflow-wrap:anywhere}}video{{width:100%;background:#e4eaf0}}a{{color:#175d94}}input{{width:90%;font-size:18px;padding:12px}}section{{margin-top:40px}}</style><h1>Oracle / fixed references · Existing video gallery</h1><p>Total {len(playable)} fully decodable videos. The selected 36-scene series is separate from historical diagnostics. All come from existing files, without new experiments. Historical revisions, failed attempts and physics comparisons remain; playable video is not proof of full-task success.</p><p><a href="oracle-videos-all.zip">Download all videos ZIP</a> · <a href="manifest.json">Complete provenance and checks</a></p><input id="q" placeholder="Search task, arm count, attempt or video filename">{''.join(groups)}<details><summary>Unplayable files ({len(records)-len(playable)} files, excluded from the download)</summary><ul>{bad}</ul></details><script>document.querySelector('#q').addEventListener('input',e=>{{const q=e.target.value.toLowerCase();document.querySelectorAll('article').forEach(c=>c.hidden=!c.dataset.search.toLowerCase().includes(q));}});</script>'''
    (OUT/'index.html').write_text(page)
    (OUT/'README.md').write_text('# Oracle video gallery\n\nExisting Oracle / fixed-reference videos, including historical revisions, failed attempts and physics comparisons.\n\n'+''.join(f'- [{r["path"]}]({(ROOT/r["path"]).as_posix()})\n' for r in playable))
    print(json.dumps(dict(total=len(records),playable=len(playable),groups=Counter(r['group'] for r in playable),zip_bytes=(OUT/'oracle-videos-all.zip').stat().st_size),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
