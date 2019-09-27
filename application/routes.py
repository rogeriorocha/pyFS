from flask import Flask, request, make_response, flash, redirect, jsonify, send_from_directory, Response
from flask import current_app as app
from datetime import datetime
import math
import argparse
import json
import urllib.request
import os
from application import service, storage
from flask_restplus import Api, Resource, fields, inputs, reqparse
from werkzeug.datastructures import FileStorage
from application.models import SimNaoEnum

import socket

api = Api(app = app, 
                version = "0.1b", 
                title = "FileServer", 
                description = "File Server Resource") 

def valid_date(s):
    try:
        return datetime.strptime(s, '%d-%m-%YT%H:%M:%S')
    except :
        msg = "Not a valid date: '{0}'.".format(s)
        raise ValueError('Not a valid date format.')
        #raise argparse.ArgumentTypeError(msg)

upload_parser = api.parser()
upload_parser.add_argument('arquivo', location='files', type=FileStorage, required=True)
upload_parser.add_argument('categoria', location='path', type=int, required=False, default=service.FILE_CATEGORIA_DEFAULT) 

#upload_parser.add_argument('dataExpurgo', location='path', type=lambda x: datetime.strptime(x,'%d-%m-%YT%H:%M:%S'), required=False, default=None) 
upload_parser.add_argument('dataExpurgo', location='path', type=valid_date, required=False, default=None) 
upload_parser.add_argument('descricao', location='path', type='string', required=False)
upload_parser.add_argument('codigoUsuario', location='path', type='string', required=False, default="118104")


update_parser = api.parser()
update_parser.add_argument('dataExpurgo', location='path', type=valid_date, required=False, default=None) 

waterkark_parser = api.parser()
waterkark_parser.add_argument('id', location='path', type=int, required=True) 
waterkark_parser.add_argument('texto', location='path', type='string', required=True)
waterkark_parser.add_argument('filename', location='path', type='string', required=False, default=service.WATERMARK_DEFAULT_FILENAME)


name_space = api.namespace('FS', description='Endpoints')

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

arquivo = api.model('Arquivo', {
    'id': fields.Integer(required=True, description='id do arquivo'),
    'nome': fields.String(required=True, description='nome do arquivo'),

})


"""
payload = name_space.model('Payload', {
    'categoria': fields.Integer(required=True),
    'dataExpurgo': fields.Date(required=True)
})
"""

@name_space.route("/upload/"
    ,"/upload/<int:categoria>/"
    ,doc={"description": "Faz upload de um arquivo", },)    
class upload(Resource):
    @name_space.expect(upload_parser, validate=True)
    @api.doc(responses={201: 'Upload com sucesso', 400: 'Erro de validacao'})
    def post(self, categoria=None):
        """Incluir arquivo"""
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('categoria', type=str)
        #parser.add_argument('dataExpurgo', type=lambda x: datetime.strptime(x,'%d-%m-%YT%H:%M:%S'), help="erro na data")
        parser.add_argument('dataExpurgo', type=valid_date,help="Erro na formatacao da data '%d-%m-%YT%H:%M:%S'!")
         
        try:  # Will raise an error if date can't be parsed.
            args = parser.parse_args()  # type "dict"
            #return jsonify(args)
        except ValueError as e:
            return  str(e), 500
        
        if categoria == None:
            categoria = service.FILE_CATEGORIA_DEFAULT

        descricao = request.args.get("descricao")
        dataExpurgo = request.args.get("dataExpurgo")
        dtExpurgo = None
        if dataExpurgo:
            dtExpurgo = datetime.strptime(dataExpurgo, '%d-%m-%YT%H:%M:%S')

        FILE_ATTACHED = 'arquivo'
        if FILE_ATTACHED not in request.files:
            flash('No file part')
            content = {}
            raise InvalidUsage('No "'+FILE_ATTACHED + '" part', status_code=500)
            
        file = request.files[FILE_ATTACHED]

        if file.filename == '':
            flash('No arquivo selected for uploading')
            return redirect(request.url)            
        try:
            codArq = service.upload(file, categoria, descricao, dtExpurgo)
        except Exception as e:
            #InvalidUsage(str(e), status_code=)
            return str(e), 400

        flash('File successfully uploaded')
        resp = {"codArq": codArq}
        response = make_response(json.dumps(resp))
        response.content_type = "application/json"    

        return response    

