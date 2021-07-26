from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date


class Pedido(db.Model,UserMixin):
    __tablename__ = 'pedido'

    id_pedido = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    notaFiscal = db.Column(db.String(50))
    dataPedido = db.Column(db.Date, default = date.today())
    prazoPagamento = db.Column(db.Integer)
    statusPagamento = db.Column(db.Integer)
    observacao = db.Column(db.String(500))
    id_empresa_funcionario = db.Column(db.Integer,nullable = False)
    id_funcionario  = db.Column(db.Integer, db.ForeignKey('usuarioSistema.id'), nullable=False)
    id_pedido_item = db.relationship('Itens_Pedido', backref="pedido")


    # dataPedidoF = datetime.strptime(dataPedido, "%Y-%m-%d").date()
    
    
    def __init__(self,valor,notaFiscal,dataPedido,prazoPagamento,statusPagamento,observacao,id_empresa_funcionario,id_funcionario):
        self.valor = valor
        self.notaFiscal = notaFiscal
        self.dataPedido = dataPedido
        self.prazoPagamento = prazoPagamento
        self.statusPagamento = statusPagamento
        self.observacao = observacao
        self.id_empresa_funcionario = id_empresa_funcionario
        self.id_funcionario = id_funcionario

    
    def __repr__(self):
        return '<Pedido %r>' % self.valor