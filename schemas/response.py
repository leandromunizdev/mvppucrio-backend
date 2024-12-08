from pydantic import BaseModel

class ValorSchema(BaseModel):
    valor: float

class TotalSchema(BaseModel):
    total: int
