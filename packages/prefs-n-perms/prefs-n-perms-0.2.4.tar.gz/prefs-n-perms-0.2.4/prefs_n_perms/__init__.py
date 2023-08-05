import os


def _get_git_revision(path):
    revision_file = os.path.join(path, 'refs', 'heads', 'master')
    if not os.path.exists(revision_file):
        return None
    fh = open(revision_file, 'r')
    try:
        return fh.read().strip()[:7]
    finally:
        fh.close()


def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir))
    path = os.path.join(checkout_dir, '.git')
    if os.path.exists(path):
        return _get_git_revision(path)
    return None


def get_version():
    base = __version__
    if __build__:
        base = '%s (%s)' % (base, __build__)
    return base


__version__ = '0.2.4'
__build__ = get_revision()
VERSION = get_version()

default_app_config = 'prefs_n_perms.apps.PrefsNPermsConfig'
from prefs_n_perms.registries import section_registry, model_registry
