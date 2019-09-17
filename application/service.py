from application.storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from application.models import ArquivoCategoria, ArquivoDado, db


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

    #fileSize = os.path.getsize(file)
    #ad.tam_arq = fileSize
    ad.nom_orig = filename;
    ad.cod_algtm_hash = hashFileMD5;

    db.session.flush();
    db.session.commit();

    print(fs.exists())
    
    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)   

    
    return codArq
