"""Check the four 3x3 grids and caption clearance in a composed factory."""
import argparse
import json
from pathlib import Path


def check(scene, catalog):
    manifest = json.loads((Path(scene).parent / 'manifest.json').read_text())
    cases = {c['id']: c for c in json.loads(Path(catalog).read_text())['cases']}
    labels = {l['id']: l for l in manifest['factory_labels']['labels']}
    rows = []
    for family in ('transport', 'mosaic', 'relay', 'dial'):
        places = [p for p in manifest['placements'] if p['family'] == family]
        if len(places) != 9:
            raise ValueError(f'{family}: expected nine workstations')
        ordered = sorted(places, key=lambda p: -(p['planning_bounds_xy_m'][1] + p['planning_bounds_xy_m'][3]))
        for level in (1, 2, 3):
            row = sorted(ordered[(level-1)*3:level*3], key=lambda p: p['planning_bounds_xy_m'][0])
            sizes = [cases[p['case_id']].get('dials', cases[p['case_id']]['arms']) for p in row]
            if [cases[p['case_id']]['level'] for p in row] != [level]*3 or sizes != sorted(sizes) or len(set(sizes)) != 3:
                raise ValueError(f'{family}: wrong ordering at level {level}')
            rows.append(dict(family=family, level=level, cases=[p['case_id'] for p in row]))
        for p in places:
            label = labels['ws_caption_'+p['case_id']]
            gap = label['bounds_xy_m'][1] - p['table_bounds_xy_m'][3]
            if not .1 <= gap <= 1.01:
                raise ValueError(f'{p["case_id"]}: caption not above tabletop or too far away ({gap})')
    return dict(passed=True, grids=rows, stations=36, scope='Top camera grid and table-edge clearance; initial state only')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scene', type=Path, required=True)
    p.add_argument('--catalog', type=Path, default=Path('configs/suites/frontier-current-oracle.json'))
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = check(a.scene, a.catalog)
    a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
