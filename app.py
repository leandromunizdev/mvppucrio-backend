from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from database import db, init_db
from models.produto import Produto
from models.estoque import Estoque
from models.venda import Venda
from schemas.mensagem import MensagemSchema
from schemas.produto import ListagemProdutosSchema, ProdutoBuscaPorIDSchema, ProdutoSchema
from schemas.estoque import EstoqueBuscaPorIDSchema, EstoqueSchema, ListagemEstoquesSchema
from schemas.venda import VendaSchema
from schemas.error import ErrorSchema
from sqlalchemy.exc import SQLAlchemyError
from schemas.response import ValorSchema, TotalSchema

# Informações da API
info = Info(title="Loja de Roupas API", version="1.0.0", description="API para gerenciar produtos, estoque e vendas.")
app = OpenAPI(__name__, info=info)
CORS(app)

# Configurações do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Tags para categorização dos endpoints
produto_tag = Tag(name="Produto", description="Endpoints para gerenciar produtos.")
estoque_tag = Tag(name="Estoque", description="Endpoints para gerenciar o estoque.")
venda_tag = Tag(name="Venda", description="Endpoints para gerenciar vendas.")

# Endpoints
@app.post("/produtos", tags=[produto_tag], responses={"201": ProdutoSchema})
def criar_produto(body: ProdutoSchema):
    """Cria um novo produto."""
    produto = Produto(**body.dict())
    db.session.add(produto)
    db.session.commit()

    # Reutilizando apresenta_produtos para retornar o produto criado
    return {"produto": apresenta_produtos([produto])[0]}, 201


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """
    Faz a busca por todos os Produtos cadastrados.

    Retorna uma representação da listagem de produtos com o saldo em estoque.
    """
    session = db.session

    # Busca todos os produtos
    produtos = session.query(Produto).all()

    if not produtos:
        return {"produtos": []}, 200

    produtos_com_saldo = []
    for produto in produtos:
        # Calcula o total de entradas no estoque
        total_estoque = session.query(
            db.func.sum(Estoque.quantidade)
        ).filter(Estoque.produto_id == produto.id).scalar() or 0

        # Calcula o total de saídas (vendas)
        total_vendas = session.query(
            db.func.sum(Venda.quantidade)
        ).filter(Venda.produto_id == produto.id).scalar() or 0

        # Saldo = total_estoque - total_vendas
        saldo = total_estoque - total_vendas

        # Adiciona o produto com saldo à lista
        produtos_com_saldo.append({
            "id": produto.id,
            "nome": produto.nome,
            "descricao": produto.descricao,
            "preco": produto.preco,
            "saldo": saldo
        })

    return {"produtos": produtos_com_saldo}, 200

@app.put('/produto', tags=[produto_tag],
         responses={"200": ProdutoSchema, "404": ErrorSchema})
def atualizar_produto(body: ProdutoSchema):
    """
    Atualiza os dados de um produto existente.

    Args:
        body (ProdutoSchema): Dados para atualizar o produto, incluindo o ID.

    Returns:
        ProdutoSchema: Produto atualizado.
        ErrorSchema: Mensagem de erro caso o produto não seja encontrado.
    """
    session = db.session

    # Extraindo o ID do produto do body
    produto_id = body.id

    # Buscando o produto
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        return {"message": f"Produto com ID {produto_id} não encontrado."}, 404

    # Atualizando os dados
    for key, value in body.dict().items():
        if key != "id":  # Ignorar o ID para evitar conflitos
            setattr(produto, key, value)

    session.commit()

    return apresenta_produtos([produto])[0], 200

@app.delete('/produto', tags=[produto_tag],
             responses={"200": MensagemSchema, "404": ErrorSchema})
def deletar_produto(query: ProdutoBuscaPorIDSchema):
    """
    Remove um produto pelo ID.

    Args:
        id (int): ID do produto a ser deletado.

    Returns:
        dict: Mensagem de sucesso ou erro.
    """
    session = db.session

    # Buscando o produto
    produto = session.query(Produto).filter(Produto.id == query.id).first()

    if not produto:
        return {"message": f"Produto com ID {query.id} não encontrado."}, 404

    # Removendo o produto
    session.delete(produto)
    session.commit()

    return MensagemSchema(message=f"Produto com ID {query.id} deletado com sucesso.").dict(), 200

def apresenta_produtos(produtos):
    """Converte os objetos Produto em uma lista de dicionários.

    Funciona tanto para uma lista quanto para um único produto.
    """
    return [ProdutoSchema.from_orm(produto).dict() for produto in produtos]


@app.post("/estoques", tags=[estoque_tag], responses={"201": EstoqueSchema})
def criar_estoque(body: EstoqueSchema):
    """Adiciona uma nova entrada de estoque."""
    estoque = Estoque(**body.dict())
    db.session.add(estoque)
    db.session.commit()
    return EstoqueSchema.from_orm(estoque).dict(), 201

@app.get('/estoques', tags=[estoque_tag],
         responses={"200": ListagemEstoquesSchema, "404": ErrorSchema})
