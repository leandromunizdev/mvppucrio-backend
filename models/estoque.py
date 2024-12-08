from database import db
from datetime import datetime

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    numero_nota_fiscal = db.Column(db.String(50), nullable=False)    

    produto = db.relationship("Produto", backref="estoque")
