from flask import Flask, request, make_response, flash, redirect, jsonify, send_from_directory
from flask import current_app as app

import json
import urllib.request
import os
from application import service, storage



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



@app.route('/union/<string:arquivos>', methods=['POST'])
def union(arquivos):
    codArq = service.union(1,3) 

    print(codArq)

    resp = {"codArq": codArq}
    response = make_response(json.dumps(resp))
    response.content_type = "application/json"    
    return response
    