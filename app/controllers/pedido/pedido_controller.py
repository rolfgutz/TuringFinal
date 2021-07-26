from flask_migrate import current
from sqlalchemy.orm import query
from app.models.Pedido import Pedido
from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.ProdutoModel import ProdutoModel
from app.models.ItensPedido import Itens_Pedido
from app.models.Empresa import Empresa
from app.models.UsuarioModel import UsuarioModel
from app.models.ItensPedido import Itens_Pedido
from datetime import date, datetime
from sqlalchemy import extract

from app.controllers.login.login import requires_roles 
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json 


@app.route('/selecionarProdutos')
@app.route('/selecionarProdutos/<int:page>')
# @login_required
def selecionarProdutos(page=1):
    produtos = produtosPagined(page)
    produtosPagina = ConvertePagina(produtos)
    return render_template('pedidos/selecionarProdutos.html', produtos=produtosPagina)     

@app.route('/pedido/addPedido/', methods=['POST'])
# @login_required
def addPedido():    
    pedido = Pedido(0,0,None,0,0,'',current_user.id_empresa,current_user.id) 
    produtosLista = request.form['lista']
    jsonresult = json.loads(produtosLista)
    
    db.session.add(pedido)
    db.session.commit()        

    valor_total = 0
    sobra = 0
    for p in jsonresult:
        produtoBanco = ProdutoModel.query.filter_by(idProduto = p['idProduto']).first()
        itens = Itens_Pedido(pedido.id_pedido,p['idProduto'],float(p['valorProduto']),float(p['quantity']))
        valor_total += itens.valorProduto()

        quilos = produtoBanco.kg 
        sobra = quilos - int(p['quantity'])
        produtoBanco.kg = sobra
        
        db.session.commit()

        db.session.add(itens)
        db.session.commit()

    pedido.valor =  valor_total
    
    db.session.commit()   

    itensPedido  = PedidoItensArray(pedido)
    return itensPedido 

@app.route('/listarPedidos/')
@app.route('/listarPedidos/<int:page>')
def listarPedidos(page):
    pedidos = PedidosPagined(page)
    return render_template('pedidos/listarPedidos.html', pedidoArray = pedidos)

@app.route('/detalhesPedido/<int:id>')
def detalhesPedido(id):
    pedido = Pedido.query.filter_by(id_pedido=id).first()
    itensPedido  = PedidoItensArray(pedido)
    return render_template('/pedidos/detalhesPedido.html',   itensPedido = itensPedido)

def produtosPagined (page=1):
    page = page
    produtos = ProdutoModel.query.filter(ProdutoModel.kg > 0).paginate(page,15,False)
    return produtos

@app.route('/gerenciarPedidos/')
@app.route('/gerenciarPedidos/<int:page>')
def gerenciarPedidos(page=1):  
    pedidos = db.session.query(Pedido,Empresa).filter(Pedido.id_empresa_funcionario == Empresa.id_empresa).filter(UsuarioModel.id_empresa == Empresa.id_empresa).paginate(page, 25, False)
    pedidos = ConverterPedidosAdm(pedidos)
    return render_template('pedidos/gerenciarpedidos.html',   pedidos = pedidos)

@app.route('/editarPedido/<int:id>')
def editarPedido(id):  
    pedidoId = Pedido.query.filter_by(id_pedido=id).first()
    pedido  = PedidoItensArray(pedidoId)
    return render_template('/pedidos/editarPedido.html', pedido = pedido)

@app.route('/saveEditarPedido',methods=['POST'])
def saveEditarPedido():
    idProduto = int(request.form.get('IdPedido'))
    notaFiscal = int(request.form.get('NotaFiscal'))
    prazoDePagamento = int(request.form.get('prazoPagamento'))
    status = int(request.form.get('status'))
    observacao = request.form.get('observacao')
    
    pedido = Pedido.query.filter_by(id_pedido = idProduto).first()
    
    pedido.notaFiscal = notaFiscal
    pedido.prazoPagamento = prazoDePagamento
    pedido.statusPagamento = status
    pedido.observacao = observacao

    db.session.commit()
    
    produtosVoltarEstoque = []
    if status == 2:    
        produtosDoPedido =db.session.query(Itens_Pedido).filter(Itens_Pedido.id_pedido == pedido.id_pedido).all()  
        for index in range(len(produtosDoPedido)):
            produtosDoPedido[index]
            produto = {'id_produto' : produtosDoPedido[index].id_produto,
                       'quantidade' : int(produtosDoPedido[index].kg)
                      }
            produtosVoltarEstoque.append(produto)
    
    for p in range (len(produtosVoltarEstoque)):
        produtoAdd = db.session.query(ProdutoModel).filter(ProdutoModel.idProduto == produtosVoltarEstoque[p]['id_produto']).first()
        produtoAdd.kg = produtoAdd.kg + produtosVoltarEstoque[p]['quantidade']
        db.session.commit()

    return redirect(url_for('gerenciarPedidos'))

