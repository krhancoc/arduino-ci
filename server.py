import os
import time

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

UPLOAD_FOLDER='files'
ALLOWED_EXTENSIONS = set(['ino'])

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "WHATEVERYOUWANTBRO"

class INOWatcher(PatternMatchingEventHandler):
    def process(self, event):
        print event.src_path, event.event_type

    def on_created(self, event):
        self.process(event)

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
        # check if the post request has the file part
        if 'ino' not in request.files:
            flash(u'No File Part', 'error')
            return render_template('index.html',message="ERROR")
        file = request.files['ino']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash(u'No Filename', 'error')
            return render_template('index.html', message="ERROR")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(u'Confirmed Upload')
            return render_template('index.html', message="SUCCESS")

if __name__ == "__main__":
    
    observer = Observer()
    observer.schedule(INOWatcher(), path='files')
    observer.start()
    app.run()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


