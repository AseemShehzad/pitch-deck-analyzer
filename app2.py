import gradio as gr
import utils
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = 'gpt-3.5-turbo-16k'

def process(file):
    # check if the file is allowed
    if file is None or not allowed_file(file.name):
        return "Invalid file format. Please upload a PDF."
    
    # save to temporary folder
    filepath = file.name

    try:
        loader = utils.DocumentLoader(filepath)
        document = loader.load_document()
        processing = utils.OpenAIInterface(model)
        overview = processing.generate_overview(document)
        responses = processing.generate_response(document)
        stylized_output = processing.stylize_output(overview, responses, 'abc')
    except Exception as e:
        return f"Error processing file: {str(e)}"

    # Saving the stylized_output to a file
    filename = os.path.basename(filepath)
    filename = os.path.splitext(filename)[0]
    filename = filename + ".html"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'w') as f:
        f.write(stylized_output)

    return filepath

gr.Interface(fn=process, inputs="file", outputs="file", css="footer {visibility: hidden}").launch(debug=True, show_api=False)