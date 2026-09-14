import bcrypt


def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return senha_hash.decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8"),
    )