from pydantic import BaseModel
from typing import List, Optional

class ProdutoSchema(BaseModel):
    id: Optional[int]
    nome: str
    descricao: str
    preco: float

    class Config:
        orm_mode = True
        from_attributes = True


class ListagemProdutosSchema(BaseModel):
    produtos: List[ProdutoSchema]

class ProdutoBuscaPorIDSchema(BaseModel):
    id: int

class ProdutoCriarSchema(BaseModel):
    nome: str
    descricao: str
    preco: float    
