from pydantic import BaseModel

class MensagemSchema(BaseModel):
    message: str