@app.route('/gerenciarPedidos/consultaPedidos',methods=['POST'])   
@app.route('/gerenciarPedidos/consultaPedidos/<int:page>', methods=['POST'])
# @login_required
def consultaPedidos(page=1):
    consulta = '%'+request.form.get('consulta')+'%'
    campo = request.form.get('campo') 
    if campo == 'nomeEmpresa':
        pedidos = db.session.query(Pedido,Empresa).filter(Pedido.id_empresa_funcionario == Empresa.id_empresa).filter(UsuarioModel.id_empresa == Empresa.id_empresa).filter(Empresa.nome .like(consulta)).paginate(page, 25, False)
        pedidos = ConverterPedidosAdm(pedidos)
    if campo == 'numeroPedido':
        numeroPedido = int(consulta.replace('%',''))
        pedidos = db.session.query(Pedido,Empresa).filter(Pedido.id_empresa_funcionario == Empresa.id_empresa).filter(UsuarioModel.id_empresa == Empresa.id_empresa).filter(Pedido.id_pedido == numeroPedido).paginate(page, 25, False)
        pedidos = ConverterPedidosAdm(pedidos)

    return render_template('/pedidos/gerenciarpedidos.html',   pedidos = pedidos)

@app.route('/detalhesPedidoAdm/<int:id>')
def detalhesPedidoAdm(id):
    pedidoId = Pedido.query.filter_by(id_pedido=id).first()
    pedido  = PedidoItensArray(pedidoId)
    return render_template('/pedidos/detalhesPedidoAdm.html',   pedido = pedido)

@app.route('/graficoPedidos/')
def graficosPedido():
    mesJaneiro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==1).all()
    mesFevereiro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==2).all()
    mesMarco = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==3).all()
    mesAbril = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==4).all()
    mesMaio = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==5).all()
    mesJunho = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==6).all()
    mesJulho = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==7).all()
    mesAgosto = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==8).all()
    mesSetembro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==9).all()
    mesNovembro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==10).all()
    mesOutubro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==11).all()
    mesDezembro = db.session.query(Pedido).filter(extract('year', Pedido.dataPedido)== 2021).filter(extract('month',Pedido.dataPedido)==12).all()

    janeiroTotal = totalMes(mesJaneiro)
    fevereiroTotal = totalMes(mesFevereiro)
    marcoTotal = totalMes(mesMarco)
    abrilTotal = totalMes(mesAbril)
    maioTotal = totalMes(mesMaio)
    junhoTotal = totalMes(mesJunho)
    julhoTotal = totalMes(mesJulho)
    agostoTotal = totalMes(mesAgosto)
    setembroTotal = totalMes(mesSetembro)
    novembroTotal = totalMes(mesNovembro)
    outubroTotal = totalMes(mesOutubro)
    dezembroTotal = totalMes(mesDezembro)
  
    emAberto  = db.session.query(Pedido).filter(Pedido.statusPagamento == 0).all()
    emAberto = len(emAberto)
    pago  = db.session.query(Pedido).filter(Pedido.statusPagamento == 1).all()
    pago = len(pago)
    cancelado  = db.session.query(Pedido).filter(Pedido.statusPagamento == 2).all()
    cancelado = len(cancelado)

    return render_template('/pedidos/graficoPedidos.html', 
                            janeiro = janeiroTotal, fevereiro = fevereiroTotal,
                            marco = marcoTotal, abril = abrilTotal, maio = maioTotal,
                            junho = junhoTotal, julho = julhoTotal, agosto = agostoTotal,
                            setembro = setembroTotal, outubro =  outubroTotal,
                            novembro = novembroTotal, dezembro = dezembroTotal ,
                            aberto = emAberto, pago = pago, cancelado = cancelado )

   
def ConvertePagina(produtos):
    produtoResult = {'has_next': produtos.has_next,
                    'has_prev':produtos.has_prev,
                    'items': [],
                    'next_num' : produtos.next_num,
                    'page': produtos.page,
                    'pages':produtos.pages,
                    'per_page':produtos.per_page,
                    'prev_num': produtos.prev_num
                    }
    totalItens = len(produtos.items)
    for index in range(totalItens):
        produto = { 'idProduto' : produtos.items[index].idProduto,
                    'nome':produtos.items[index].nome,
                    'valorTela':ConverterMoeda(produtos.items[index].valor),
                    'valor':produtos.items[index].valor,
                    'kg':ConverterQuilos(produtos.items[index].kg),
                    'id_fornecedor':produtos.items[index].id_fornecedor
                   }

        produtoResult['items'].append(produto)
    
    return produtoResult

