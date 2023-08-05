# coding=utf-8
import os
import requests
from contextlib import closing
from hashlib import sha256

from tqdm import tqdm

from .db.backend_conection import BackendConnection
from .metadata_db import BackendMetadataDB
from .object_store import BackendGCSObjectStore
from .data_volume_config import BasicDataVolumeConfig
from .config import Config
from .api import handle_api
from .utils.os_utils import safe_make_dirs, safe_rm_tree
from .multi_process_control import get_multi_process_control


BATCH_SIZE = 500
NUM_PROCESSES = -1


def clone(config, volume_id, version_id, dir_structure, cache_dir=None, data_volume_dir=None, use_cache=False):
    metadata_db = _create_metadata_db(config, volume_id)
    multi_process_control = get_multi_process_control(NUM_PROCESSES)

    # TODO: version can be `head` so cannot cache in that case
    query = '@version:%s @seed:1337' % version_id
    dest_root_dir = _get_destination_root_dir(cache_dir, data_volume_dir, query, dir_structure)

    if use_cache and os.path.exists(dest_root_dir):
        return dest_root_dir

    safe_rm_tree(dest_root_dir)

    dest_dir = os.path.join(dest_root_dir, dir_structure)

    with closing(multi_process_control):
        start_index = 0
        results, total_data_points = _get_next_results(metadata_db, query, start_index)

        with tqdm(total=total_data_points, desc='Downloading', unit=' data point', ncols=80) as bar:
            while True:
                for item in results:
                    item = _normalize_item(item)
                    multi_process_control.execute(_download_entity,
                                                  args=(config.init_dict, volume_id, dest_dir, item),
                                                  callback=lambda _: bar.update())

                if len(results) != BATCH_SIZE:
                    break

                start_index += len(results)
                results, _ = _get_next_results(metadata_db, query, start_index)

    return dest_root_dir


def _create_metadata_db(config, volume_id):
    data_volume_config = BasicDataVolumeConfig(volume_id)
    return BackendMetadataDB(BackendConnection(data_volume_config), config, handle_api)


def _create_object_store(config, volume_id):
    data_volume_config = BasicDataVolumeConfig(volume_id)
    return BackendGCSObjectStore(BackendConnection(data_volume_config), config, handle_api,
                                 use_multiprocess=True, processes=-1)


def _get_destination_root_dir(cache_dir, data_volume_dir, query, dir_structure):
    cache_dir = cache_dir or _default_cache_dir()
    data_volume_dir = data_volume_dir or _default_data_volume_dir(query, dir_structure)

    return os.path.join(cache_dir, data_volume_dir)


def _default_cache_dir():
    return os.path.join(os.path.expanduser('~'), '.MissingLinkAI')


def _default_data_volume_dir(query, dir_structure):
    return sha256('%s-%s' % (query, dir_structure)).hexdigest()


def _get_next_results(metadata_db, query, start_index=0):
    result_generator, total = metadata_db.query(query, max_results=BATCH_SIZE, start_index=start_index)
    return list(result_generator), total


def _download_entity(config_init_dict, volume_id, dest_dir, item):
    import google.api_core.exceptions

    config = Config(**config_init_dict)
    object_store = _create_object_store(config, volume_id)

    try:
        _, data = object_store.get_raw(item['@id'])
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            return

        raise
    except google.api_core.exceptions.NotFound:
        return

    phase = item.get('@phase')

    if phase is None:
        return

    _, file_extension = os.path.splitext(item['@path'])

    _add_sys_var('phase', phase, item)
    _add_sys_var('path', item['@path'], item)
    _add_sys_var('name', os.path.basename(item['@path']), item)
    _add_sys_var('dir', os.path.dirname(item['@path']), item)
    _add_sys_var('ext', os.path.basename(file_extension), item)

    item['@'] = phase

    dest_file = _fill_in_vars(dest_dir, item)

    safe_make_dirs(os.path.dirname(dest_file))

    def append_id(filename, uid):
        name, ext = os.path.splitext(filename)
        return "{name}_{uid}{ext}".format(name=name, uid=uid, ext=ext)

    if os.path.exists(dest_file):
        dest_file = append_id(dest_file, item['@id'])

    with open(dest_file, 'wb') as f:
        f.write(data)


def _normalize_item(item):
    result_item = {}

    for key, val in item.items():
        if key == 'meta':
            continue

        result_item['@' + key] = val

    for key, val in item.get('meta', {}).items():
        result_item[key] = val

    return result_item


def _fill_in_vars(path, replace_vars):
    replace_vars_keys = sorted(replace_vars.keys(), reverse=True)

    for var_name in replace_vars_keys:
        var_value = replace_vars[var_name]
        path = path.replace('$' + var_name, str(var_value))
        path = path.replace('#' + var_name, str(var_value))

    return path


def _add_sys_var(name, value, current_vars):
    current_vars['@' + name] = value

    if name not in current_vars:
        current_vars[name] = value
