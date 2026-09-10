from pydantic import BaseModel, ConfigDict


class LojaBase(BaseModel):
    nome: str
    endereco: str
    tipo: str


class LojaCreate(LojaBase):
    pass


class LojaUpdate(BaseModel):
    nome: str | None = None
    endereco: str | None = None
    tipo: str | None = None


class LojaResponse(LojaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)