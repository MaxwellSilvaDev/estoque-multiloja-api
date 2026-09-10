from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    preco: Decimal
    sku: str


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: str | None = None
    categoria: str | None = None
    preco: Decimal | None = None
    sku: str | None = None


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)