@name_space.route("/union/<arquivos>", doc={"description": "Unir dois ou mais arquivos PDFs", },)
class union(Resource):
    #@app.route('/union/<arquivos>', methods=['POST'])
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'arquivos': 'lista de dois ou mais ids de arquivos PDFs separadas por virgula.' }) 
    def post(self,arquivos=None):
        """Unir arquivos PDF"""
        if arquivos == None:
            raise InvalidUsage('"arquivos" not present', status_code=500)
        arquivos = arquivos.replace(" ", "")
        lstArq = arquivos.split(",")
        
        if len(lstArq) <= 1:
            raise InvalidUsage('"arquivos" deve conter mais de um codigo de arquivo', status_code=400)

        codArq = service.union(lstArq) 
        data = {'codArq'  : codArq}
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@name_space.route("/download/<int:id>", doc={"description": "Faz download de um arquivo", },)
class download(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Id associado ao FileServer'})
    #@app.route('/download/<int:id>', methods=['GET'])
    def get(self, id):
        """Baixar arquivo"""
        sf = storage.FileStorage(id)
        ad = service.getArquivoDado(id)
        filename = ad.nom_orig
        return send_from_directory(sf.path, sf.filename, as_attachment=True, attachment_filename=filename)

@name_space.route("/data/<int:id>", doc={"description": "Retorna o nome original do arquivo", },)
class data(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Id associado ao FileServer'})
    
    def get(self,id):
        """Retornar dados do arquivo"""
        ad = service.getArquivoDado(id)
        
        resp = {"id": id, "nome": ad.nom_orig, "descricao": ad.dsc_arq, "hash":ad.cod_algtm_hash
        #, "categoria":ad.categoria.dsc_categ
        , "codigoCategoria":ad.cod_categ
        , "dataExpurgo" : None if ad.dat_expur == None else ad.dat_expur.strftime('%d-%m-%YT%H:%M:%S')
        , "dataInclusao": None if ad.dat_incl == None else ad.dat_incl.strftime('%d-%m-%YT%H:%M:%S')
        , "ativo":ad.flg_ati == SimNaoEnum.S
        }
        response = make_response(json.dumps(resp))
        response.content_type = "application/json"    

        return response

@name_space.route("/watermark/<int:id>", doc={"description": "Cria marca d'agua em um arquivo PDF", "deprecated": False,},)
@name_space.expect(waterkark_parser)
class watermark(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, )
	#		 params={'id': 'Id de um arquivo PDF associado ao FileServer', 'texto':'texto do watermark'})
    def post(self, id):
        """Criar novo arquivo PDF com marca d'agua"""
        if id == None:
            raise InvalidUsage('"id" not present', status_code=500)

        texto = request.args.get("texto") 
        if not texto:
            raise InvalidUsage('"texto" not present', status_code=500)

        filename = request.args.get("filename") 
        if not filename:
            filename = service.WATERMARK_DEFAULT_FILENAME

        codArq = service.watermark(id, texto, filename) 
        data = {'codArq'  : codArq}
        js = json.dumps(data)

        resp = Response(js, status=200, mimetype='application/json')
        return resp        
        pass

@name_space.route("/delete/<int:id>", doc={"description": "Deleta e arquivo do FS"},)
class delete(Resource):
    @api.doc(responses={ 204: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={'id': 'Id associado ao FileServer'})
    #@app.route('/download/<int:id>', methods=['GET'])
    def delete(self, id):
        """Excluir arquivo """
        service.delete(id)
        resp = Response("{}", status=204, mimetype='application/json')
        return resp

@name_space.route("/expurga", doc={"description": "expurga arquivos expirados"},)
class expurgar(Resource):
    def post(self):
        qtde = service.expurgar()
        data = {'qtde'  : qtde}
        js = json.dumps(data)

        resp = Response(js, status=200, mimetype='application/json')
        return resp

@name_space.route("/set-expurgo/<int:id>", doc={"description": "Set data de expurgo", },)
class update(Resource):
    @name_space.expect(update_parser, validate=True)
    @api.doc(responses={201: 'Upload com sucesso', 500: 'Erro de validacao'})
    def put(self, id):
        """ seta data expurgo """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('dataExpurgo', type=valid_date,help="Erro na formatacao da data '%d-%m-%YT%H:%M:%S'!")
         
        try:  
            args = parser.parse_args()  # type "dict"
        except ValueError as e:
            return  str(e), 500

        dataExpurgo = request.args.get("dataExpurgo") 
        if dataExpurgo:
            dataExpurgo = datetime.strptime(dataExpurgo, '%d-%m-%YT%H:%M:%S')
        service.setExpurgo(id, dataExpurgo)
        
        return 200


@name_space.route("/cpu-inc/")
class test(Resource):
    @api.doc(responses={201: 'Upload com sucesso', 500: 'Erro de validacao'})
    def get(self):
        x = 0.0001
        for i in range(100000000):
            x = x + math.sqrt(i)
        return "OK, i'm "+socket.gethostname() +"!" , 200