def get_estoques():
    """Faz a busca por todos os Estoques cadastrados.

    Retorna uma representação da listagem de estoques.
    """
    session = db.session
    estoques = session.query(Estoque).all()

    if not estoques:
        return {"estoques": []}, 200

    return {"estoques": apresenta_estoques(estoques)}, 200

def apresenta_estoques(estoques):
    """Converte os objetos Estoque em uma lista de dicionários.

    Funciona tanto para uma lista quanto para um único estoque.
    """
    return [EstoqueSchema.from_orm(estoque).dict() for estoque in estoques]

@app.put('/estoque', tags=[estoque_tag],
         responses={"200": EstoqueSchema, "404": ErrorSchema})
def atualizar_estoque(body: EstoqueSchema):
    """
    Atualiza os dados de um estoque existente.

    Args:
        body (EstoqueSchema): Dados para atualizar o estoque, incluindo o ID.

    Returns:
        EstoqueSchema: Estoque atualizado.
        ErrorSchema: Mensagem de erro caso o estoque não seja encontrado.
    """
    session = db.session

    # Extraindo o ID do produto do body
    estoque_id = body.id

    # Buscando o produto
    estoque = session.query(Estoque).filter(Estoque.id == estoque_id).first()

    if not estoque:
        return {"message": f"Estoque com ID {estoque_id} não encontrado."}, 404

    # Atualizando os dados
    for key, value in body.dict().items():
        if key != "id":  # Ignorar o ID para evitar conflitos
            setattr(estoque, key, value)

    session.commit()

    return apresenta_estoques([estoque])[0], 200

@app.delete('/estoque', tags=[estoque_tag],
             responses={"200": MensagemSchema, "404": ErrorSchema})
def deletar_estoque(query: EstoqueBuscaPorIDSchema):
    """
    Remove um estoque pelo ID.

    Args:
        id (int): ID do estoque a ser deletado.

    Returns:
        dict: Mensagem de sucesso ou erro.
    """
    session = db.session

    # Buscando o estoque
    estoque = session.query(Estoque).filter(Estoque.id == query.id).first()

    if not estoque:
        return {"message": f"Estoque com ID {query.id} não encontrado."}, 404

    # Removendo o estoque
    session.delete(estoque)
    session.commit()

    return MensagemSchema(message=f"Estoque com ID {query.id} deletado com sucesso.").dict(), 200

@app.post("/vendas", tags=[venda_tag], responses={"201": VendaSchema, "400": ErrorSchema})
def criar_venda(body: VendaSchema):
    """
    Registra uma nova venda para cada item fornecido.

    Args:
        body (VendaSchema): Dados da venda, incluindo itens.

    Returns:
        dict: Mensagem de sucesso com as vendas registradas ou erro.
    """

        # Exibindo o conteúdo do body no console
    print("Body recebido:")
    print(body.json(indent=2))  # Converte para JSON com indentação para legibilidade

    session = db.session

    vendas_registradas = []
    try:
        data_criacao = datetime.utcnow()
        for item in body.itens:
            # Criar uma venda para cada item
            venda = Venda(
                codigo=body.codigo,
                data=data_criacao,
                produto_id= item.produto_id,
                quantidade= item.quantidade,
                preco= item.preco 
            )
            session.add(venda)
            vendas_registradas.append(venda)

        # Salvar todos os registros no banco de dados
        session.commit()

        # Retornar todas as vendas registradas
        return jsonify([VendaSchema.from_orm(venda).dict() for venda in vendas_registradas]), 201

    except SQLAlchemyError as e:
        # Fazer rollback em caso de erro
        session.rollback()
        return {"message": f"Erro ao registrar as vendas: {str(e)}"}, 400

# Totalizadores para a tela de início    
@app.get('/vendas/total', tags=[venda_tag], responses={"200": ValorSchema})
def get_valor_total_vendas():
    """
    Retorna o valor total das vendas com base no preço registrado em cada venda.
    """
    session = db.session
    # Calcula o valor total em vendas usando o preço na tabela Venda
    total_vendas = session.query(
        db.func.sum(Venda.quantidade * Venda.preco)
    ).scalar() or 0.0

    return ValorSchema(valor=total_vendas).dict(), 200


@app.get('/produtos/total', tags=[produto_tag], responses={"200": TotalSchema})
def get_total_produtos():
    """
    Retorna o total de produtos cadastrados.
    """
    session = db.session
    # Conta o total de produtos cadastrados
    total_produtos = session.query(db.func.count(Produto.id)).scalar() or 0

    return TotalSchema(total=total_produtos).dict(), 200


@app.get('/estoque/total', tags=[estoque_tag], responses={"200": TotalSchema})
def get_total_estoque():
    """
    Retorna o total geral de itens em estoque considerando as vendas.
    """
    session = db.session
    # Soma o total de itens no estoque
    total_estoque = session.query(
        db.func.sum(Estoque.quantidade)
    ).scalar() or 0

    # Soma o total de itens vendidos
    total_vendido = session.query(
        db.func.sum(Venda.quantidade)
    ).scalar() or 0

    # Calcula o estoque disponível
    estoque_disponivel = total_estoque - total_vendido

    return TotalSchema(total=estoque_disponivel).dict(), 200   

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
