from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Category, Product


class CategoryRepository:
    """Acesso a dados de categorias."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Category]:
        stmt = select(Category).order_by(Category.nome)
        return list(self.db.scalars(stmt).all())

    def get_by_slug(self, slug: str) -> Optional[Category]:
        stmt = select(Category).where(Category.slug == slug)
        return self.db.scalars(stmt).first()


class ProductRepository:
    """Acesso a dados de produtos, incluindo filtros e ordenação."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.get(Product, product_id)

    def list(
        self,
        *,
        category_id: Optional[int] = None,
        q: Optional[str] = None,
        order: Optional[str] = None,
    ) -> list[Product]:
        stmt = select(Product)

        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)

        if q:
            stmt = stmt.where(Product.nome.ilike(f"%{q}%"))

        if order == "price_asc":
            stmt = stmt.order_by(Product.preco.asc())
        elif order == "price_desc":
            stmt = stmt.order_by(Product.preco.desc())
        elif order == "rating":
            stmt = stmt.order_by(Product.rating.desc())
        else:
            stmt = stmt.order_by(Product.id.asc())

        return list(self.db.scalars(stmt).all())
