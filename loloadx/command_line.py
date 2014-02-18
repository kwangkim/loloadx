"""
This is the command line interface to quickly
load a folder with edx xml courses into a vagrant
fullstack instance.
"""

from loloadx.util import CourseImporter
from loloadx.config import conf

def execute():
    """
    Import the courses in the directory
    """

    importer = CourseImporter()
    importer.load_course_dir()
    if conf['debug']:
        print('\n'.join(importer.messages))
