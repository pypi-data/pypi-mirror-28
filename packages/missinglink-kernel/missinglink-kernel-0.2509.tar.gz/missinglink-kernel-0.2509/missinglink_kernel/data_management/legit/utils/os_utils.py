# -*- coding: utf8 -*-
import os
import shutil
import errno


def create_dir(dirname):
    if not dirname or os.path.exists(dirname):
        return

    try:
        os.makedirs(dirname)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def safe_make_dirs(dir):
    try:
        os.makedirs(dir)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def safe_rm_tree(path):
    try:
        shutil.rmtree(path)
    except OSError as ex:
        if ex.errno != errno.ENOENT:
            raise
