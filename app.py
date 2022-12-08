from jinja2 import Environment, FileSystemLoader
import jmespath
import json
import os
import uuid
from flask import Flask, abort, flash, request, redirect, url_for, render_template, send_file
from lykdat import LykdatGlobalSearchFile,LykdatGlobalSearchUrl
from werkzeug.utils import secure_filename

# the "files" directory next to the app.py file
UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'files')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'q854ds'


@app.route('/', methods=['GET'])
def main_page():
    return _show_page()


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    #file = request.files['file']
    app.logger.info(request.files)
    upload_files = request.files.getlist('file')
    app.logger.info(upload_files)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if not upload_files:
        flash('No selected file')
        return redirect(request.url)
    for file in upload_files:
        original_filename = file.filename
        extension = original_filename.rsplit('.', 1)[1].lower()
        filename = str(uuid.uuid1()) + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
        files = _get_files()
        files[filename] = original_filename
        with open(file_list, 'w') as fh:
            json.dump(files, fh)

    flash('Upload succeeded')

    LykdatGlobalSearchFile('files' + '/' + filename)

    with open('files/'+"responseFile.json", "r") as d:
        responseFile = json.load(d)
        headings = ("Category", "Currency", "Gender", "Matching_Image","Name", "Price", "Url")
        datas = jmespath.search(
            "result_groups[*].similar_products[*].[category,currency,gender,matching_image,name,price,url]",
            responseFile['data'])

    fileLoader = FileSystemLoader("templates")
    env = Environment(loader=fileLoader)

    rendered = env.get_template("gallery.html").render(
        headings=headings, datas=datas)

    fileName = "index.html"

    with open(f"./templates/{fileName}", "w") as f:
        f.write(rendered)    


    return redirect(url_for('upload_file'))

@app.route('/download/<code>', methods=['GET'])
def download(code):
    files = _get_files()
    if code in files:
        path = os.path.join(UPLOAD_FOLDER, code)
        if os.path.exists(path):
            return send_file(path)
    abort(404)

@app.route('/vmd_timestamp')
def vmd_timestamp():
    return render_template('index.html')    

def _show_page():
    files = _get_files()
    return render_template('upload.html', files=files)


def _get_files():
    file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
    if os.path.exists(file_list):
        with open(file_list) as fh:
            return json.load(fh)
    return {}  

if __name__ == "__main__":

    app.run(debug=True)