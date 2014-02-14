"""
Utility functions for actually loading courses
"""

import os
import subprocess

from loloadx.config import conf

def vprint(*args):
    """Print stuff if debug is turned on."""
    if conf['debug']:
        for arg in args:
            print(arg)


class CourseImporter(object):
    """
    Handles importing courses based on settings, into directory
    """
    def __init__(self, edx_venv=conf['edx_venv'],
                 edx_root=conf['edx_root'], course_dir=conf['course_dir']):
        """Setup all the internals for running methods"""

        self.edx_venv = edx_venv
        self.edx_root = edx_root
        self.course_dir = course_dir

    def import_course(self, course, static=True):
        """
        Load the specified course into edx using the management command.
        """
        import_cmd = ['{0}/bin/python'.format(self.edx_venv),
                      'manage.py', 'lms', '--settings=aws',
                      'import', self.course_dir, course, ]
        if not static:
            import_cmd.append('--nostatic')
        vprint(import_cmd)
        wd = '{0}/{1}'.format(self.edx_root, 'edx-platform')
        vprint(wd)
        course_import = subprocess.check_output(import_cmd, cwd=wd)
        return course_import

    def load_course_dir(self):
        """
        Loop through all courses in the directory and
        load them up.
        """
        for dirname in os.listdir(self.course_dir):
            fullpath = os.path.join(self.course_dir, dirname)
            if os.path.isdir(fullpath):
                vprint('Importing course {0} from {1}'.format(
                    dirname, self.course_dir))
                vprint(self.import_course(dirname))
