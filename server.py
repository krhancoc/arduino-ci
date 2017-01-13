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


def process(filename):
    app.logger.debug("Calling integration.sh script with filename: " + filename)
    subprocess.call("bin/integration.sh " + filename, shell=True)


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
    if request.method == 'POST':
        if 'ino' not in request.files:
            app.logger.error("Non ino file attempted to be uploaded")
            flash('Not and INO file')
            return redirect(url_for('index'))
        file = request.files['ino']
        if file.filename == '':
            app.logger.error("No filename given")
            flash('No file given')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            app.logger.info("File " + filename + " accepted.  Moving through to build and upload")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process(filename)
            flash('Success!')
            return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
