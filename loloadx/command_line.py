"""
This is the command line interface to quickly
load a folder with edx xml courses into a vagrant
fullstack instance.
"""

import argparse
import os
import sys

from loloadx.util import CourseImporter
from loloadx.config import conf


def print_config():
    """
    Returns a raw formatted string with the current configuration
    """
    config_list = []
    for key in conf.keys():
        config_list.append('{0}: {1}'.format(key, conf[key]))
    return '\n'.join(config_list)


def execute():
    """
    Import the courses in the directory
    """
    parser = argparse.ArgumentParser(
        prog='loloadx',
        formatter_class=argparse.RawTextHelpFormatter,
        description=('''
Load courses in the configured directory into the edx-platform.

Configuration can be set by setting options in the loloadx section of an INI
file in the current directory as loloadx.conf, /etc/loloadx.conf, or
~/.loloadx.conf

You can choose to load a specific course by specifying that courses directory
as an argument

Current Configuration:
{0}
        '''.format(print_config()))
    )
    parser.add_argument(
        'course',
        default=None,
        nargs='?',
        help='Course specific directory or ID to load'
    )
    args = parser.parse_args()

    importer = CourseImporter()
    if args.course:
        course = None
        # Try config based course_dir
        if args.course in importer.course_list():
            course = args.course

        # Try course_id based argument
        if not course:
            course_id_dir = importer.course_by_id(args.course)
            if course_id_dir in importer.course_list():
                course = course_id_dir

        # Try loading by path
        if not course:
            course_full_path = os.path.abspath(args.course)
            if os.path.isdir(course_full_path):
                importer.course_dir, p_course = os.path.split(course_full_path)
                if p_course in importer.course_list():
                    course = p_course

        if not course:
            sys.stderr.write('I could not find the course by ID or path.\n')
            sys.exit(-1)

        importer.import_course(course)
    else:
        importer.load_course_dir()

    if conf['debug']:
        sys.stdout.write('\n'.join(importer.messages))
        sys.stdout.write('\n')
