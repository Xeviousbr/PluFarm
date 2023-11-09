from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import chardet
from openai import OpenAI

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_api_key():
    with open('chaveapi.txt', 'r') as file:
        return file.read().strip()

openai.api_key = load_api_key()

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

def read_text_file(file_path):
    with open(file_path, 'rb') as file:  # note 'rb' for reading as binary
        raw_data = file.read()
    encoding = chardet.detect(raw_data)['encoding']
    return raw_data.decode(encoding)

@app.route('/analyze_document', methods=['POST'])
def analyze_document():
    document_content = """
     Agência Nacional de Vigilância Sanitária
     www.anvisa.gov.br
     Consulta Pública n° 1.206, de 2 de outubro de 2023
     D.O.U de 4/10/2023
     A Diretoria Colegiada da Agência Nacional de Vigilância Sanitária, no uso das 
     atribuições que lhe confere o art. 15, III e IV, aliado ao art. 7º, III e IV da Lei nº 9.782, de 26 de 
     janeiro de 1999, e ao art. 187, III, § 1º do Regimento Interno aprovado pela Resolução de 
     Diretoria Colegiada – RDC nº 585, de 10 de dezembro de 2021, resolve submeter à consulta 
     pública, para comentários e sugestões do público em geral, proposta de ato normativo, 
     conforme deliberado em reunião realizada em 27 de setembro de 2023, e eu, Diretor-Presidente 
     substituto, determino a sua publicação.
     ...
     Relacionados”.
     """
    prompt = f"{document_content}\n\nQuais vantagens e desvantagens deste documento para empresas que têm produtos biológicos?"
    client = OpenAI(
        api_key=openai.api_key,
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return jsonify(success=chat_completion['choices'][0]['message']['content'])
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
