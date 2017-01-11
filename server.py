import os
import subprocess

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER='files'
ALLOWED_EXTENSIONS = set(['ino'])

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "WHATEVERYOUWANTBRO"

def process(filename):
    print filename
    subprocess.call("bin/integration.sh " + filename, shell=True)

# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/submit', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'ino' not in request.files:
            return render_template('index.html',message="ERROR")
        file = request.files['ino']
        if file.filename == '':
            return render_template('index.html', message="ERROR")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process(filename)
            return render_template('index.html', message="SUCCESS")

if __name__ == "__main__":
    app.run()    
   


