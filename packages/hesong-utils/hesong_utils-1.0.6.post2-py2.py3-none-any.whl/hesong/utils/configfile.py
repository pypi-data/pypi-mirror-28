from __future__ import absolute_import, unicode_literals

import os.path
from io import FileIO

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

try:
    import yaml
except ImportError:
    yaml = None
else:
    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader

from .jsonutils import json_loads

__all__ = ['load']


def load(fname):
    """
    Load a dict config from ``ini``, ``json`` or ``yaml`` file
    :param str fname: config file path name, ``*.ini``, ``*.json`` or ``*.yaml``
    :return: configuration's dict object
    :rtype: dict
    """
    _, ext = os.path.splitext(fname)
    ext = ext.lower()
    if ext == '.yaml':
        if yaml:
            config = yaml.load(FileIO(fname), YamlLoader)
        else:
            raise RuntimeError('yaml package not installed')
    elif ext == '.json':
        config = json_loads(open(fname).read())
    elif ext == '.ini':
        config_parser = ConfigParser()
        config_parser.read(fname)
        config = {}
        # Python 2.6 can not be like so
        # config = {s: dict(config_parser.items(s)) for s in config_parser.sections()}
        # changed to:
        for s in config_parser.sections():
            config[s] = dict(config_parser.items(s))
    else:
        raise RuntimeError('Unknown logging config file ext name: {0}'.format(fname))
    return config
