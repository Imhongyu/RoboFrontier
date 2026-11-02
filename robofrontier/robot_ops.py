"""The runtime operations a policy role may call through its robot tool.

One list for every transport: the Claude robot MCP, the Codex CLI robot tool (the
runtime itself rejects anything else) and the Codex Desktop robot MCP. Meta's
administrative methods are never reachable through a policy connection.
"""
POLICY_OPS = frozenset(('public_image', 'ready', 'robot_model', 'check_motion', 'send', 'inbox', 'wait_events',
                        'history', 'work', 'delegate', 'return_task', 'team', 'checkpoint', 'yield',
                        'observe', 'stop', 'move', 'gripper', 'action_batch', 'recover_action', 'job', 'finish',
                        'pending'))
