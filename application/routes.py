from flask import Flask, request, make_response, flash, redirect, jsonify
from flask import current_app as app

import json
import urllib.request
import os
from application import service

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

