from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MovimentacaoBase(BaseModel):
    produto_id: int
    loja_id: int
    tipo: str
    quantidade: int


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoResponse(MovimentacaoBase):
    id: int
    data: datetime

    model_config = ConfigDict(from_attributes=True)