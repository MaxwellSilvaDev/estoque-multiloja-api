from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LojaBase(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=150
    )
    endereco: str = Field(
        min_length=1,
        max_length=255
    )
    tipo: Literal["matriz", "filial"]


class LojaCreate(LojaBase):
    pass


class LojaUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )
    endereco: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )
    tipo: Literal["matriz", "filial"] | None = None


class LojaResponse(LojaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)