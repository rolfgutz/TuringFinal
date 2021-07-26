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


@app.route('/inicio')
# @login_required
def inicio():
    return render_template('inicio/inicio.html')
