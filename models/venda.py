from database import db
from datetime import datetime

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String, nullable=False, unique=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Campos de frete (opcionais)
    frete_cep = db.Column(db.String(9), nullable=True)
    frete_logradouro = db.Column(db.String, nullable=True)
    frete_numero = db.Column(db.Integer, nullable=True)
    frete_complemento = db.Column(db.String, nullable=True)
    frete_bairro = db.Column(db.String, nullable=True)
    frete_cidade = db.Column(db.String, nullable=True)
    frete_uf = db.Column(db.String(2), nullable=True)

    # Relacionamento com os itens da venda
    itens = db.relationship("VendaItem", backref="venda", cascade="all, delete-orphan")