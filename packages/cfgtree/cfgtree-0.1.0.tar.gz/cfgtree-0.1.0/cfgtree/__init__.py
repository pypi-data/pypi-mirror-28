# coding: utf-8

import pbr.version

__version__ = pbr.version.VersionInfo('cfgtree').release_string()
VERSION = __version__

__all__ = [
    '__version__',
    'VERSION',
]
