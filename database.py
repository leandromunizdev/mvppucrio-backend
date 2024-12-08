from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from models.produto import Produto
    from models.estoque import Estoque
    from models.venda import Venda
    db.create_all()
