from database import db

class VendaItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    produto = db.relationship("Produto", backref="itens_venda")