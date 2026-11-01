import json
from pathlib import Path
import tempfile
import unittest

from scripts.check_factory_layout import check


class FactoryLayoutChecks(unittest.TestCase):
    def test_four_grids_and_caption_direction_are_checked(self):
        places, cases, labels = [], [], []
        for family in ('transport', 'mosaic', 'relay', 'dial'):
            for level in (1, 2, 3):
                for size in (4, 6, 8):
                    case_id = f'{family}-{size}-d{level}'
                    x, y = size*2, (4-level)*10
                    places.append(dict(case_id=case_id, family=family,
                        planning_bounds_xy_m=[x-1,y-1,x+1,y+1],
                        table_bounds_xy_m=[x-1,y-1,x+1,y+1]))
                    cases.append(dict(id=case_id, family=family, level=level, arms=size))
                    labels.append(dict(id='ws_caption_'+case_id,
                        bounds_xy_m=[x-1,y-1.46,x+1,y-1.2]))
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            manifest = root/'manifest.json'; catalog = root/'catalog.json'
            def write():
                manifest.write_text(json.dumps(dict(placements=places, factory_labels=dict(labels=labels))))
                catalog.write_text(json.dumps(dict(cases=cases)))
            write()
            self.assertTrue(check(root/'scene.xml', catalog)['passed'])
            labels[0]['bounds_xy_m'][0] += .35
            labels[0]['bounds_xy_m'][2] += .35
            write()
            with self.assertRaisesRegex(ValueError, 'not centered'):
                check(root/'scene.xml', catalog)
            labels[0]['bounds_xy_m'][0] -= .35
            labels[0]['bounds_xy_m'][2] -= .35
            labels[0]['bounds_xy_m'][3] = places[0]['table_bounds_xy_m'][3] + .5
            write()
            with self.assertRaisesRegex(ValueError, 'caption'):
                check(root/'scene.xml', catalog)
            labels[0]['bounds_xy_m'][3] = places[0]['table_bounds_xy_m'][1] - .2
            cases[0]['level'] = 3
            write()
            with self.assertRaisesRegex(ValueError, 'ordering'):
                check(root/'scene.xml', catalog)
