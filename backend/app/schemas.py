from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryOut(BaseModel):
    """Categoria exposta pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    slug: str


class ProductOut(BaseModel):
    """Produto exposto pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str
    preco: Decimal
    category_id: int
    rating: float
    estoque: int
    imagem_url: str


class CartItemIn(BaseModel):
    """Item enviado pelo cliente ao calcular o carrinho."""

    product_id: int
    qty: int = Field(gt=0, description="Quantidade desejada (maior que zero).")


class CartIn(BaseModel):
    """Corpo do POST /api/cart."""

    items: list[CartItemIn] = Field(min_length=1)


class CartLineOut(BaseModel):
    """Linha calculada do carrinho (produto + quantidade + subtotal)."""

    product_id: int
    nome: str
    preco_unitario: Decimal
    qty: int
    subtotal: Decimal


class CartOut(BaseModel):
    """Carrinho calculado retornado pela API (não persistido)."""

    items: list[CartLineOut]
    total: Decimal
