from flask import Flask, request, make_response, flash, redirect, jsonify, send_from_directory, Response
from flask import current_app as app

import json
import urllib.request
import os
from application import service, storage

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

@app.route('/upload/<int:categoria>', methods=['POST'])
@app.route('/upload/', methods=['POST'])

def upload_file(categoria=service.FILE_CATEGORIA_DEFAULT):
    FILE_ATTACHED = 'arquivo'
    #if request.method == 'POST':
    if FILE_ATTACHED not in request.files:
        flash('No file part')
        content = {}
        raise InvalidUsage('No "'+FILE_ATTACHED + '" part', status_code=500)
        
    file = request.files[FILE_ATTACHED]

    if file.filename == '':
        flash('No arquivo selected for uploading')
        return redirect(request.url)            
    
    codArq = service.upload(file, categoria)
    

    flash('File successfully uploaded')
    resp = {"codArq": codArq}
    response = make_response(json.dumps(resp))
    response.content_type = "application/json"    

    return response


@app.route('/download/<int:id>', methods=['GET'])
def download(id):
    sf = storage.FileStorage(id)
    filename = service.getFileName(id)
    return send_from_directory(sf.path, sf.filename, as_attachment=True, attachment_filename=filename)

@app.route('/filename/<int:id>', methods=['GET'])
def filename(id):
    filename = service.getFileName(id)
    resp = {"codArq": id, "nome": filename}
    response = make_response(json.dumps(resp))
    response.content_type = "application/json"    

    return response

#if __name__ == "__main__":
#    app.run(debug=True, use_reloader=True)



@app.route('/union/<arquivos>', methods=['POST'])
def union(arquivos=None):
    if arquivos == None:
        raise InvalidUsage('"arquivos" not present', status_code=500)
    lstArq = arquivos.split(",")
    
    if len(lstArq) <= 1:
        raise InvalidUsage('"arquivos" deve conter mais de um codigo de arquivo', status_code=500)


    codArq = service.union(lstArq) 
    
    print(codArq)
    data = {
        'codArq'  : codArq
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp