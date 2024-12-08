from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class VendaItemSchema(BaseModel):
    produto_id: int
    quantidade: int
    preco: float  # Preço do produto na venda

class VendaSchema(BaseModel):
    id: Optional[int]
    codigo: str
    itens: Optional[List[VendaItemSchema]]  # Lista de produtos na venda
    data: Optional[datetime]

    class Config:
        orm_mode = True
