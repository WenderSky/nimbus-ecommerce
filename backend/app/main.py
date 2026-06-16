from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import cart, categories, products
from .seed import seed


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Cria as tabelas e popula o catálogo na primeira execução."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(
    title="NIMBUS API",
    description=(
        "API REST do NIMBUS, e-commerce de tecnologia. "
        "Catálogo, categorias e cálculo de carrinho com arquitetura em camadas."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS liberado para o frontend estático consumir a API durante a demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["health"], summary="Healthcheck")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
