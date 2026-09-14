import getpass

from app.crud.usuario import criar_usuario
from app.db.session import SessionLocal
from app.schemas.usuario import UsuarioCreate


def main():
    nome = input(
        "Nome do administrador: "
    ).strip()

    email = input(
        "E-mail do administrador: "
    ).strip()

    senha = getpass.getpass(
        "Senha do administrador: "
    )

    db = SessionLocal()

    try:
        usuario = criar_usuario(
            db,
            UsuarioCreate(
                nome=nome,
                email=email,
                senha=senha,
                perfil="admin",
                loja_id=None,
            ),
        )

        print(
            f"Administrador criado com sucesso: "
            f"{usuario.email}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()