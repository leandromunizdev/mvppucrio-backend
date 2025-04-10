from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class EstoqueSchema(BaseModel):
    id: Optional[int] = None
    produto_id: int
    quantidade: int
    data_entrada: datetime
    numero_nota_fiscal: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class ListagemEstoquesSchema(BaseModel):
    estoques: List[EstoqueSchema]   

class EstoqueBuscaPorIDSchema(BaseModel):
    id: int     


