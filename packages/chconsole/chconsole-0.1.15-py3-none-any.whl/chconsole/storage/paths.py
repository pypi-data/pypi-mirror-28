# encoding: utf-8
"""Path utility functions."""

# Copyright (c) 2016, Manfred Minimair
# Distributed under the terms of the Modified BSD License.

# Derived from jupyter_core.paths, which is
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Derived from IPython.utils.path, which is
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.


import os
import sys


def get_home_dir():
    """Get the real path of the home directory"""
    home_dir = os.path.expanduser('~')
    # Next line will make things work even when /home/ is a symlink to
    # /usr/home as it is on FreeBSD, for example
    home_dir = os.path.realpath(home_dir)
    return home_dir


def chconsole_config_dir():
    """Get the config directory for this platform and user.
    
    Returns CHCONSOLE_CONFIG_DIR if defined, else ~/.chconsole
    """

    env = os.environ
    home_dir = get_home_dir()

    if env.get('CHCONSOLE_CONFIG_DIR'):
        return env['CHCONSOLE_CONFIG_DIR']
    
    return os.path.join(home_dir, '.chconsole')


def chconsole_data_dir():
    """Get the config directory for data files.
    
    These are non-transient, non-configuration files.
    
    Returns CHCONSOLE_DATA_DIR if defined, else a platform-appropriate path.
    """
    env = os.environ
    
    if env.get('CHCONSOLE_DATA_DIR'):
        return env['CHCONSOLE_DATA_DIR']
    
    home = get_home_dir()

    if sys.platform == 'darwin':
        return os.path.join(home, 'Library', 'Chconsole')
    elif os.name == 'nt':
        app_data = os.environ.get('APPDATA', None)
        if app_data:
            return os.path.join(app_data, 'chconsole')
        else:
            return os.path.join(chconsole_config_dir(), 'data')
    else:
        # Linux, non-OS X Unix, AIX, etc.
        xdg = env.get("XDG_DATA_HOME", None)
        if not xdg:
            xdg = os.path.join(home, '.local', 'share')
        return os.path.join(xdg, 'chconsole')
