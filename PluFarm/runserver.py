from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return jsonify(error="PDF files are required."), 400
    
    pdf1 = request.files['pdf1']
    pdf2 = request.files['pdf2']
    
    # Here you can process the PDF files as needed
    # ...

    return jsonify(success="PDFs uploaded successfully.")

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.', 'ai-plugin.json', mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

@app.route('/compare_pdfs', methods=['POST'])
def compare_pdfs():
    if 'pdf1' not in request.files or 'pdf2' not in request.files:
        return jsonify(error="compare_pdfs")
    file1 = request.files['pdf1']
    file2 = request.files['pdf2']        
    if file1.filename == '' or file2.filename == '':
        return jsonify(error="Nenhum arquivo selecionado")
    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file1.save(filepath1)
        file2.save(filepath2)
        return jsonify(success="compare_pdfs")
    return jsonify(success="compare_pdfs")

if __name__ == '__main__':
    app.run(debug=True)
