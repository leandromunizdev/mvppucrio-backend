from database import db

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # Campos de frete (opcionais)
    frete_cep = db.Column(db.String(9), nullable=True)
    frete_logradouro = db.Column(db.String, nullable=True)
    frete_numero = db.Column(db.Integer, nullable=True)
    frete_complemento = db.Column(db.String, nullable=True)
    frete_bairro = db.Column(db.String, nullable=True)
    frete_cidade = db.Column(db.String, nullable=True)
    frete_uf = db.Column(db.String(2), nullable=True)
        
    produto = db.relationship("Produto", backref="vendas")
