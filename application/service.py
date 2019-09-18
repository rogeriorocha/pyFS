from application.storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from application.models import ArquivoCategoria, ArquivoDado, db
from application.pdfutils import union as pdfUtils_union
from shutil import copyfile


FILE_CATEGORIA_DEFAULT = 1
FILE_CATEGORIA_UNION = 2
FILE_CATEGORIA_WATERMARK = 2

def getFileName(id):
    ad = db.session.query(ArquivoDado).get(id)

    return ad.nom_orig

def upload(file, categoria):
    ad = ArquivoDado()
    ad.cod_categ = categoria
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
    

    ad.tam_arq = fileSize
    ad.nom_orig = filename;
    ad.cod_algtm_hash = hashFileMD5;

    db.session.commit();
    db.session.flush();

    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)   
    
    return codArq

def _file_size(fname):
    statinfo = os.stat(fname)
    return statinfo.st_size



def union(*args):
    files = ()


    for codArq in args:
        sf = FileStorage(codArq)
        files = files +(str(sf.file),)

    filename = pdfUtils_union(files)

    ad = ArquivoDado()
    ad.cod_categ = 1 
    #FILE_CATEGORIA_UNION
    db.session.add(ad)
    db.session.commit()
    
    codArq = ad.cod_arq

    fs = FileStorage(codArq)
    os.makedirs(fs.path, exist_ok=True)

    copyfile(filename, fs.file)
    print(filename)
    print(fs.file)

    #os.remove(filename)

    hashFileMD5 = HashUtils.getFileMD5(fs.file)
    fileSize = _file_size(fs.file)

    ad.tam_arq = fileSize
    ad.nom_orig = "union.pdf"
    ad.cod_algtm_hash = hashFileMD5;

    db.session.commit();
    db.session.flush();
    

    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)      

    return codArq