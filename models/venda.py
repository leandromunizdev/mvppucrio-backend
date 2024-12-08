from database import db

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    produto = db.relationship("Produto", backref="vendas")
