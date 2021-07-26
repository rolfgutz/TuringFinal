from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date

class Empresa(db.Model,UserMixin):
    __tablename__ = 'empresa'

    id_empresa = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(200))
    cnpj = db.Column(db.Integer,nullable = False ,unique=True, index=True)
    nome = db.Column(db.String(150),nullable=False)
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    usuario = db.relationship('UsuarioModel', backref="usuario")


    def __init__(self,razao_social,cnpj,nome,endereco,cidade,estado,cep):
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep 


    def __repr__(self):
        return '<Empresa %r>' % self.nome