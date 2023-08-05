# coding=utf-8
import requests
import six

from .legit.data_volume_config import BasicDataVolumeConfig
from .legit.config import Config, default_config_file
from .legit.api import handle_api
from .legit.clone import clone as clone_data_volume


class DataVolume(object):
    def __init__(self, volume_id, config=None):
        self.volume_id = volume_id
        self.data_volume_config = BasicDataVolumeConfig(volume_id)

        if isinstance(config, Config):
            self.config = config
        else:
            config_path = config if isinstance(config, six.string_types) else default_config_file(None)
            self.config = Config(config_file=config_path)

    def get_data_volume(self):
        result = handle_api(self.config, requests.get, 'data_volumes/%s' % self.volume_id)
        return result

    def clone(self, version_id, dir_structure='$@phase/$@name', cache_dir=None, data_volume_dir=None, use_cache=False):
        data_volume_root_dir = clone_data_volume(self.config, self.volume_id, version_id,
                                                 dir_structure, cache_dir, data_volume_dir,
                                                 use_cache=use_cache)

        return data_volume_root_dir
