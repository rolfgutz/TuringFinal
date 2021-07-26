from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user

class UsuarioModel(db.Model,UserMixin):
	__tablename__ = 'usuarioSistema'

	id = db.Column(db.Integer, primary_key=True)
	cpf = db.Column(db.Integer,unique=True, index = True)
	nome = db.Column(db.String(150), nullable = False)
	email = db.Column(db.String(150),nullable = False)
	password = db.Column(db.String(255),nullable = False)
	endereco = db.Column(db.String(255))
	cidade = db.Column(db.String(255))
	estado = db.Column(db.String(50))
	cep = db.Column(db.String(10))
	tipoUsuario = db.Column(db.String(50))
	id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id_empresa'),nullable = False)
	id_funcionario = db.relationship('Pedido', backref="usuarioSistema")
							
	def __init__(self, cpf,nome,email,password,endereco,cidade,estado,cep,tipoUsuario,id_empresa):
		self.cpf = cpf
		self.nome = nome
		self.email = email
		self.password = password
		self.endereco = endereco
		self.cidade = cidade
		self.estado = estado
		self.cep = cep
		self.tipoUsuario = tipoUsuario
		self.id_empresa = id_empresa

	def __repr__(self):
		return '<UsuarioModel %r>' % self.nome
