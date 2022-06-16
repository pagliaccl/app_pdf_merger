from werkzeug.wrappers import Request, Response
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = ['pdf']
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['MERGED_FOLDER'] = 'merged'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def merge_pdf(pdfs, path):
    merger = PdfMerger()
    pdfs = [os.path.join(app.config['UPLOAD_FOLDER'], pdf) for pdf in pdfs]
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(path)
    merger.close()
    

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if not request.files:
            return Response("{'message':'No file'}", status=400)
        print(request.files)

        filenames = []
        files = []
        for i in range(len(request.files)):
            file = request.files.get(f'part{i+1}')
            files.append(file)
            filenames.append(file.filename)
        
        if not files:
            return Response("{'message':'file empty'}", status=400)

        for filename in filenames:
            if not allowed_file(filename):
                return Response(f"{{'message':'file {filename} not supported'}}", status=400)
        
        filenames =  [secure_filename(filename) for filename in filenames]
        print(filenames)
        for file, filename in zip(files, filenames):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        merge_pdf(filenames, os.path.join(app.config['MERGED_FOLDER'], 'result.pdf'))
        return send_from_directory(app.config['MERGED_FOLDER'], 'result.pdf')

    return Response("{'message':'No file'}", status=400)


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app.run(debug=True, host='0.0.0.0', port=9000)    