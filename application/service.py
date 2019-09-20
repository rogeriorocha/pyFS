from application.storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from application.models import ArquivoCategoria, ArquivoDado, db, SimNaoEnum
from application.pdfutils import union as pdfUtils_union
from shutil import copyfile

from sqlalchemy import text
from datetime import datetime

FILE_CATEGORIA_DEFAULT = 1
FILE_CATEGORIA_UNION = 2
FILE_CATEGORIA_WATERMARK = 2

def getFileName(id):
    ad = db.session.query(ArquivoDado).get(id)

    return ad.nom_orig

def delete(id):
    fs = FileStorage(id)
    if os.path.exists(fs.file):
        os.remove(fs.file)

    if os.path.exists(fs.fileHash):
        os.remove(fs.fileHash)

    ad = db.session.query(ArquivoDado).get(id)
    ad.flg_ati = SimNaoEnum.N
    db.session.commit();
    db.session.flush();    

def insertNext(categoria):
    connection = db.engine.connect()
    trans = connection.begin()
    try:

        #now = datetime.now()
        #now.strftime("%d/%m/%Y %H:%M:%S")

        res =connection.execute('INSERT INTO arquivo_dados (flg_ati, dat_incl, cod_categ)  VALUES (\'S\', GETDATE(),'+str(categoria)+') select next =SCOPE_IDENTITY()')
        #res =connection.execute('INSERT INTO arquivo_dados (flg_ati, dat_incl, cod_categ)  VALUES (\'S\', GETDATE(),'+str(categoria)+') select next =SCOPE_IDENTITY()')
        """
        res =connection.execute('INSERT INTO arquivo_dados (flg_ati, dat_incl, cod_categ)  VALUES (\'S\', :dat_incl, :cod_categ) select next =SCOPE_IDENTITY()'
        , {'dat_incl':datetime.now(), 'cod_categ': categoria}
        )
        """
        row = res.fetchone()
        next = row['next']
        trans.commit()
        return next
    except:
        trans.rollback()
        raise


def upload(file, categoria):
    """ problema no SQL Server com OUTPUT qndo trem trigger na tabela    
    ad = ArquivoDado()
    ad.cod_categ = categoria
    db.session.add(ad)
    db.session.commit()
    codArq = ad.cod_arq
    """

    ad = db.session.query(ArquivoDado).get(insertNext(categoria))
    codArq = ad.cod_arq
    
    fs = FileStorage(codArq)
    filename = secure_filename(file.filename)
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    os.makedirs(fs.path, exist_ok=True)
    file.save(fs.file)

    hashFileMD5 = HashUtils.getFileMD5(fs.file)

    fileSize = _file_size(fs.file)
    #ad.cod_categ = categoria
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

def union(listArq):
    files = ()

    strCodArq = "union="
    for codArq in listArq:
        strCodArq = strCodArq + codArq+","
        sf = FileStorage(codArq)
        files = files + (str(sf.file),)

    strCodArq = strCodArq[:-1]

    filename = pdfUtils_union(files)

    
    """
    ad = ArquivoDado()
    ad.cod_categ = FILE_CATEGORIA_UNION
    db.session.add(ad)
    db.session.commit()
    codArq = ad.cod_arq
    """
    
    ad = db.session.query(ArquivoDado).get(insertNext(FILE_CATEGORIA_UNION))
    codArq = ad.cod_arq    
    

    fs = FileStorage(codArq)
    os.makedirs(fs.path, exist_ok=True)

    copyfile(filename, fs.file)


    hashFileMD5 = HashUtils.getFileMD5(fs.file)
    fileSize = _file_size(fs.file)

    ad.tam_arq = fileSize
    ad.nom_orig = "union.pdf"
    ad.cod_algtm_hash = hashFileMD5;
    ad.dsc_arq = strCodArq

    db.session.commit();
    db.session.flush();

    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)      

    return codArq