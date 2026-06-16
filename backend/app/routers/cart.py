from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CartIn, CartOut
from ..services import CartService, NotFoundError, OutOfStockError

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.post("", response_model=CartOut, summary="Calcular carrinho")
def calculate_cart(payload: CartIn, db: Session = Depends(get_db)) -> CartOut:
    """Calcula subtotais e total do carrinho. Não persiste nenhum pedido."""
    try:
        return CartService(db).calculate(payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except OutOfStockError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
