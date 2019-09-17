from flask import Flask, request, make_response, flash, redirect, jsonify

import json
import urllib.request
import os
import service

app = Flask("fs")




#UPLOAD_FOLDER='c:/temp/stored'

app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv    

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/all", methods=['GET'])
def lista_de_noticias():
    cat = request.args.get("categoria")
    qtd = request.args.get("quantidade")
    pessoas = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               ]
    response = make_response(json.dumps(pessoas))
    response.content_type = "application/json"    
    
    return response

@app.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            content = {}
            raise InvalidUsage('No file part', status_code=500)
            
        file = request.files['file']
        

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)            
        
        codArq = service.upload(file)
             
        

        flash('File successfully uploaded')
        pessoas = {"codArq": codArq}
        response = make_response(json.dumps(pessoas))
        response.content_type = "application/json"    
    
        return response

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)


