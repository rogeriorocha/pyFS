import os
import sys



from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, schema, types


from sqlalchemy.ext.declarative import declarative_base

metadata = schema.MetaData()


Base = declarative_base()


class ArquivoCategoria(Base):
    __tablename__ = "arquivo_categoria"

    cod_categ = Column(Integer, primary_key=True )
    dsc_categ = Column(String(100))

class ArquivoDado(Base):
    __tablename__ = "arquivo_dados"

    cod_arq = Column(Integer, primary_key=True,  autoincrement=True )
    end_arq = Column(String(100))
    nom_orig = Column(String(100))
    cod_categ = Column(Integer, ForeignKey('arquivo_categoria.cod_categ'))
    categoria = relationship(ArquivoCategoria)
    dat_incl = Column(DateTime, default=func.now())
    cod_algtm_hash = Column(String(50))
    tam_arq = Column(Integer)
    dsc_arq = Column(String(255))

    def __repr__(self):
         return "<ArquivoDado(id='%d', end_arq='%s', nom_orig='%s')>" % (self.cod_arq, self.end_arq, self.nom_orig)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///fs.db')
 
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
#Base.metadata.create_all(engine)