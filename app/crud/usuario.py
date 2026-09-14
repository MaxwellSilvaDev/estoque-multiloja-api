from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import gerar_hash_senha
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


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


def buscar_usuario_por_email(
    db: Session,
    email: str,
) -> Usuario | None:
    return db.scalar(
        select(Usuario).where(
            Usuario.email == email
        )
    )


def buscar_usuario_por_id(
    db: Session,
    usuario_id: int,
) -> Usuario | None:
    return db.get(
        Usuario,
        usuario_id,
    )


def listar_usuarios(
    db: Session,
) -> list[Usuario]:
    return list(
        db.scalars(
            select(Usuario).order_by(
                Usuario.id
            )
        ).all()
    )


def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados: UsuarioUpdate,
) -> Usuario | None:
    usuario = buscar_usuario_por_id(
        db,
        usuario_id,
    )

    if usuario is None:
        return None

    atualizacoes = dados.model_dump(
        exclude_unset=True,
    )

    for campo, valor in atualizacoes.items():
        setattr(
            usuario,
            campo,
            valor,
        )

    db.commit()
    db.refresh(usuario)

    return usuario