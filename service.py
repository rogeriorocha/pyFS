from storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from model import ArquivoCategoria, ArquivoDado
from session import session

def upload(file):
    ad = ArquivoDado()
    session.add(ad)
    
    codArq = ad.cod_arq

    print(codArq)

    fs = FileStorage(codArq)
    filename = secure_filename(file.filename)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    os.makedirs(fs.path, exist_ok=True)
    file.save(fs.file)
    hashFileMD5 = HashUtils.getFileMD5(fs.file)
    print(fs.exists())
    
    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)   

    
    return codArq
