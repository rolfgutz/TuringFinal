from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date

class ProdutoModel(db.Model,UserMixin):
    __tablename__ = 'produto'

    idProduto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150),nullable=False)
    valor = db.Column(db.Float)
    kg = db.Column(db.Float)
    id_fornecedor = db.Column(db.Integer, db.ForeignKey('fornecedor.id_fornecedor'),nullable=False)
    produto = db.relationship('Itens_Pedido', backref="produto")
    


    def __init__(self,nome,valor,kg,id_fornecedor):     
        self.nome = nome
        self.valor = valor
        self.kg = kg
        self.id_fornecedor = id_fornecedor

    
    def __repr__(self):
        return '<ProdutoModel %r>' % self.nome
