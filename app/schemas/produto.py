from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoBase(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=150
    )
    categoria: str = Field(
        min_length=1,
        max_length=100
    )
    preco: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    sku: str = Field(
        min_length=1,
        max_length=50
    )


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )
    categoria: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    preco: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    sku: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)