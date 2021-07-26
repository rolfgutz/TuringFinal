from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.models.Empresa import Empresa
from app.controllers.login.login import requires_roles 
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re


@app.route('/cadastrarEmpresa')
# @login_required
def cadastrarEmpresa():
	return render_template('empresa/cadastroEmpresa.html')


@app.route('/salvar_empresa',methods=['POST'])
# @login_required
def salvar_empresa():
	razao_social = request.form.get('razao_social')
	text2 = re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",request.form.get('cnpj'))
	cnpj = int(text2)
	nome = request.form.get('nome')
	endereco = request.form.get('endereco')
	cidade = request.form.get('cidade')
	estado = request.form.get('estado')
	cep = request.form.get('cep')

	empresa = Empresa(razao_social,cnpj,nome,endereco,cidade,estado,cep)

	db.session.add(empresa)
	db.session.commit()

	empresas = Empresa.query.all()
	return render_template('empresa/listarEmpresa.html', empresas=empresas)
    
@app.route('/listarEmpresa')
# @login_required
# @requires_roles('Cliente')
def listarEmpresa():
	empresas = Empresa.query.all()
	return render_template('empresa/listarEmpresa.html',  empresas=empresas)


@app.route('/deletarEmpresa/<int:id>')
# @login_required
def deletarEmpresa(id=0):
	empresa = Empresa.query.filter_by(id_empresa=id).first()
	return render_template('empresa/deletarEmpresa.html', empresa=empresa)

    
@app.route('/saveDeletarEmpresa',methods=['POST'])
# @login_required
def saveDeletarEmpresa():
	id = int(request.form.get('id_empresa'))
	empresa = Empresa.query.filter_by(id_empresa=id).first()
	
	db.session.delete(empresa)
	db.session.commit()
	
	empresas = Empresa.query.all()
	return render_template('empresa/listarEmpresa.html',  empresas=empresas)


@app.route('/editarEmpresa/<int:id>')
# @login_required
def editarEmpresa(id=0):
	empresa =  Empresa.query.filter_by(id_empresa=id).first()
	return render_template('empresa/editarEmpresa.html', empresa=empresa)


@app.route('/saveEditarEmpresa',methods=['POST'])
# @login_required
def saveeditarEmpresa():
	id = int(request.form.get('id_empresa'))
	razao_social = request.form.get('razao_social')
	text2 = re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",request.form.get('cnpj'))
	cnpj = int(text2)
	nome = request.form.get('nome')
	endereco = request.form.get('endereco')
	cidade = request.form.get('cidade')
	estado = request.form.get('estado')
	cep = request.form.get('cep')

	empresa = Empresa.query.filter_by(id_empresa=id).first()

	empresa.razao_social =razao_social
	empresa.nome = nome
	empresa.cnpj = cnpj
	empresa.endereco = endereco
	empresa.cidade = cidade
	empresa.estado = estado
	empresa.cep = cep

	db.session.commit()

	empresas = Empresa.query.all()
	return render_template('empresa/listarEmpresa.html', empresas=empresas)

