from operator import contains
from flask import Flask,render_template,redirect,request,url_for,flash
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError 
from app import app, db, login_manager
from app.models.ProdutoModel import ProdutoModel
from app.models.Fornecedor import Fornecedor
from app.controllers.login.login import requires_roles
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import locale



@app.route('/cadastrarProduto')
# @requires_roles('Administrador')
# @login_required
def cadastrarProduto():
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/cadastroProduto.html',fornecedores = fornecedores)

@app.route('/salvar_produto',methods=['POST'])
# @login_required
def salvar_produto():
    nome_form = request.form.get('nome')
    valor_form = request.form.get('valor')
    kg_form = request.form.get('kg')
    id_fornecedor_form = int(request.form.get('id_fornecedor'))
    
    produtoJson = {'nome':nome_form, 'valor':valor_form, 'kg':kg_form, 'id_fornecedor':id_fornecedor_form  }
    msg = CheckFormulario(produtoJson)
    
    if msg is not None:
        flash(message=msg, category='danger')
        fornecedores = Fornecedor.query.all()
        return render_template('produtos/cadastroProduto.html',fornecedores = fornecedores)
    
    produto = ProdutoModel(nome_form,valor_form,kg_form,id_fornecedor_form)

    produto.valor = float(produto.valor)
    produto.kg = float(produto.kg)

    db.session.add(produto)
    db.session.commit()

    fornecedores = Fornecedor.query.all()
    return redirect(url_for('listarProdutos'))
    

def CheckFormulario(produto):
    if produto['nome'] == '' or produto['valor'] == '' or produto['kg'] == '' or produto['id_fornecedor'] == '':
        return'Preenchimento de todos os campos necessário'    
    else:
	    return None
    
    
# @app.route('/listarProdutos/<int:page>',methods=['POST'],defaults={'page':1})
@app.route('/listarProdutos')
@app.route('/listarProdutos/<int:page>')
# @login_required
def listarProdutos(page=1):
    produtos = produtosPagined(page)
    return render_template('produtos/listarProdutos.html', produtos=produtos)


@app.route('/deletarProduto/<int:id>')
# @login_required
def deletarProduto(id=0):
    produto = ProdutoModel.query.filter_by(idProduto=id).first()

    fornecedores = Fornecedor.query.all()
    return render_template('produtos/deletarProduto.html', produto=produto, fornecedores = fornecedores)


@app.route('/saveDeleteProduto',methods=['POST'])
# @login_required
def saveDeleteProduto():
    id = int(request.form.get('idProduto'))
    produto = ProdutoModel.query.filter_by(idProduto=id).first()
    
    try:
        db.session.delete(produto)
        db.session.commit()
        msg = 'Produto deletado com sucesso'
        flash(message=msg , category='sucess')	  
        produtosArray = produtosPagined()
        return render_template('produtos/listarProdutos.html', produtos = produtosArray)

    except SQLAlchemyError as e:
        if '(sqlite3.IntegrityError) NOT NULL constraint failed: itens_pedido.id_produto' == e.args[0]: 
            db.session.rollback()
            msg = 'Não é possivel deletar esse produto, o mesmo possui registros de vendas. Zere a quantidade disponível para indisponibilizar a venda'
            flash(message=msg , category='error')	  
            produtosArray = produtosPagined()
            return render_template('produtos/listarProdutos.html', produtos = produtosArray)


@app.route('/editarProduto/<int:id>')
# @login_required
def editarProduto(id=0):
    produto = ProdutoModel.query.filter_by(idProduto=id).first()
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/editarProduto.html', produto=produto, fornecedores = fornecedores)

@app.route('/saveEditarProduto',methods=['POST'])
# @login_required
def saveEditarProduto():
    id = int(request.form.get('idProduto'))
    nome = request.form.get('nome')
    valor = float(request.form.get('valor'))
    kg = float(request.form.get('kg'))
    id_fornecedor = request.form.get('id_fornecedor')

    produto = ProdutoModel.query.filter_by(idProduto=id).first()
  
    produto.nome = nome
    produto.valor = valor
    produto.kg = kg
    produto.id_fornecedor = id_fornecedor

    db.session.commit()

    produtosArray = produtosPagined()
    return render_template('produtos/listarProdutos.html', produtos = produtosArray)


def produtosPagined (page=1):
    page = page
    produtosArray = []
    produtos = ProdutoModel.query.paginate(page , 15, False)
    if (produtos.pages > 0): 
        produtosArray = ProdutosArray(produtos)
    else:
        return produtos
    return produtosArray

    
def ProdutosArray (produtos):
    produtosResult = {'has_next': produtos.has_next,
                    'has_prev':produtos.has_prev,
                    'items': [],
                    'next_num' : produtos.next_num,
                    'page': produtos.page,
                    'pages':produtos.pages,
                    'per_page':produtos.per_page,
                    'prev_num': produtos.prev_num
                    }
    itens = len(produtos.items)
    for x in range(itens):
        produtoJson = {'idProduto': produtos.items[x].idProduto,
                        'nome': produtos.items[x].nome,
                        'valor': ConverterMoeda(produtos.items[x].valor),
                        'kg': ConverterQuilos(produtos.items[x].kg) 
                        }
        produtosResult['items'].append(produtoJson)
    
    return produtosResult

def ConverterMoeda(my_value):
    moeda = 'R$ '
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return moeda + c.replace('v','.')

    
def ConverterQuilos(my_value):
    a = '{:,.0f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')