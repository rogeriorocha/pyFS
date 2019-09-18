from . import db

#import sqlalchemy as db

#from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
#from sqlalchemy import create_engine, schema, types
#from sqlalchemy.ext.declarative import declarative_base
#import os
#import sys

#metadata = schema.MetaData()


#Base = declarative_base()


 
class ArquivoCategoria(db.Model):
    __tablename__ = "arquivo_categoria"

    cod_categ = db.Column(db.Integer, primary_key=True )
    dsc_categ = db.Column(db.String(100))

class ArquivoDado(db.Model):
    __tablename__ = "arquivo_dados"

    cod_arq = db.Column(db.Integer, primary_key=True,  autoincrement=True )
    end_arq = db.Column(db.String(100))
    nom_orig = db.Column(db.String(100))
    cod_categ = db.Column(db.Integer, db.ForeignKey('arquivo_categoria.cod_categ'))
    categoria = relationship(ArquivoCategoria)
    dat_incl = db.Column(db.DateTime, default=db.func.now())
    cod_algtm_hash = db.Column(db.String(50))
    tam_arq = db.Column(db.Integer)
    dsc_arq = db.Column(db.String(255))

    def __repr__(self):
         return "<ArquivoDado(id='%d', end_arq='%s', nom_orig='%s')>" % (self.cod_arq, self.end_arq, self.nom_orig)

#from sqlalchemy import create_engine
#engine = create_engine('sqlite:///fs.db')
 
#from sqlalchemy.orm import sessionmaker
#session = sessionmaker()
#session.configure(bind=engine)
#Base.metadata.create_all(engine)