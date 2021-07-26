from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date


class Itens_Pedido(db.Model,UserMixin):
    __tablename__ = 'itens_pedido'

    id_itens = db.Column(db.Integer, primary_key=True)
    id_pedido =  db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.idProduto'),nullable=False)
    valor = db.Column(db.Float)
    kg = db.Column(db.Float)
    
       
    def __init__(self,id_pedido,id_produto,valor,kg):
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.valor = valor
        self.kg = kg 

    def valorProduto (self):
        return self.valor * self.kg


    def __repr__(self):
        return '<Empresa %r>' % self.nome