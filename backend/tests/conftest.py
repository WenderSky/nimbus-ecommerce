from __future__ import annotations

from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.seed import seed

# Banco em memória isolado para os testes (não toca no app.db de produção).
# StaticPool mantém a mesma conexão entre threads do TestClient.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _override_get_db() -> Iterator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def _setup_database() -> Iterator[None]:
    """Cria o schema e popula o catálogo uma vez por sessão de testes."""
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        seed(db)
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> TestClient:
    # Evita o evento de startup (que criaria/popularia o app.db real).
    return TestClient(app, raise_server_exceptions=True)
