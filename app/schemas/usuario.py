from typing import Literal

from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=150,
    )

    email: str = Field(
        min_length=3,
        max_length=255,
    )

    senha: str = Field(
        min_length=8,
    )

    perfil: Literal["admin", "operador"]

    loja_id: int | None = None