def Pedidosarray(pedido):
    pedidoResult = {'has_next': pedido.has_next,
                    'has_prev':pedido.has_prev,
                    'items': [],
                    'next_num' : pedido.next_num,
                    'page': pedido.page,
                    'pages':pedido.pages,
                    'per_page':pedido.per_page,
                    'prev_num': pedido.prev_num
                    }
    
    itens = len(pedido.items)
    for index in range(itens):
        empresa = Empresa.query.filter_by(id_empresa = pedido.items[index].id_empresa_funcionario).first()
        usuario = UsuarioModel.query.filter_by(id = pedido.items[index].id_funcionario).first()
        
        detalhesPedido =  { 'razaoSocial' :  empresa.razao_social,
                            'nomeUsuario' :usuario.nome,
                            'numeroPedido' : pedido.items[index].id_pedido,
                            'DatadoPedido' : ConvertData(pedido.items[index].dataPedido),
                            'ValorPedido' : ConverterMoeda(pedido.items[index].valor),
                            'StatusdePagamento' : StatusDePagamento(pedido.items[index].statusPagamento)
                        }
        
        pedidoResult['items'].append(detalhesPedido)
    
    return pedidoResult

def ConvertData(dtPedido):
    data = dtPedido
    dataFormatada = data.strftime('%d/%m/%Y')
    return dataFormatada

def PedidoItensArray(pedido):
    empresa = Empresa.query.filter_by(id_empresa = pedido.id_empresa_funcionario).first()
    itens = Itens_Pedido.query.filter_by(id_pedido = pedido.id_pedido).all()
    produtosDoPedido = []

    for x in itens:        
        produto  = ProdutoModel.query.filter_by(idProduto = x.id_produto).first()
        if x.id_produto == produto.idProduto:
            itemNome = produto.nome       
            produtoValor = x.valor
            quantidade = x.kg 
            valorProdutos = x.kg * x.valor
            p = {'nome' : itemNome,
                'produtoValor': ConverterMoeda(produtoValor) ,
                'quantidade': ConverterQuilos(quantidade),
                'valorProdutos': ConverterMoeda(valorProdutos)
                 }
            produtosDoPedido.append(p)
            
    detalhesPedido = { 'razaoSocial' :  empresa.razao_social,
                    'cnpj': empresa.cnpj,
                    'numeroPedido' : pedido.id_pedido,
                    'DatadoPedido' : ConvertData(pedido.dataPedido),
                    'NomeUsuario':pedido.usuarioSistema.nome,
                    'NotaFiscal': pedido.notaFiscal,
                    'ValorTotalPedido' : ConverterMoeda(pedido.valor),
                    'produtos' : produtosDoPedido,
                    'observacao' : pedido.observacao,
                    'prazoPagamento': ConverterPrazoPagamento(pedido.prazoPagamento),
                    'statusPagamento' :StatusDePagamento(pedido.statusPagamento)
                    }
            
    return detalhesPedido   
    
def PedidosPagined (page=1):
    page = page
    pedidoArray = []
    usuario =current_user.tipoUsuario
    if (usuario != "Administrador"):
        pedido = Pedido.query.filter(Pedido.id_funcionario == current_user.id_empresa).paginate(page , 15, False)
    else:
        pedido = Pedido.query.filter().paginate(page , 15, False)
    if (pedido.pages > 0): 
        pedidoArray = Pedidosarray(pedido)
    else:
        return pedido
    return pedidoArray

def StatusDePagamento(status):
    if status  == 0:
        return 'Em Aberto'
    elif status == 1:
        return 'Pago'
    else:
        return 'Cancelado'

def StatusDePagamentoInt(status):
    if status == "Em Aberto":
        return 0
    elif status == "Pago":
        return 1 
    else:
        return 2 
        
def ConverterMoeda(my_value):
    moeda = 'R$ '
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return moeda + c.replace('v','.')

def ConverterPrazoPagamento(my_value):
    if my_value  == None:
        return 0
    else:
        return my_value

def ConverterQuilos(my_value):
    a = '{:,.0f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

def totalMes(mes):
    mesTotal = 0
    for m in range(len(mes)):
        mesTotal += mes[m].valor
    if len(mes) > 0:
        mesTotal = mesTotal/len(mes)
    return mesTotal

def ConverterPedidosAdm(pedido):
    pedidoResult = {'has_next': pedido.has_next,
                    'has_prev':pedido.has_prev,
                    'items': [],
                    'next_num' : pedido.next_num,
                    'page': pedido.page,
                    'pages':pedido.pages,
                    'per_page':pedido.per_page,
                    'prev_num': pedido.prev_num
                    }
    
    itens = len(pedido.items)
    for index in range(itens):
        usuario = UsuarioModel.query.filter_by(id = pedido.items[index].Pedido.id_funcionario).first()
        
        detalhesPedido =  { 'empresa' :  pedido.items[index].Empresa.razao_social,
                            'nomeUsuario' :usuario.nome,
                            'numeroPedido' : pedido.items[index].Pedido.id_pedido,
                            'DatadoPedido' : ConvertData(pedido.items[index].Pedido.dataPedido),
                            'ValorPedido' : ConverterMoeda(pedido.items[index].Pedido.valor),
                            'StatusdePagamento' : StatusDePagamento(pedido.items[index].Pedido.statusPagamento)
                        }
        
        pedidoResult['items'].append(detalhesPedido)
    
    return pedidoResult

