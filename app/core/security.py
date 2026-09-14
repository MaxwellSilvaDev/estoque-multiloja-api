from datetime import datetime, timedelta, timezone

import bcrypt
import jwt


def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    senha_hash = bcrypt.hashpw(
        senha_bytes,
        bcrypt.gensalt(),
    )

    return senha_hash.decode("utf-8")


def verificar_senha(
    senha: str,
    senha_hash: str,
) -> bool:
    return bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8"),
    )


def criar_token_acesso(
    usuario_id: int,
    chave_secreta: str,
) -> str:
    agora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=60),
    }

    return jwt.encode(
        payload,
        chave_secreta,
        algorithm="HS256",
    )