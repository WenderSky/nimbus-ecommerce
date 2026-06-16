from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ProductOut
from ..services import NotFoundError, ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut], summary="Listar produtos")
def list_products(
    category: Optional[str] = Query(None, description="Slug da categoria."),
    q: Optional[str] = Query(None, description="Busca por nome do produto."),
    order: Optional[str] = Query(
        None,
        description="Ordenação: price_asc, price_desc ou rating.",
        pattern="^(price_asc|price_desc|rating)$",
    ),
    db: Session = Depends(get_db),
) -> list[ProductOut]:
    return ProductService(db).list_products(category=category, q=q, order=order)


@router.get("/{product_id}", response_model=ProductOut, summary="Detalhar produto")
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductOut:
    try:
        return ProductService(db).get_product(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
