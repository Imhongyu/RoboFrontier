"""Verify that a Claude Code fork inherited its parent's history, from native transcripts.

`claude --resume PARENT --fork-session` writes the child's transcript under the same
config directory. Observed with CLI 2.1.312 and 2.1.316: the child carries every parent
message row with the same uuid and content, differing only in `sessionId` and
`promptId`, and the CLI writes it as the child's first turn starts, before the model
replies. Anything else that differs, or a parent that changed after the fork, is
rejected rather than tolerated. The model's own claims are never used as evidence.
"""
import hashlib
import json
import re
from pathlib import Path

UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
# Per-session fields that legitimately differ between a parent row and its forked copy.
SESSION_FIELDS = ('sessionId', 'promptId')


def transcript_rows(config_dir, session_id):
    """Return the parsed rows of exactly one transcript for this native session ID."""
    if not UUID.fullmatch(session_id):
        raise ValueError('Expected a native session UUID')
    matches = sorted(Path(config_dir).glob('projects/*/' + session_id + '.jsonl'))
    if len(matches) != 1:
        raise ValueError('Native transcript missing or ambiguous for session ' + session_id)
    rows = []
    for number, line in enumerate(matches[0].read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as error:
            raise ValueError('Native transcript line %d is not JSON' % number) from error
        if not isinstance(row, dict):
            raise ValueError('Native transcript line %d is not an object' % number)
        rows.append(row)
    return rows


def history(rows, session_id):
    """Message rows in file order with per-session fields removed; fail on foreign rows."""
    out = []
    for row in rows:
        if not isinstance(row.get('uuid'), str):
            continue  # bookkeeping rows are not conversation history
        if row.get('sessionId') != session_id:
            raise ValueError('Transcript row belongs to a different session')
        out.append({k: v for k, v in row.items() if k not in SESSION_FIELDS})
    if len({row['uuid'] for row in out}) != len(out):
        raise ValueError('Duplicate message UUID inside one transcript')
    return out


class ForkDiverged(ValueError):
    """The histories differ in a way no further transcript write can repair."""


def fork_provenance(parent, child, config_dir, at=None):
    """Compare the native history prefix; this alone does not prove fork creation.

    Without `at`, the child must copy the parent's whole current history. `at` pins the
    parent's history at the fork point (for a delegate, its pending delegate call): the
    parent must still begin with it, though it may have moved on since, and the child
    must copy exactly it, with no later parent row.
    """
    if parent == child:
        raise ValueError('A fork cannot be its own source')
    current = history(transcript_rows(config_dir, parent), parent)
    copy = history(transcript_rows(config_dir, child), child)
    source = current if at is None else at
    if not source:
        raise ValueError('Source session has no recorded history')
    if current[:len(source)] != source:
        raise ForkDiverged('Source session no longer begins with the fork point')
    if copy[:len(source)] != source:
        raise ValueError('Native fork history does not match the source session')
    if at is not None and {row['uuid'] for row in copy[len(source):]} & {row['uuid'] for row in current}:
        raise ForkDiverged('Native fork copied source history beyond the fork point')
    digest = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()
    return {'source_thread_id': parent, 'source_ordinal': len(source),
            'source_sha256': digest, 'source_last_uuid': source[-1]['uuid'], 'engine': 'claude'}


def first_input(rows):
    """Text of the first user message in these history rows that is not a tool result.

    A fork taken at a pending tool call starts with rows the CLI adds itself (an error
    result for the unanswered call and a short assistant reply); the host's first
    message to the child follows them.
    """
    for row in rows:
        message = row.get('message')
        if row.get('type') != 'user' or row.get('isMeta') or not isinstance(message, dict):
            continue
        content = message.get('content')
        if isinstance(content, str):
            return content
        if isinstance(content, list) and content and all(
                isinstance(item, dict) and item.get('type') == 'text' for item in content):
            return ''.join(item.get('text', '') for item in content)
    return None
