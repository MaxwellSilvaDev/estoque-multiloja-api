from pydantic import BaseModel, ConfigDict


class EstoqueBase(BaseModel):
    produto_id: int
    loja_id: int
    quantidade: int


class EstoqueResponse(EstoqueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)