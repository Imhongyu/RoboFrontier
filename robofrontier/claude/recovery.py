"""Bounded capacity recovery; never resubmits robot requests or recreates forks."""
from robofrontier.claude.native_home import history_directory
import json
import time

from robofrontier.claude.provenance import history, transcript_rows
from robofrontier import run_layout

MAX_CAPACITY_RETRIES = 3
BASE_DELAY_SECONDS = 10
MAX_DELAY_SECONDS = 60
CAPACITY_CODES = frozenset(('rate_limit', 'rate_limit_error', 'overloaded_error', 'server_overloaded'))
CONTINUE_PROMPT = ('The previous model turn ended with a confirmed capacity or rate-limit error. '
                   'Continue the same running task and saved work. Inspect pending and original job IDs '
                   'before further actions; do not replay submitted motion or recreate delegates. '
                   'The experiment has already STARTED; continue without another START. '
                   'The original task deadline still applies.')


def capacity_code(events):
    """Only structured CLI/API error fields count, never model text or stderr."""
    for event in reversed(events):
        if event.get('type') == 'assistant' and event.get('isApiErrorMessage') is True:
            code = event.get('error')
        elif event.get('type') == 'error' and isinstance(event.get('error'), dict):
            code = event['error'].get('type')
        else:
            continue
        if isinstance(code, dict): code = code.get('type')
        return code if isinstance(code, str) and code in CAPACITY_CODES else None
    return None


def recover(host, store, now=None):
    """Return True while safely waiting/retrying; False leaves ordinary error handling.

    Caller keeps polling its original deadline and STOP. Successful retries stay
    in the same native session. Unknown process outcomes and uncertain costs under
    explicit caps never enter this path.
    """
    now = time.monotonic() if now is None else now
    with host.lock:
        if (host.state != 'error' or not host.retryable_capacity
                or host.capacity_retry_count >= host.max_capacity_retries
                or host.cancel_event.is_set() or run_layout.path(host.run, 'stop', 'claude').exists()
                or store.get('lifecycle') != 'running' or store.get('dispatch_paused', False)):
            return False
        try:
            if not history(transcript_rows(history_directory(host.run), host.session_id), host.session_id): return False
        except ValueError:
            return False
        actions = store.actions(host.actor).values()
        if any(a['status'] == 'uncertain' for a in actions): return False
        busy = any(a['status'] in ('pending', 'running') for a in store.actions(host.actor).values())
        busy = busy or bool(store.db.execute("SELECT 1 FROM calls WHERE actor=? AND status='accepted' LIMIT 1",
                                            (host.actor,)).fetchone())
        # A tool-free creation turn must not be retried through this mechanism.
        if any(b['status'] == 'creating' for b in store.get('delegations', {}).values()): return False
        if host.capacity_retry_due is None:
            host.capacity_retry_due = now + min(MAX_DELAY_SECONDS, BASE_DELAY_SECONDS * 2**host.capacity_retry_count)
            host.event('capacity_wait', retry_number=host.capacity_retry_count+1,
                       error_code=(host.last_result or {}).get('summary', {}).get('capacity_error_code'),
                       max_retries=host.max_capacity_retries,
                       delay_s=host.capacity_retry_due-now)
        if busy or now < host.capacity_retry_due: return True
        host.capacity_retry_count += 1
        host.capacity_retry_due = None
        host.retryable_capacity = False
        host.state = 'idle'  # Proven failure; this is a resume, never a new session.
        host.event('capacity_retry', retry_number=host.capacity_retry_count)
        try:
            host.send(CONTINUE_PROMPT)
        except Exception:
            host.state = 'unknown'
            raise
        return True
