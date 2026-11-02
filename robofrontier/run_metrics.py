"""Derived host metrics with explicit missing values; never evaluator feedback."""
import json
import math
import os
from pathlib import Path
import time

from . import run_layout


def host_event(run, event, **fields):
    # Telemetry is derived evidence. Its failure must not hide a robot result
    # or turn a settled action into an apparently unsubmitted request.
    try:
        path = run_layout.path(run, 'host_log', 'claude')
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps({'schema': 'robofrontier.host-event.v1', 'at': time.time(),
                           'event': event, **fields}, ensure_ascii=False, allow_nan=False)+'\n').encode()
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try: return os.write(fd, raw) == len(raw)
        finally: os.close(fd)
    except (OSError, ValueError, TypeError):
        return False


def number(value):
    return value if type(value) in (int, float) and math.isfinite(value) and value >= 0 else None


def usage(engine, raw, model_usage=None):
    raw = raw if isinstance(raw, dict) else {}
    if engine == 'claude':
        # CLI modelUsage is cumulative over all requests in this CLI turn;
        # usage may describe only its final request. Never add the two together.
        if isinstance(model_usage, dict) and model_usage:
            aliases = {'input_tokens':'inputTokens', 'cache_read_input_tokens':'cacheReadInputTokens',
                       'cache_creation_input_tokens':'cacheCreationInputTokens', 'output_tokens':'outputTokens'}
            entries = list(model_usage.values())
            raw = {key: sum(item[name] for item in entries)
                   if all(isinstance(item, dict) and number(item.get(name)) is not None for item in entries) else None
                   for key, name in aliases.items()}
        uncached = number(raw.get('input_tokens'))
        cached = number(raw.get('cache_read_input_tokens'))
        written = number(raw.get('cache_creation_input_tokens'))
        total = uncached+cached+written if None not in (uncached, cached, written) else None
    else:
        total = number(raw.get('input_tokens', raw.get('inputTokens')))
        cached = number(raw.get('cached_input_tokens', raw.get('cachedInputTokens')))
        uncached = total-cached if total is not None and cached is not None and total >= cached else None
        written = None  # Codex does not separately report cache writes here.
    return {'input_tokens': total, 'uncached_input_tokens': uncached,
            'cached_input_tokens': cached, 'cache_write_input_tokens': written,
            'output_tokens': number(raw.get('output_tokens', raw.get('outputTokens')))}


def _records(path):
    if not path.is_file(): return []
    records = []
    for line in path.read_text().splitlines():
        try:
            value = json.loads(line)
            if isinstance(value, dict): records.append(value)
        except ValueError:
            records.append({'event': 'malformed_evidence'})
    return records


def _union(intervals):
    total = 0.; end = None
    for low, high in sorted(intervals):
        total += max(0., high-max(low, end if end is not None else low))
        end = max(high, end if end is not None else high)
    return total


