from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class EstoqueSchema(BaseModel):
    id: Optional[int]
    produto_id: int
    quantidade: int
    data_entrada: datetime
    numero_nota_fiscal: Optional[str]

    class Config:
        orm_mode = True

class ListagemEstoquesSchema(BaseModel):
    produtos: List[EstoqueSchema]   

class EstoqueBuscaPorIDSchema(BaseModel):
    id: int     


