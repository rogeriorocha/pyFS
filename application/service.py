from application.storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from application.models import ArquivoCategoria, ArquivoDado, db


def getFileName(id):
    ad = db.session.query(ArquivoDado).get(id)

    return ad.nom_orig

    


def upload(file):
    ad = ArquivoDado()
    db.session.add(ad)
    db.session.commit()
    
    codArq = ad.cod_arq
    

    fs = FileStorage(codArq)
    filename = secure_filename(file.filename)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    os.makedirs(fs.path, exist_ok=True)
    file.save(fs.file)
    
    


    hashFileMD5 = HashUtils.getFileMD5(fs.file)

    fileSize = _file_size(fs.file)
    print(fileSize)

    ad.tam_arq = fileSize
    ad.nom_orig = filename;
    ad.cod_algtm_hash = hashFileMD5;

    db.session.flush();
    db.session.commit();

    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)   

    
    return codArq

def _file_size(fname):
        statinfo = os.stat(fname)
        return statinfo.st_size