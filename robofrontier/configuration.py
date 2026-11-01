"""Resolve and validate one public configuration before preparing frozen inputs."""
from copy import deepcopy
import math
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'robofrontier.toml'
TOPOLOGIES = {
    'single': 'centralized',
    'controller-worker': 'hierarchical',
    'worker-worker': 'peer',
    'adaptive': 'adaptive',
}
SCHEMA = {
    'schema_version': int,
    'policy': dict.fromkeys(('engine', 'profile', 'effort', 'topology'), str),
    'batch': {'parallel': int, 'startup_interval_s': float, 'task_wall_limit_s': float, 'startup_timeout_s': float},
    'selection': {'families': list, 'cases': list, 'level': int, 'min_arms': bool},
    'render': {'device': str, 'observation_profile': str, 'record_realtime_video': bool},
    'runtime': {'codex_home_scope': str, 'codex_home': str},
    'evidence': {'auto_collect': bool, 'auto_archive': bool, 'archive_format': str, 'delete_sources': bool},
}


def _validate_shape(values, schema, prefix=''):
    if not isinstance(values, dict) or set(values) != set(schema):
        raise ValueError('Missing or unknown configuration options in ' + (prefix or 'root'))
    for key, kind in schema.items():
        name = prefix + key
        if isinstance(kind, dict):
            _validate_shape(values[key], kind, name + '.')
        elif type(values[key]) is not kind and not (kind is float and type(values[key]) is int):
            raise ValueError('Incorrect configuration type: ' + name)


def _merge(base, updates, prefix=''):
    for key, value in updates.items():
        name = prefix + key
        if key not in base:
            raise ValueError('Unknown configuration option: ' + name)
        if isinstance(base[key], dict):
            if not isinstance(value, dict):
                raise ValueError('Expected a configuration section: ' + name)
            _merge(base[key], value, name + '.')
        else:
            if type(value) is not type(base[key]) and not (
                    type(base[key]) is float and type(value) is int):
                raise ValueError('Incorrect configuration type: ' + name)
            base[key] = value


def load_configuration(path=None, overrides=None):
    """Layer a partial user TOML and explicit options over checked-in defaults.

    Secrets and arbitrary environment expansion are deliberately not supported.
    Old prepared runs keep their frozen configuration and are never re-resolved.
    """
    with DEFAULT.open('rb') as stream:
        result = tomllib.load(stream)
    if path is not None and Path(path).resolve() != DEFAULT.resolve():
        with Path(path).open('rb') as stream:
            _merge(result, tomllib.load(stream))
    if overrides:
        _merge(result, deepcopy(overrides))
    validate_configuration(result)
    return result


def validate_configuration(config):
    _validate_shape(config, SCHEMA)
    def choice(section, field, allowed):
        if config[section][field] not in allowed:
            raise ValueError(f'Invalid {section}.{field}: choose from {", ".join(map(str, allowed))}')

    if type(config['schema_version']) is not int or config['schema_version'] != 1:
        raise ValueError('Unsupported configuration schema_version')
    choice('policy', 'engine', ('codex', 'claude'))
    choice('policy', 'topology', TOPOLOGIES)
    choice('policy', 'effort', ('minimal', 'low', 'medium', 'high', 'xhigh', 'max'))
    from re import fullmatch
    if not fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', config['policy']['profile']):
        raise ValueError('Invalid policy.profile identifier')
    batch = config['batch']
    if type(batch['parallel']) is not int or not 1 <= batch['parallel'] <= 36:
        raise ValueError('batch.parallel must be 1..36')
    for field in ('startup_interval_s', 'task_wall_limit_s', 'startup_timeout_s'):
        value = batch[field]
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or (
                field != 'startup_interval_s' and value == 0):
            raise ValueError('Invalid batch.' + field)
    if config['policy']['engine'] == 'claude' and batch['task_wall_limit_s'] > 86400:
        raise ValueError('The current Claude engineering runner supports at most 86400 seconds')
    choice('selection', 'level', (0, 1, 2, 3))
    if type(config['selection']['level']) is not int:
        raise ValueError('selection.level must be an integer')
    for field in ('families', 'cases'):
        values = config['selection'][field]
        if not all(type(value) is str and value for value in values) or len(set(values)) != len(values):
            raise ValueError('selection.' + field + ' must contain distinct nonempty strings')
    choice('render', 'device', ('nvidia', 'cpu', 'native'))
    choice('render', 'observation_profile', ('jpeg_896x560_q85', 'png_1280x800'))
    choice('runtime', 'codex_home_scope', ('task', 'shared'))
    choice('evidence', 'archive_format', ('zip',))
    if config['evidence']['auto_archive'] and not config['evidence']['auto_collect']:
        raise ValueError('evidence.auto_archive requires evidence.auto_collect')
    if config['evidence']['delete_sources']:
        raise ValueError('Automatic source deletion is not supported; verify restored evidence before explicit cleanup')


def rendering_environment(device, system, base):
    """Set the chosen backend explicitly; never silently fall back to software."""
    env = dict(base)
    for key in ('MUJOCO_GL', 'PYOPENGL_PLATFORM', 'LIBGL_ALWAYS_SOFTWARE', 'GALLIUM_DRIVER'):
        env.pop(key, None)
    if device == 'native':
        if system != 'Darwin':
            raise ValueError('native rendering requires macOS; select nvidia or cpu on Linux')
    elif device == 'cpu':
        if system != 'Linux':
            raise ValueError('CPU OSMesa rendering requires Linux, including a Linux Docker container')
        env.update(MUJOCO_GL='osmesa', PYOPENGL_PLATFORM='osmesa',
                   LIBGL_ALWAYS_SOFTWARE='true', GALLIUM_DRIVER='llvmpipe', CUDA_VISIBLE_DEVICES='')
    elif device == 'nvidia':
        if system != 'Linux':
            raise ValueError('NVIDIA EGL rendering requires Linux; select native on macOS')
        env.update(MUJOCO_GL='egl', PYOPENGL_PLATFORM='egl', LIBGL_ALWAYS_SOFTWARE='false')
    else:
        raise ValueError('Unknown rendering device')
    return env
