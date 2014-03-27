"""
Utility functions for actually loading courses
"""
# pylint: disable=c0103

import os
import re
import subprocess

from loloadx.config import conf


class CourseImporter(object):
    """
    Handles importing courses based on settings, into directory
    """
    def __init__(self, edx_venv=conf['edx_venv'],
                 edx_root=conf['edx_root'], course_dir=conf['course_dir'],
                 import_static=conf['import_static']):
        """Setup all the internals for running methods"""

        self.edx_venv = edx_venv
        self.edx_root = edx_root
        self.course_dir = course_dir
        self.import_static = import_static
        self.messages = []

    def course_list(self):
        """
        Use directory listing to get a list of courses.
        """
        courses = []
        if not os.path.isdir(self.course_dir):
            self.messages.append('Course directory {0} doesn\'t exist, '
                                 'please create it.'.format(self.course_dir))
            return courses
        for dirname in os.listdir(self.course_dir):
            fullpath = os.path.join(self.course_dir, dirname)
            if os.path.isdir(fullpath):
                courses.append(dirname)
        return courses

    def course_by_id(self, course_id):
        """
        Trounce through course xml and try to find the id given.
        Return the course directory found.
        """
        course_m = re.search(r'(?P<org>[\w_\.\-]+)/(?P<name>[\w_\.\-]+)',
                             course_id)
        if not course_m:
            self.messages.append('Invalid course_id passed in')
            return None
        course_dict = course_m.groupdict()
        org = course_dict['org']
        name = course_dict['name']

        for course in self.course_list():
            course_xml = '{0}/{1}/course.xml'.format(self.course_dir, course)
            if os.path.exists(course_xml):
                with open(course_xml, 'r') as fp:
                    courseml = fp.read()
                m = re.search(r'org="(?P<org>[\w_\.\-]+)"', courseml)
                if m:
                    if org == m.groupdict()['org']:
                        m = re.search(r'course="(?P<course>[\w_\.\-]+)"',
                                      courseml)
                        if m:
                            if name == m.groupdict()['course']:
                                return course
        return None

    def import_course(self, course):
        """
        Load the specified course into edx using the management command.
        """
        import_cmd = ['{0}/bin/python'.format(self.edx_venv),
                      'manage.py', 'lms', '--settings=aws',
                      'import', self.course_dir, course, ]
        if not self.import_static:
            import_cmd.append('--nostatic')
        full_course_dir = '{0}/{1}'.format(self.course_dir, course)

        if not os.path.isdir(full_course_dir):
            self.messages.append('Course does not '
                                 'exist at {0}'.format(full_course_dir))
            return False
        self.messages.append(' '.join(import_cmd))
        wd = '{0}/{1}'.format(self.edx_root, 'edx-platform')
        self.messages.append(wd)
        try:
            course_import = subprocess.check_output(import_cmd, cwd=wd,
                                                    stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            self.messages.append("Unable to import course: {0!r}".format(
                ex.output))
            return False
        self.messages.append(course_import)
        return True

    def load_course_dir(self):
        """
        Loop through all courses in the directory and
        load them up.
        """
        courses = self.course_list()
        if len(courses) == 0:
            self.messages.append('No courses found, does {0} have '
                                 'a course in it?'.format(self.course_dir))
        for course in courses:
            self.messages.append('Importing course {0} from {1}'.format(
                course, self.course_dir))
            self.import_course(course)
