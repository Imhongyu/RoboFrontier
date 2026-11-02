"""Locate native session history without copying a managed credential store."""
import json
from pathlib import Path


def config_directory(run, profile=None):
    run = Path(run)
    if profile is None:
        launch = run / 'private/inputs/claude.json'
        profile = json.loads(launch.read_text()).get('profile', {}) if launch.is_file() else {}
    if profile.get('auth_mode') != 'native_login':
        return run / 'private/claude-config'
    if profile.get('provider') != 'anthropic' or profile.get('env_key'):
        raise ValueError('Native login requires Anthropic and no credential environment variable')
    value = profile.get('native_config_dir')
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        raise ValueError('Native login requires an explicit absolute configuration directory')
    home = Path(value).resolve()
    if not home.is_dir():
        raise ValueError('Native login configuration directory is missing')
    return home


def history_directory(run, profile=None):
    """Stopped exports use their collected sessions, never the original account."""
    run = Path(run)
    marker = run / 'private/state/claude-collected-sessions.json'
    if marker.is_file():
        saved = json.loads(marker.read_text())
        if (saved.get('schema') != 'robofrontier.claude-collected-sessions.v1'
                or saved.get('writers_stopped') is not True):
            raise ValueError('Invalid collected native session marker')
        return run / 'private/claude-config'
    return config_directory(run, profile)
