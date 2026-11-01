"""Explicit compatibility of historical Oracle checks with shared integration.

The returned hash identifies the historical source, never the current file.
Current bytes and the unaffected AST must both match the reviewed receipt.
This does not certify Relay's changed scoring or produce new physical evidence.
"""
import ast
import hashlib
import json
from pathlib import Path

RECEIPT = 'configs/task_families/source-compatibility.json'


def normalized_digest(source, rule):
    tree = ast.parse(source)
    if rule == 'exclude_relay_class':
        found = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Relay']
        if len(found) != 1:
            raise ValueError('Expected one Relay class')
        tree.body.remove(found[0])
    elif rule in ('exclude_prepared_policy_guard', 'exclude_policy_service', 'exclude_policy_service_and_observation_metadata'):
        world = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'World')
        method = next(n for n in world.body if isinstance(n, ast.FunctionDef) and n.name == 'start_trial')
        expected = ast.parse("if self.task.get('execution_readiness')=='prepared_policy_trial':\n from .task_families import validate_frozen_policy\n validate_frozen_policy(self.task,self.directory)").body[0]
        method.body = [n for n in method.body if ast.dump(n) != ast.dump(expected)]
        if rule in ('exclude_policy_service', 'exclude_policy_service_and_observation_metadata'):
            # CLI hosting changes only the GUI/service wrapper. World stepping,
            # robot control, task sampling and recording remain in the digest.
            service=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Service')
            tree.body.remove(service)
        if rule == 'exclude_policy_service_and_observation_metadata':
            # Admit only these reviewed non-physical changes. Every remaining
            # AST node must still match the original receipt, including world
            # stepping, controls, task sampling and motion recording.
            imports = [ast.parse(text).body[0] for text in (
                'import os', 'from .observation_image import observation_profile',
                'from .tool_errors import CallIdConflict, conflict_error')]
            for expected_import in imports:
                matches = [node for node in tree.body if ast.dump(node) == ast.dump(expected_import)]
                if len(matches) != 1:
                    raise ValueError('Observation compatibility import differs from reviewed source')
                tree.body.remove(matches[0])
            init = next(node for node in world.body if isinstance(node, ast.FunctionDef) and node.name == '__init__')
            observed = ast.parse("frozen_cfg=json.loads(hand_cfg.read_text()) if hand_cfg.exists() else {}\n"
                                 "self.observation_image=observation_profile(frozen_cfg)\n"
                                 "profile=frozen_cfg.get('gripper_position_servo','legacy')").body
            indices = [i for i in range(len(init.body)-2)
                       if [ast.dump(n) for n in init.body[i:i+3]] == [ast.dump(n) for n in observed]]
            if len(indices) != 1:
                raise ValueError('Observation initialization differs from reviewed source')
            original = ast.parse("profile=json.loads(hand_cfg.read_text()).get('gripper_position_servo','legacy') if hand_cfg.exists() else 'legacy'").body
            init.body[indices[0]:indices[0]+3] = original
            facts = next(node for node in world.body if isinstance(node, ast.FunctionDef) and node.name == 'robot_facts')
            expected_size = ast.parse("[self.observation_image['width'],self.observation_image['height']]", mode='eval').body
            sizes = [node for node in ast.walk(facts) if isinstance(node, ast.List) and ast.dump(node) == ast.dump(expected_size)]
            if len(sizes) != 1:
                raise ValueError('Observation camera metadata differs from reviewed source')
            sizes[0].elts = [ast.Constant(1280), ast.Constant(800)]
    elif rule == 'exclude_policy_harness_selection':
        method=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='load_harness')
        reviewed=ast.parse("if c['manager'] != 'Meta' or c['coordinator'] not in ('Controller', 'Coordinator'):\n"
                           " raise ValueError('Use Meta and Controller; legacy Coordinator is accepted for frozen runs')\n"
                           "if c.get('engine','codex') not in ('codex','claude'):\n"
                           " raise ValueError('Unknown policy engine')\n"
                           "if c.get('startup_protocol', 'ready_barrier_v1') not in ('ready_barrier_v1', 'direct_controller_v2', 'direct_team_v3'):\n"
                           " raise ValueError('Unknown startup protocol')\n"
                           "if c.get('startup_protocol') == 'direct_controller_v2' and c['topology'] not in ('adaptive', 'centralized'):\n"
                           " raise ValueError('Direct startup requires a single Controller')\n"
                           "if c.get('startup_protocol') == 'direct_team_v3' and c['topology'] not in ('hierarchical', 'peer'):\n"
                           " raise ValueError('Direct team startup requires standing Workers')").body
        original=ast.parse("if c['manager'] != 'Meta' or c['coordinator'] != 'Coordinator':\n"
                           " raise ValueError('Use explicit Meta / Coordinator role boundary')").body[0]
        for index,expected in enumerate(reviewed):
            matches=[i for i,node in enumerate(method.body) if ast.dump(node)==ast.dump(expected)]
            if len(matches)!=1:
                raise ValueError('Harness selection differs from reviewed configuration checks')
            if index==0:method.body[matches[0]]=original
            else:method.body.pop(matches[0])
    elif rule == 'mosaic_public_projection':
        # This authenticates only the old review artifact's public projection.
        # Validator improvements and current scoring are explicitly not equated.
        names={'_public_boundary','project_public','_check_target','_target_image'}
        functions=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names]
        guards=[node for node in tree.body if isinstance(node,ast.Assign) and
                any(isinstance(target,ast.Name) and target.id=='FORBIDDEN_PUBLIC_KEYS' for target in node.targets)]
        if len(functions)!=4 or len(guards)!=1:
            raise ValueError('Mosaic public projection structure differs')
        tree.body=[node for node in tree.body if node in functions or node in guards]
    elif rule == 'mosaic_preview_display_text':
        # The receipt also pins the complete reviewed current bytes. Only this
        # display generator admits its caption translation; no controller does.
        class DisplayText(ast.NodeTransformer):
            def visit_Constant(self,node):
                if isinstance(node.value,str):node.value='TEXT'
                return node
        tree=DisplayText().visit(tree)
    else:
        raise ValueError('Unknown compatibility rule')
    return hashlib.sha256(ast.dump(tree).encode()).hexdigest()


def historical_digest(root, relative, family):
    root = Path(root)
    data = (root/relative).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    receipt = json.loads((root/RECEIPT).read_text())
    for item in receipt['files']:
        if item['path'] != relative or family not in item['families']:
            continue
        if actual == item['historical_sha256']:
            return actual
        if actual != item['integrated_sha256'] or normalized_digest(data, item['rule']) != item['unaffected_ast_sha256']:
            raise ValueError('Unreviewed shared source change: '+relative)
        return item['historical_sha256']
    return actual
