from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import utils
import openai
import os  # for path operations
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'secret_key'
model = "gpt-3.5-turbo-16k"
openai.api_key = os.environ.get('OPENAI_KEY')
openai.organization = os.environ.get('OPENAI_ORG')

UPLOAD_FOLDER = os.getcwd() + '/temp_uploads'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def process_file():

    stylized_output = None  # Initialized here
    filename_for_download = None  # Initialized here
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Save the file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filename = f"{filename.split('.')[0]}"

            # Now, pass the filepath to DocumentLoader
            loader = utils.DocumentLoader(filepath)
            document = loader.load_document()
            processing = utils.OpenAIInterface(model)
            overview = processing.generate_overview(document)
            responses = processing.generate_response(document)
            stylized_output = processing.stylize_output(overview, responses, filename)
            
            # Delete the file after processing
            os.remove(filepath)

            # Send the stylized_output as a downloadable file
            buffer = BytesIO()
            buffer.write(stylized_output.encode('utf-8'))
            buffer.seek(0)
            
            filename_for_download = filename + ".html"
            
            # Save the stylized_output in the session
            session['stylized_output'] = stylized_output
            session['filename_for_download'] = filename_for_download

    return render_template('index.html', content=stylized_output, filename=filename_for_download)

@app.route('/download/<filename>')
def download_file(filename):
    buffer = BytesIO()
    stylized_output = session['stylized_output']
    filename = session['filename_for_download']
    buffer.write(stylized_output.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype="text/html")


if __name__ == "__main__":
    app.run()
