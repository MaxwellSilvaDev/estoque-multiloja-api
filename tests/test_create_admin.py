from app.crud.usuario import buscar_usuario_por_email


def test_script_create_admin_possui_funcao_principal():
    from app.scripts.create_admin import main

    assert callable(main)


def test_script_create_admin_cria_primeiro_admin(
    db_session,
    monkeypatch,
):
    from app.scripts import create_admin

    respostas = iter(
        [
            "Administrador Inicial",
            "admin@example.com",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda mensagem="": next(respostas),
    )

    monkeypatch.setattr(
        create_admin.getpass,
        "getpass",
        lambda mensagem="": "SenhaSegura123",
    )

    monkeypatch.setattr(
        create_admin,
        "SessionLocal",
        lambda: db_session,
    )

    create_admin.main()

    usuario = buscar_usuario_por_email(
        db_session,
        "admin@example.com",
    )

    assert usuario is not None
    assert usuario.nome == "Administrador Inicial"
    assert usuario.perfil == "admin"
    assert usuario.ativo is True
    assert usuario.loja_id is None
    assert usuario.senha_hash != "SenhaSegura123"