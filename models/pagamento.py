from database import db

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_venda = db.Column(db.String, nullable=False)  # Utiliza o mesmo código da venda
    forma = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
