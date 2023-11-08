from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
