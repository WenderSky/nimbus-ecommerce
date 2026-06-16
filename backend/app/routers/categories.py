from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CategoryOut
from ..services import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut], summary="Listar categorias")
def list_categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    return CategoryService(db).list_categories()
