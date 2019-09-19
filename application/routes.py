from flask import Flask, request, make_response, flash, redirect, jsonify, send_from_directory, Response
from flask import current_app as app


import json
import urllib.request
import os
from application import service, storage

from flask_restplus import Api, Resource, fields


from werkzeug.datastructures import FileStorage



api = Api(app = app, 
                version = "1.0", 
                title = "FileServer Resource", 
                description = "File Server Resource") 


upload_parser = api.parser()
upload_parser.add_argument('arquivo', location='files',
                           type=FileStorage, required=True) 
#upload_parser.add_argument('categoria', type=int, required=false, default=service.FILE_CATEGORIA_DEFAULT)                           


name_space = api.namespace('FS', description='File Server operations')

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


@name_space.route("/union/<arquivos>", doc={"description": "Unir dois ou mais arquivos PDFs", },)
class Union(Resource):
    #@app.route('/union/<arquivos>', methods=['POST'])
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'arquivos': 'lista de dois ou mais ids de arquivos PDFs separadas por virgula.' }) 
    def post(self,arquivos=None):
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

@name_space.route("/upload/<int:categoria>", doc={"description": "Faz upload de um arquivo", },)
@name_space.expect(upload_parser)
class UploadResource(Resource):
    #@app.route('/upload/<int:categoria>', methods=['POST'])
    #@app.route('/upload/', methods=['POST'])
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'categoria': 'categoria do arquivo' })
    def post(self, categoria=service.FILE_CATEGORIA_DEFAULT):
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


@name_space.route("/download/<int:id>", doc={"description": "Faz download de um arquivo", },)
class FSDownloadResource(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Id associado ao FileServer'})
    #@app.route('/download/<int:id>', methods=['GET'])
    def get(self, id):
        sf = storage.FileStorage(id)
        filename = service.getFileName(id)
        return send_from_directory(sf.path, sf.filename, as_attachment=True, attachment_filename=filename)



@name_space.route("/filename/<int:id>", doc={"description": "Retorna o filename de um arquivo", },)
class FSFilenameResource(Resource):
    #name_space.route("/filename/<int:id>")
    #app.route('/filename/<int:id>', methods=['GET'])
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Id associado ao FileServer'})
    def get(self,id):
        filename = service.getFileName(id)
        resp = {"codArq": id, "nome": filename}
        response = make_response(json.dumps(resp))
        response.content_type = "application/json"    

        return response


@name_space.route("/watermark/<int:id>", doc={"description": "Cria marca d'agua em um arquivo PDF", "deprecated": True,},)
class FSWatermarkResource(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'id': 'Id de um arquivo PDF associado ao FileServer', 'texto':'texto do watermark'})
    #@app.route('/download/<int:id>', methods=['GET'])
    def post(self, id, texto):
        pass


@name_space.route("/delete/<int:id>", doc={"description": "Deleta e arquivo do FS", "deprecated": True,},)
class DeleteRS(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'id': 'Id associado ao FileServer'})
    #@app.route('/download/<int:id>', methods=['GET'])
    def delete(self, id):
        pass
