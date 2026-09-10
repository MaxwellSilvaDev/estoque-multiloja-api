from fastapi import FastAPI

from app.api.routes.lojas import router as lojas_router
from app.api.routes.produtos import router as produtos_router
from app.api.routes.estoques import router as estoques_router
from app.api.routes.movimentacoes import router as movimentacoes_router


app = FastAPI(
    title="Estoque Multiloja API",
    version="1.0.0",
    description="API para controle de estoque de múltiplas lojas."
)

app.include_router(lojas_router)
app.include_router(produtos_router)
app.include_router(estoques_router)
app.include_router(movimentacoes_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "Estoque Multiloja API funcionando"
    }