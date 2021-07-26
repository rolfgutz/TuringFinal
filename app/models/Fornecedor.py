from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date

class Fornecedor(db.Model,UserMixin):
    __tablename__ = 'fornecedor'

    id_fornecedor = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.Integer,nullable = False ,unique=True, index=True)
    razao_social = db.Column(db.String(200))
    nome = db.Column(db.String(150),nullable=False)
    produto = db.relationship('ProdutoModel', backref="fornecedor")

    def __init__(self,cnpj,razao_social,nome):
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome = nome

    def __repr__(self):
        return '<Fornecedor %r>' % self.nome