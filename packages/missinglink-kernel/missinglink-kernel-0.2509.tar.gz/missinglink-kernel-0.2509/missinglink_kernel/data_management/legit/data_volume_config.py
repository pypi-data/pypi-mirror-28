# -*- coding: utf8 -*-


class BasicDataVolumeConfig(object):
    def __init__(self, volume_id):
        self.volume_id = volume_id
        self.object_store_config = {}

        self._install_dependencies()

    def _install_dependencies(self):
        if 'bucket_name' in self.object_store_config and self.object_store_config['bucket_name'].startswith('s3://'):
            from missinglink_kernel.data_management.dynamic_import import install_dependencies, S3_DEPENDENCIES
            install_dependencies(S3_DEPENDENCIES)
        else:
            from missinglink_kernel.data_management.dynamic_import import install_dependencies, GCS_DEPENDENCIES
            install_dependencies(GCS_DEPENDENCIES)
