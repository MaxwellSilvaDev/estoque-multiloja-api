import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.auth import router as auth_router
from app.api.routes.estoques import router as estoques_router
from app.api.routes.lojas import router as lojas_router
from app.api.routes.movimentacoes import router as movimentacoes_router
from app.api.routes.produtos import router as produtos_router


app = FastAPI(
    title="Estoque Multiloja API",
    version="1.0.1",
    description="API para controle de estoque de múltiplas lojas.",
)


@app.middleware("http")
async def bloquear_escrita_em_demo(
    request: Request,
    call_next,
):
    demo_read_only = (
        os.getenv(
            "DEMO_READ_ONLY",
            "false",
        )
        .strip()
        .lower()
        == "true"
    )

    metodos_de_escrita = {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }

    rota_login = (
        request.method == "POST"
        and request.url.path == "/auth/login"
    )

    if (
        demo_read_only
        and request.method in metodos_de_escrita
        and not rota_login
    ):
        return JSONResponse(
            status_code=403,
            content={
                "detail": (
                    "Ambiente de demonstração: "
                    "operações de escrita estão desativadas."
                )
            },
        )

    return await call_next(request)


app.include_router(auth_router)
app.include_router(lojas_router)
app.include_router(produtos_router)
app.include_router(estoques_router)
app.include_router(movimentacoes_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "Estoque Multiloja API funcionando"
    }