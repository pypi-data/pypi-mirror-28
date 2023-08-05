# coding=utf-8
try:
    from keras.preprocessing.image import ImageDataGenerator
except ImportError:
    ImageDataGenerator = object

import os


class MLImageDataGenerator(ImageDataGenerator):
    def __init__(self, *args, **kwargs):
        if ImageDataGenerator is object:
            raise ImportError('The use of MLImageDataGenerator requires Keras installed.')

        from missinglink_kernel.data_management.dynamic_import import install_dependencies, COMMON_DEPENDENCIES
        install_dependencies(COMMON_DEPENDENCIES)

        super(MLImageDataGenerator, self).__init__(*args, **kwargs)

        self._ml_data_volume = None
        self._ml_data_downloaded = False
        self._ml_data_volume_dir = None

    def use_data_volume(self, volume_id, version_id,
                        dir_structure='$@phase/$@name',
                        lazy=False, use_cache=True, config=None):
        from .data_volume import DataVolume

        self._ml_data_volume = DataVolume(volume_id, config)
        self._ml_data_downloaded = False

        if not lazy:
            self._ml_data_volume_dir = self._ml_data_volume.clone(version_id,
                                                                  dir_structure=dir_structure,
                                                                  use_cache=use_cache)
            self._ml_data_downloaded = True
        else:
            # TODO: suppport lazy=True, cloning on demand
            pass

    def flow_from_train_dir(self, *args, **kwargs):
        train_dir = self._get_sub_dir(self._ml_data_volume_dir, 'train')
        return self.flow_from_directory(train_dir, *args, **kwargs)

    def flow_from_validation_dir(self, *args, **kwargs):
        validation_dir = self._get_sub_dir(self._ml_data_volume_dir, 'validation')
        return self.flow_from_directory(validation_dir, *args, **kwargs)

    def flow_from_test_dir(self, *args, **kwargs):
        test_dir = self._get_sub_dir(self._ml_data_volume_dir, 'test')
        return self.flow_from_directory(test_dir, *args, **kwargs)

    def _get_sub_dir(self, download_dir, sub_dir):
        from .legit.exceptions import MissingLinkException

        if not self._ml_data_downloaded or not os.path.exists(download_dir):
            raise MissingLinkException("Data volume wasn't downloaded.")

        sub_dir = os.path.join(download_dir, sub_dir)

        if not os.path.exists(sub_dir):
            raise MissingLinkException("Data directory '%s' doesn't exist." % sub_dir)

        return sub_dir
