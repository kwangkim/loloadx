"""
Simplistic flask application for reloading the
local courses from a Web interface
"""

from flask import Flask
from flask import escape, request, make_response

from loloadx.util import CourseImporter
from loloadx.config import conf
from loloadx.webutil import crossdomain

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    """
    Display configuratio and available courses.
    """
    output = 'Configuration:<br />'
    for key in conf.keys():
        output += '{0}: {1}<br />'.format(key, conf[key])
    output += "<br />Courses:<br />"
    for course in CourseImporter().course_list():
        output += "{0}<br />".format(course)
    return output


@app.route('/load_all', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def load_all():
    """
    Load the configured directory into the edX store
    """
    if request.method == 'POST':
        importer = CourseImporter()
        importer.load_course_dir()
        return '\n'.join(importer.messages)


@app.route('/load_course', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def load_course():
    """
    Load a specified course specified by the directory
    the course is in.
    """
    if request.method == 'POST':
        use_dir = True
        course_dir = request.form.get('course_dir', None)
        course_id = request.form.get('course_id', None)
        if not (course_dir or course_id):
            return ('No course identified specified. '
                    'Either directory or course id expected.')

        if course_id:
            use_dir = False
        importer = CourseImporter()

        if course_id:
            course_dir = importer.course_by_id(course_id)
            if not course_dir:
                return 'No course found by ID {0}'.format(course_id)

        if not course_dir in importer.course_list():
            return 'No course found in {0} directory'.format(course_path)

        importer.import_course(course_dir)
            
        return '\n'.join(importer.messages)


def run_web():
    app.debug = False
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    run_web()