def export_metrics(run, engine):
    """Count actual host events, including setup; deduplicate terminal event identities."""
    events = _records(run_layout.path(run, 'host_log', engine))
    rows, seen = [], set()
    legacy = False
    if engine == 'claude':
        for e in events:
            if e.get('event') != 'cli_turn_completed': continue
            key = e.get('events_name')
            if not key or key in seen: continue
            seen.add(key)
            rows.append({'actor': e.get('actor'), 'session_id': e.get('session_id'),
                         'phase': e.get('phase', 'policy'),
                         'usage': usage(engine, e.get('usage'), e.get('model_usage')),
                         'usage_source': 'model_usage' if e.get('model_usage') else 'usage',
                         'reported_cost_usd': number(e.get('reported_cost_usd')),
                         'duration_s': number(e.get('duration_s')), 'ended_at': number(e.get('at'))})
        if not rows:
            legacy = True
            # Older runs remain readable. Setup usage may be absent, so this
            # fallback is explicitly partial rather than a full-run total.
            for p in sorted(run_layout.path(run, 'engine_turns', engine).glob('*-summary.json')):
                data = json.loads(p.read_text()); record = data.get('record') or {}
                summary = record.get('summary') or {}
                rows.append({'actor': data.get('actor'), 'session_id': data.get('session_id'),
                             'phase': 'policy', 'usage': usage(engine, summary.get('usage'), summary.get('model_usage')),
                             'usage_source': 'model_usage' if summary.get('model_usage') else 'usage',
                             'reported_cost_usd': number(summary.get('total_cost_usd')),
                             'duration_s': None, 'ended_at': None})
    else:
        previous = {}
        for e in events:
            if e.get('event') != 'thread/tokenUsage/updated': continue
            tid = e.get('thread_id'); value = e.get('token_usage') or {}
            total, last = value.get('total'), value.get('last')
            if not tid or not isinstance(total, dict) or not isinstance(last, dict): continue
            normalized = usage(engine, total)
            old = previous.get(tid)
            if old == normalized: continue
            delta = usage(engine, last) if old is None else {
                k: v-old[k] if v is not None and old.get(k) is not None and v >= old[k] else None
                for k, v in normalized.items()}
            previous[tid] = normalized
            rows.append({'actor': e.get('actor'), 'session_id': tid, 'phase': 'policy',
                         'usage': delta, 'reported_cost_usd': None, 'duration_s': None, 'ended_at': None})
    fields = ('input_tokens', 'uncached_input_tokens', 'cached_input_tokens', 'cache_write_input_tokens', 'output_tokens')
    totals = {k: sum(r['usage'][k] for r in rows) if rows and all(r['usage'][k] is not None for r in rows) else None for k in fields}
    known_usage = {k: sum(r['usage'][k] for r in rows if r['usage'][k] is not None)
                   if any(r['usage'][k] is not None for r in rows) else None for k in fields}
    costs = [r['reported_cost_usd'] for r in rows if r['reported_cost_usd'] is not None]
    tools = [e for e in events if e.get('event') in ('robot_tool_completed', 'robot_tool_failed')]
    tool_seconds = [number(e.get('duration_s')) for e in tools]
    setup_seconds = ([r['duration_s'] for r in rows if r['phase'] in ('snapshot_setup', 'fork_setup')]
                     if engine == 'claude' else
                     [number(e.get('duration_s')) for e in events if e.get('event') in ('snapshot_created', 'fork_created')])
    intervals = [(r['ended_at']-r['duration_s'], r['ended_at']) for r in rows
                 if r['ended_at'] is not None and r['duration_s'] is not None]
    model_seconds = [r['duration_s'] for r in rows]
    if engine == 'codex':
        completed = [e for e in events if e.get('event') == 'turn/completed']
        intervals = [(e['at']-e['duration_s'], e['at']) for e in completed
                     if number(e.get('at')) is not None and number(e.get('duration_s')) is not None]
        model_seconds = [number(e.get('duration_s')) for e in completed]
    by_actor = {}
    for actor in sorted({r['actor'] for r in rows if r['actor']}):
        selected = [r for r in rows if r['actor'] == actor]
        by_actor[actor] = {k: sum(r['usage'][k] for r in selected)
                          if all(r['usage'][k] is not None for r in selected) else None for k in fields}
    malformed = sum(e.get('event') == 'malformed_evidence' for e in events)
    started = {e.get('events_name') for e in events if e.get('event') == 'cli_turn_started'}
    unfinished = len(started-seen) if engine == 'claude' else None
    complete = not legacy and not malformed and not unfinished
    return {'schema': 'robofrontier.run-metrics.v1', 'engine': engine, 'usage': totals,
            'known_usage_subtotals': known_usage,
            'by_actor': by_actor, 'evidence_scope': 'legacy_policy_only' if legacy else 'host_observed',
            'cache_hit_rate': totals['cached_input_tokens']/totals['input_tokens']
                if totals['input_tokens'] and totals['cached_input_tokens'] is not None else None,
            'reported_cost_usd': sum(costs) if costs else None,
            'cost_complete': bool(rows) and len(costs) == len(rows) and complete,
            'rows': rows, 'phase_counts': {p: sum(r['phase'] == p for r in rows) for p in sorted({r['phase'] for r in rows})},
            'row_unit': 'cli_turn' if engine == 'claude' else 'token_usage_update',
            'unfinished_cli_turns': unfinished,
            'tool_call_count': len(tools),
            'tool_seconds_sum': sum(tool_seconds) if tool_seconds and None not in tool_seconds else None,
            'fork_setup_seconds_sum': sum(setup_seconds) if setup_seconds and None not in setup_seconds else None,
            'model_process_wall_seconds_union': _union(intervals) if intervals else None,
            'model_process_seconds_sum': sum(model_seconds) if model_seconds and None not in model_seconds else None,
            'usage_complete': bool(rows) and all(totals[k] is not None for k in ('input_tokens', 'cached_input_tokens', 'output_tokens')) and complete,
            'malformed_event_count': malformed,
            'interpretation': 'Reported usage/cost, not a provider bill. Missing values are null. '
                              'CLI wall time includes tool waits; overlapping durations are not additive wall-time shares. '
                              'Legacy summaries may omit setup; host-observed Codex counters are not native-transcript totals.'}


def native_codex_sessions(run, thread, codex_home=None):
    """Resolve an explicit home, collected mapping, batch marker, then environment.

    A known batch home which is unavailable never falls back to unrelated users'
    default sessions. This function reads neither credentials nor live databases.
    """
    if not thread: return []
    run = Path(run).resolve()
    if codex_home is not None:
        home = Path(codex_home).expanduser().resolve()
    else:
        home = None
        for parent in (run, *run.parents):
            collection = parent/'collection.json'
            if collection.is_file():
                data = json.loads(collection.read_text())
                matches = []
                for job in data.get('jobs', []):
                    if (parent/job.get('run', '')).resolve() != run: continue
                    for role in job.get('roles', []):
                        if role.get('thread_id') == thread:
                            if not isinstance(role.get('session'), str): continue
                            path = (parent/role['session']).resolve()
                            if path.is_relative_to(parent) and path.is_file(): matches.append(path)
                return sorted(set(matches))
            if parent == run: marker = run_layout.path(run, 'codex_home_marker')
            elif (parent/'batch.json').is_file(): marker = run_layout.batch_path(parent, 'codex_home_marker')
            else: marker = parent/'codex-home.json'
            if home is None and marker.is_file():
                home = Path(json.loads(marker.read_text())['codex_home']).expanduser().resolve()
        if home is None: home = Path(os.environ.get('CODEX_HOME', Path.home()/'.codex')).expanduser().resolve()
    return sorted((home/'sessions').rglob('*'+thread+'*.jsonl'))
