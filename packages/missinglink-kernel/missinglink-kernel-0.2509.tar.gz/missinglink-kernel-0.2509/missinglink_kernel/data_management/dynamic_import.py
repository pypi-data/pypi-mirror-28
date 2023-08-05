# coding=utf-8
import sys
import logging
import threading
from pkg_resources import get_distribution, DistributionNotFound

from missinglink.pip_util import pip_install, get_pip_server


COMMON_DEPENDENCIES = {
    'ply': '3.8',
    'flatten_json': '0.1.6',
    'tqdm': '4.19.4',
    'pyparsing': '2.2',
    'google-cloud-core': '0.28.0',
}
GCS_DEPENDENCIES = {
    'google-cloud-storage': '1.6.0',
}
S3_DEPENDENCIES = {
    'boto3': '1.4.8'
}
KEYWORDS = []


__pip_install_lock = threading.Lock()


def install_dependencies(dependencies, throw_exception=True):
    running_under_virtualenv = getattr(sys, 'real_prefix', None) is not None

    for dependency, version in dependencies.items():
        if _dependency_installed(dependency, version):
            continue

        with __pip_install_lock:
            if _dependency_installed(dependency, version):
                # if it is already installed in another thread, release the lock early.
                continue

            p, args = pip_install(get_pip_server(KEYWORDS),
                                  '%s==%s' % (dependency, version),
                                  not running_under_virtualenv)

            if p is None:
                raise Exception('Failed to install requirement: %s' % dependency)

            try:
                std_output, std_err = p.communicate()
            except Exception:
                if throw_exception:
                    raise

                logging.exception('%s failed', ' '.join(args))
                return False

            rc = p.returncode

            if rc != 0:
                logging.error('Failed to install requirement: %s' % dependency)
                logging.error('Failed to run %s (%s)\n%s\n%s', ' '.join(args), rc, std_err, std_output)

                if throw_exception:
                    raise Exception('Failed to install requirement: %s' % dependency)


def _dependency_installed(dependency, version=None):
    try:
        dist = get_distribution(dependency)

        if version is None:
            return True

        return dist.version == version
    except DistributionNotFound:
        return False
