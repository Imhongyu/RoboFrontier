"""Former locations of policy texts that released registries still name.

Registries and review packages record the path a text had when they were built,
and their hashes cover those records, so the records stay unchanged. Each text
now lives, byte for byte, under prompts/archive/; `source` maps a recorded path
to where its bytes are read today.
"""
from pathlib import PurePosixPath

MOVED = (
    ('prompts/tasks/', 'prompts/archive/tasks/'),
    ('prompts/common.md', 'prompts/archive/common.md'),
    ('prompts/policy-rules.md', 'prompts/archive/policy-rules.md'),
    ('prompts/claude/controller.md', 'prompts/archive/claude/controller.md'),
    ('prompts/claude/standing-controller.md', 'prompts/archive/claude/standing-controller.md'),
    ('prompts/claude/standing-worker.md', 'prompts/archive/claude/standing-worker.md'),
    ('.agents/skills/mosaic-r13/', 'prompts/archive/skills/mosaic-r13/'),
)


def source(relative):
    """The repository-relative path that now holds the text recorded as `relative`."""
    value = str(PurePosixPath(relative))
    for old, new in MOVED:
        if value == old or old.endswith('/') and value.startswith(old):
            return new + value[len(old):]
    return value
