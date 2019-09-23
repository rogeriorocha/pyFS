from application.storage import FileStorage, HashUtils
from werkzeug.utils import secure_filename
import os


from application.models import ArquivoCategoria, ArquivoDado, db, SimNaoEnum
from application.pdfutils import union as pdfUtils_union, watermark as pdfUtils_watermark
from shutil import copyfile

from sqlalchemy import text
from datetime import datetime

FILE_CATEGORIA_DEFAULT = 1
FILE_CATEGORIA_UNION = 26
FILE_CATEGORIA_WATERMARK = 27

WATERMARK_DEFAULT_FILENAME = "watermark.pdf"
UNION_DEFAULT_FILENAME = "union.pdf"

def getArquivoDado(id):
    return db.session.query(ArquivoDado).get(id)

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
    

def __insertNext(categoria):
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


def upload(file, categoria, descricao, dataExpurgo):
    """ problema no SQL Server com OUTPUT qndo trem trigger na tabela    
    ad = ArquivoDado()
    ad.cod_categ = categoria
    db.session.add(ad)
    db.session.commit()
    codArq = ad.cod_arq
    """
    if dataExpurgo:
        if dataExpurgo < datetime.now():
            raise Exception('Data de Expurgo menor que data atual')

    ad = db.session.query(ArquivoDado).get(__insertNext(categoria))
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
    ad.cod_algtm_hash = hashFileMD5
    ad.dsc_arq = descricao
    if dataExpurgo:
       ad.dat_expur = dataExpurgo

    db.session.commit();
    db.session.flush();

    with open(fs.fileHash, 'w') as fileMd5:
        fileMd5.write(hashFileMD5)   
    
    return codArq

def watermark(id, texto, filenameDefault):
    sf = FileStorage(id)
    
    filename=pdfUtils_watermark(str(sf.file), texto)
    strCodArq="id="+str(id)+", texto="+texto

    ad = db.session.query(ArquivoDado).get(__insertNext(FILE_CATEGORIA_WATERMARK))
    codArq = ad.cod_arq    
    

    fs = FileStorage(codArq)
    os.makedirs(fs.path, exist_ok=True)

    copyfile(filename, fs.file)


    hashFileMD5 = HashUtils.getFileMD5(fs.file)
    fileSize = _file_size(fs.file)

    ad.tam_arq = fileSize
    ad.nom_orig = filenameDefault
    ad.cod_algtm_hash = hashFileMD5
    ad.dsc_arq = strCodArq

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
    
    ad = db.session.query(ArquivoDado).get(__insertNext(FILE_CATEGORIA_UNION))
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

def listaExpurgo():
    lst = []
    with db.engine.connect() as con:
        sql = """
            select top 1000 cod_arq
            from bdseg.dbo.arquivo_dados
            where (dat_expur is not null) 
            and (dat_expur < getdate())
            and flg_ati = 'S'
            order by dat_expur"""
        rs = con.execute(sql)
        
        for row in rs:
            lst.append(row["cod_arq"])
    return lst

def expurgar():
    lst = listaExpurgo()
    qtde = 0
    for codArq in lst:
        delete(codArq)
        qtde+=1
    return qtde    

