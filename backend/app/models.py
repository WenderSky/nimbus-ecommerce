from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Category(Base):
    """Categoria de produtos (ex.: Notebooks, Periféricos)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)

    products: Mapped[list[Product]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Product(Base):
    """Produto do catálogo. O preço é armazenado como Numeric (Decimal)."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False, default="")
    # Numeric(10, 2) garante que o dinheiro nunca passe por float.
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False, default=0)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imagem_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")

    category: Mapped[Category] = relationship(back_populates="products")
