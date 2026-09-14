from pydantic import BaseModel, ConfigDict, Field


class EstoqueBase(BaseModel):
    produto_id: int = Field(gt=0)
    loja_id: int = Field(gt=0)
    quantidade: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0)


class EstoqueMinimoUpdate(BaseModel):
    estoque_minimo: int = Field(ge=0)


class EstoqueResponse(EstoqueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)