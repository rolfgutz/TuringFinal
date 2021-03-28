from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from app.models.TipoUserModel import TipoUserEnum

class UsuarioSistema(db.Model,UserMixin):
    __tablename__ = "userSistema"

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(150),nullable =False)
    email =db.Column(db.String(100),nullable=False, unique=True , index=True)
    password = db.Column(db.String(255),nullable=False)
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(255))
    estado = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    tipouser  = db.Column(db.String(50))

    
    
    def __init__(self, nome, email, endereco,cidade,estado,cep,tipouser):
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.tipouser = tipouser                 

    def __repr__(self):
        return '<UsuarioSistema %r>' % self.nome


