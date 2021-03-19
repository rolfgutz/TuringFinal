
from flask import render_template, request
from app import app, db
from app.models.tables import Pessoa
from templates.login import login

@app.route('/')
@app.route('/login')
def login():
    return render_template('listagem.html', pessoas=pessoas, ordem='id')