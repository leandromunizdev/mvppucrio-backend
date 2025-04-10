from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class VendaItemSchema(BaseModel):
    produto_id: int
    quantidade: int
    preco: float

    model_config = {
        "orm_mode": True,
        "from_attributes": True,
    }

class FreteSchema(BaseModel):
    cep: str
    logradouro: str
    numero: int
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str

    model_config = {
        "orm_mode": True,
        "from_attributes": True,
    }

class PagamentoSchema(BaseModel):
    forma: str
    valor: float

    model_config = {
        "orm_mode": True,
        "from_attributes": True,
    }

class VendaSchema(BaseModel):
    id: Optional[int] = None
    codigo: str
    itens: Optional[List[VendaItemSchema]] = Field(default_factory=list)
    data: Optional[datetime] = None
    frete: Optional[FreteSchema] = None
    pagamentos: Optional[List[PagamentoSchema]] = None

    model_config = {
        "orm_mode": True,
        "from_attributes": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }

    @field_validator("itens", mode="before")
    def convert_items(cls, v):
        if isinstance(v, list):
            return [item if isinstance(item, dict) else VendaItemSchema.from_orm(item) for item in v]
        return v
