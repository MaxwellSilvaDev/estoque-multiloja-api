from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MovimentacaoBase(BaseModel):
    produto_id: int = Field(gt=0)
    loja_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)


class MovimentacaoCreate(MovimentacaoBase):
    pass


class MovimentacaoResponse(MovimentacaoBase):
    id: int
    tipo: Literal["entrada", "saida", "ajuste"]
    data: datetime

    model_config = ConfigDict(from_attributes=True)