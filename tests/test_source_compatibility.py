from pathlib import Path
import shutil
import tempfile
import unittest
import ast

from robofrontier.task_families import ROOT, read, sha
from robofrontier.source_compatibility import RECEIPT, historical_digest, normalized_digest


class HistoricalCompatibilityTests(unittest.TestCase):
    def test_observation_normalization_cannot_hide_world_physics_changes(self):
        item=next(row for row in read(ROOT/RECEIPT)['files'] if row['path']=='robofrontier/pipeline.py')
        tree=ast.parse((ROOT/item['path']).read_text())
        world=next(node for node in tree.body if isinstance(node,ast.ClassDef) and node.name=='World')
        step=next(node for node in world.body if isinstance(node,ast.FunctionDef) and node.name=='step')
        step.body.insert(0,ast.parse('self.data.qvel[:] = 100').body[0])
        self.assertNotEqual(normalized_digest(ast.unparse(tree),item['rule']),item['unaffected_ast_sha256'])

    def test_receipt_pins_current_bytes_and_unaffected_ast(self):
        for item in read(ROOT/RECEIPT)['files']:
            self.assertEqual(sha(ROOT/item['path']), item['integrated_sha256'])
            self.assertEqual(normalized_digest((ROOT/item['path']).read_bytes(), item['rule']), item['unaffected_ast_sha256'])
            for family in item['families']:
                self.assertEqual(historical_digest(ROOT, item['path'], family), item['historical_sha256'])
            self.assertEqual(historical_digest(ROOT, item['path'], 'relay'), item['integrated_sha256'])

    def test_unreviewed_shared_edits_are_rejected_even_if_only_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in (RECEIPT, 'robofrontier/pipeline.py'):
                target = root/relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/relative, target)
            with (root/'robofrontier/pipeline.py').open('a') as out:
                out.write('\n# unreviewed\n')
            with self.assertRaisesRegex(ValueError, 'Unreviewed'):
                historical_digest(root, 'robofrontier/pipeline.py', 'dial')


if __name__ == '__main__':
    unittest.main()
