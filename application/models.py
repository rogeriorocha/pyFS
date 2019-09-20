from . import db

from sqlalchemy.orm import relationship, backref 
from sqlalchemy import Enum

import enum

class SimNaoEnum(enum.Enum):
    S = "S"
    N = "N"

class ArquivoCategoria(db.Model):
    __tablename__ = "arquivo_categoria"

    cod_categ = db.Column(db.Integer, primary_key=True )
    dsc_categ = db.Column(db.String(100))

    def __repr__(self):
        return "<ArquivoCategoria (cod_categ='%d', dsc_categ='%s')>" % (self.cod_categ, self.dsc_categ)

class ArquivoDado(db.Model):
    __tablename__ = "arquivo_dados"
    flg_ati = db.Column(Enum(SimNaoEnum),  default= SimNaoEnum.S)
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
         return "<ArquivoDado (cod_arq='%d', end_arq='%s', nom_orig='%s')>" % (self.cod_arq, self.end_arq, self.nom_orig)

  