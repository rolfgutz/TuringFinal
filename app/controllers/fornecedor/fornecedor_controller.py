from flask import Flask,render_template,redirect,request,url_for,flash
import flask_script
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.models.Fornecedor import Fornecedor
from app.controllers.login.login import requires_roles 
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re


@app.route('/cadastrarFornecedor')
# @login_required
def cadastrarFornecedor():
    return render_template('fornecedor/cadastroFornecedor.html')


@app.route('/salvarFornecedor',methods=['POST'])
# @login_required
def salvarFornecedor():
    cnpj_form = request.form.get('cnpj')
    cnpj = int(re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",cnpj_form))
    msg = validDoc(cnpj_form)
    
    if msg is not None:
        flash(message=msg, category="danger")        
        return render_template('fornecedor/cadastroFornecedor.html')
    
    razao_social = request.form.get('razao_social')
    nome = request.form.get('nome')
                        
    fornecedor = Fornecedor(cnpj,razao_social,nome)

    db.session.add(fornecedor)
    db.session.commit()

    fornecedores = Fornecedor.query.all()
    return render_template('fornecedor/listarFornecedor.html', fornecedores = fornecedores)
    
@app.route('/listarFornecedor')
# @login_required
# @requires_roles('Cliente')
def listarFornecedor():
	fornecedores = Fornecedor.query.all()
	return render_template('fornecedor/listarFornecedor.html', fornecedores = fornecedores)


@app.route('/deletarFornecedor/<int:id>')
# @login_required
def deletarFornecedor(id=0):
	fornecedor = Fornecedor.query.filter_by(id_fornecedor=id).first()
	return render_template('fornecedor/deletarFornecedor.html', fornecedor = fornecedor)

    
@app.route('/saveDeletarFornecedor',methods=['POST'])
# @login_required
def saveDeletarFornecedor():
    id = int(request.form.get('id_fornecedor'))
    fornecedor = Fornecedor.query.filter_by(id_fornecedor=id).first()
	
    db.session.delete(fornecedor)   
    db.session.commit()
	
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedor/listarFornecedor.html',  fornecedores = fornecedores)


@app.route('/editarFornecedor/<int:id>')
# @login_required
def editarFornecedor(id=0):
	fornecedor =  Fornecedor.query.filter_by(id_fornecedor=id).first()
	return render_template('fornecedor/editarFornecedor.html', fornecedor = fornecedor)


@app.route('/saveEditarFornecedor',methods=['POST'])
# @login_required
def saveEditarFornecedor():
    id = int(request.form.get('id_fornecedor'))
    cnpj_form = request.form.get('cnpj')
    msg = validDoc(cnpj_form)
    
    if msg is not None:
        flash(message=msg, category="danger")        
        fornecedor =  Fornecedor.query.filter_by(id_fornecedor=id).first()
        return render_template('fornecedor/editarFornecedor.html', fornecedor = fornecedor)

    cnpj = int(re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",cnpj_form))
    razao_social = request.form.get('razao_social')
    nome = request.form.get('nome')

           
    fornecedor =  Fornecedor.query.filter_by(id_fornecedor=id).first()

    fornecedor.cnpj = cnpj
    fornecedor.razao_social = razao_social
    fornecedor.nome = nome
	
    db.session.commit()

    fornecedores = Fornecedor.query.all()
    return render_template('fornecedor/listarFornecedor.html',  fornecedores = fornecedores)


def validDoc (cnpj):
    tamanho = len(cnpj)
    if  tamanho <= 11 or tamanho > 18:
        return 'CNPJ preenchimento inválido!!!'
    else:
        return None
