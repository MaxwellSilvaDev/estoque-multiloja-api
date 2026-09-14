from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import gerar_hash_senha
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


def criar_usuario(
    db: Session,
    dados: UsuarioCreate,
) -> Usuario:
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil,
        loja_id=dados.loja_id,
    )

    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Já existe um usuário com este e-mail."
        )