from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# O banco vive ao lado do pacote da aplicação (backend/app.db).
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"

# check_same_thread=False é necessário porque o SQLite é acessado por threads
# diferentes do servidor ASGI.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Classe base declarativa para todos os modelos ORM."""


def get_db() -> Session:
    """Dependência do FastAPI: abre uma sessão por requisição e a fecha ao fim."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
