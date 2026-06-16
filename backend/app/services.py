from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from sqlalchemy.orm import Session

from .models import Category, Product
from .repositories import CategoryRepository, ProductRepository
from .schemas import CartIn, CartLineOut, CartOut

# Centavos: toda quantia é quantizada para duas casas decimais.
CENTS = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    """Quantiza um Decimal para 2 casas usando arredondamento comercial."""
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


class NotFoundError(Exception):
    """Recurso não encontrado (mapeado para HTTP 404 no router)."""


class OutOfStockError(Exception):
    """Quantidade solicitada acima do estoque disponível (HTTP 409)."""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.repo = CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        return self.repo.list_all()


class ProductService:
    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)

    def list_products(
        self,
        *,
        category: Optional[str] = None,
        q: Optional[str] = None,
        order: Optional[str] = None,
    ) -> list[Product]:
        category_id: Optional[int] = None
        if category:
            found = self.category_repo.get_by_slug(category)
            # Categoria inexistente => nenhum produto, sem estourar erro.
            if found is None:
                return []
            category_id = found.id

        return self.repo.list(category_id=category_id, q=q, order=order)

    def get_product(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Produto {product_id} não encontrado.")
        return product


class CartService:
    """Calcula o carrinho com Decimal e valida estoque. Não persiste pedido."""

    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def calculate(self, payload: CartIn) -> CartOut:
        lines: list[CartLineOut] = []
        total = Decimal("0.00")

        for item in payload.items:
            product = self.repo.get_by_id(item.product_id)
            if product is None:
                raise NotFoundError(f"Produto {item.product_id} não encontrado.")
            if item.qty > product.estoque:
                raise OutOfStockError(
                    f"Estoque insuficiente para '{product.nome}': "
                    f"solicitado {item.qty}, disponível {product.estoque}."
                )

            preco_unitario = _money(Decimal(product.preco))
            subtotal = _money(preco_unitario * item.qty)
            total += subtotal

            lines.append(
                CartLineOut(
                    product_id=product.id,
                    nome=product.nome,
                    preco_unitario=preco_unitario,
                    qty=item.qty,
                    subtotal=subtotal,
                )
            )

        return CartOut(items=lines, total=_money(total))
