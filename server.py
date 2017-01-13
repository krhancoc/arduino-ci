""" Arduino Continuous Integration Tool Server for Mac-OS/Linux

This server allows for multiple developers to work on one Arduino Chip that could be attached
to a robot that you may not necessarily have two of!

Please follow the README.md for start up instruction and problems you may run into.

Attributes:
    UPLOAD_FOLDER (str): Folder in which uploads will temporarily be stored
    ALLOWED_EXTENSIONS (set): List of allowed extensions the server will take
    app (object): The flask app server

TODO:
    Add Support for libraries
    Add UI too allow different libraries to be loaded with the build.
"""

import os
import subprocess
import logging

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'ino'}
app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "WHATEVERYOUWANTBRO"


class InoTool():
    """Tool used to build and upload files handed to it by the server

    Attributes:
        upload_lock (bool): Lock that is set when a user is uploading. Stops other users from uploading as well.

    """

    def __init__(self):
        """Tool will only init the lock attribute"""
        self.upload_lock = False

    def is_locked(self):
        """Checks if upload lock is locked"""
        return self.upload_lock

    def lock(self):
        """Locks upload lock"""
        self.upload_lock = False

    def unlock(self):
        """Unlocks upload lock"""
        self.upload_lock = True

    def process(self, filename):
        """Kicks of build and upload process by calling integration.sh within bin/

        Args:
            filename (str): Filename that will be passed to the integration.sh script

        Returns:
            bool: Returns if the script errors or not any any point.  True for Success.

        """

        self.lock()
        app.logger.debug("Calling integration.sh script with filename: " + filename)
        if (subprocess.call("bin/integration.sh " + filename, shell=True) is 0):
            app.logger.error("Problem Running Integration Script")
            self.unlock()
            return False
        else:
            app.logger.info("Integration script run without error")
            self.unlock()
            return True


# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    logging.debug("Rendering index.html template")
    return render_template('index.html')


# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/submit', methods=['POST'])
def upload_file():
    if request.method == 'POST' and not app.tool.is_locked():
        uploaded_file = request.files.get('ino', None)
        if (uploaded_file is None) or (uploaded_file.filename == ''):
            flash('No file given or Bad Extension')
        elif allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            app.logger.info('File ' + filename + " accepted.  Moving through to build and upload")
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.tool.process(filename)
            flash('Success!')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.tool = InoTool()
    app.run(debug=True)
