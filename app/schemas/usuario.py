from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    perfil: Literal["admin", "operador"] | None = None
    ativo: bool | None = None
    loja_id: int | None = None


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: Literal["admin", "operador"]
    ativo: bool
    loja_id: int | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class LoginRequest(BaseModel):
    email: str = Field(
        min_length=3,
        max_length=255,
    )

    senha: str = Field(
        min_length=8,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str