from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.controllers.login.login import requires_roles 
from app.models.Empresa import Empresa
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re


@app.route('/cadastrarUsuario')
# @login_required
def cadastrarUsuario():
	empresas = Empresa.query.all()
	return render_template('usuario/cadastroUsuario.html', empresas= empresas)


@app.route('/salvar_cadastro',methods=['POST'])
# @login_required
def salvar_cadastro():
	# cpf_form = re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",request.form.get('cpf'))
	cpf = request.form.get('cpf')	
	nome = request.form.get('nome')
	email = request.form.get('email')
	password = generate_password_hash(request.form["password"])
	endereco = request.form.get('endereco')
	cidade = request.form.get('cidade')
	estado = request.form.get('estado')
	cep = request.form.get('cep')
	tipoUsuario = request.form.get('tipoUsuario')
	id_empresa = request.form['id_empresa']

	usuario = UsuarioModel(cpf,nome,email,password,endereco,cidade,estado,cep,tipoUsuario,id_empresa)
	
	msg = validDoc(usuario)
	if msg is not None:
		flash(message=msg, category="error")        
		empresas = Empresa.query.all()
		return render_template('usuario/cadastroUsuario.html', empresas= empresas)
	
	usuario.cpf = int(re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",cpf))
	db.session.add(usuario)
	db.session.commit()
	
	usuarios = UsuarioModel.query.all()
	return render_template('usuario/listarUsuarios.html', usuarios=usuarios)
    
@app.route('/listarUsuarios')
# @login_required
# @requires_roles('Administrador')
def listarUsuarios():
	usuarios = UsuarioModel.query.all()
	return render_template('usuario/listarUsuarios.html', usuarios=usuarios)


@app.route('/deletarUsuario/<int:id>')
# @login_required
def deletarUsuario(id=0):
	usuario = UsuarioModel.query.filter_by(id=id).first()

	return render_template('usuario/deletarUsuario.html', usuario=usuario)

    
@app.route('/savedeletarUsuario',methods=['POST'])
# @login_required
def savedeletarUsuario():
	id = int(request.form.get('id'))

	usuario = UsuarioModel.query.filter_by(id=id).first()
	
	db.session.delete(usuario)
	db.session.commit()
	
	usuarios = UsuarioModel.query.all()
	return render_template('usuario/listarUsuarios.html', usuarios=usuarios)

@app.route('/editarUsuario/<int:id>')
# @login_required
def editarUsuario(id=0):
	usuario = UsuarioModel.query.filter_by(id=id).first()
	return render_template('usuario/editarUsuario.html', usuario=usuario)


@app.route('/saveEditarUsuario',methods=['POST'])
# @login_required
def saveeditarUsuario():
	id = int(request.form.get('id'))
	nome_form = request.form.get('nome')
	email_form = request.form.get('email')
	endereco_form = request.form.get('endereco')
	cidade_form = request.form.get('cidade')
	estado_form = request.form.get('estado')
	cep_form = request.form.get('cep')
	tipoUsuario_form = request.form.get('tipoUsuario')

	usuarios = UsuarioModel.query.filter_by(id=id).first()

	usuarios.nome = nome_form
	usuarios.email = email_form
	usuarios.endereco = endereco_form
	usuarios.cidade = cidade_form
	usuarios.estado = estado_form
	usuarios.cep = cep_form
	usuarios.tipoUsuario = tipoUsuario_form

	db.session.commit()

	usuarios = UsuarioModel.query.all()
	return render_template('usuario/listarUsuarios.html', usuarios=usuarios)


def validDoc (usuario):
	if usuario.nome == '' or usuario.email == '' or usuario.endereco == '' or usuario.cidade == '' or  usuario.estado == '' or usuario.cep == '':
		return'Preenchimento de todos os campos necessário'
	else:
		return None
