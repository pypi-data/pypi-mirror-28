# coding: utf-8

import pbr.version

from cfgtree.cfgtree import EnvironmentConfig

__version__ = pbr.version.VersionInfo('cfgtree').release_string()
VERSION = __version__

__all__ = [
    '__version__',
    'EnvironmentConfig',
    'VERSION',
]
