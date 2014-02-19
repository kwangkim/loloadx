"""
Handle setting up the configuration for the app
"""
# pylint: disable=c0103

import ConfigParser
import os


def get_settings():
    """Load settings or use defaults"""

    settings = {
        'edx_root': '/edx/app/edxapp',
        'edx_venv': '/edx/app/edxapp/venvs/edxapp',
        'course_dir': '/vagrant/courses',
        'debug': True,
        'import_static': True,
    }

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read([
        '/etc/loloadx.conf',
        os.path.expanduser('~/.loloadx.conf'),
        os.getcwd() + '/loloadx.conf',
    ])

    for key in settings.keys():
        try:
            settings[key] = config_parser.get('loloadx', key)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            pass
    return settings

conf = get_settings()
