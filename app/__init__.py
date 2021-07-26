from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user


app = Flask(__name__, template_folder="templates")

app.config.from_object('config')
login_manager = LoginManager(app)


db = SQLAlchemy(app)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.controllers import default
<<<<<<< HEAD
=======
from app.controllers.login import login
from app.controllers.usuario import usuario_controller
from app.controllers.produto import produto_controller
from app.controllers.empresa import empresa_controller
from app.controllers.fornecedor import fornecedor_controller
from app.controllers.pedido import pedido_controller
from app.controllers.itensPedido import itensPedido
from app.controllers.inicio import inicio
>>>>>>> 8a8b6761542d3ee2cf0ddf5b8f2785f06e1c3cab
