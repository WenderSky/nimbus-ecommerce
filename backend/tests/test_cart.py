from __future__ import annotations

from decimal import Decimal

from fastapi.testclient import TestClient


def _get_product(client: TestClient, product_id: int) -> dict:
    return client.get(f"/api/products/{product_id}").json()


def test_cart_total_decimal_exact(client: TestClient) -> None:
    """O total exibido deve bater exatamente com o cálculo em Decimal."""
    p1 = _get_product(client, 1)
    p2 = _get_product(client, 4)

    payload = {"items": [{"product_id": 1, "qty": 2}, {"product_id": 4, "qty": 3}]}
    resp = client.post("/api/cart", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    esperado = (Decimal(p1["preco"]) * 2 + Decimal(p2["preco"]) * 3).quantize(
        Decimal("0.01")
    )
    assert Decimal(data["total"]) == esperado

    # Cada subtotal também precisa estar correto e quantizado.
    linha1 = next(i for i in data["items"] if i["product_id"] == 1)
    assert Decimal(linha1["subtotal"]) == (Decimal(p1["preco"]) * 2).quantize(
        Decimal("0.01")
    )


def test_cart_total_matches_sum_of_subtotals(client: TestClient) -> None:
    payload = {"items": [{"product_id": 2, "qty": 1}, {"product_id": 7, "qty": 2}]}
    resp = client.post("/api/cart", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    soma = sum(Decimal(i["subtotal"]) for i in data["items"])
    assert Decimal(data["total"]) == soma


def test_cart_out_of_stock(client: TestClient) -> None:
    produto = _get_product(client, 2)
    payload = {"items": [{"product_id": 2, "qty": produto["estoque"] + 1}]}
    resp = client.post("/api/cart", json=payload)
    assert resp.status_code == 409


def test_cart_product_not_found(client: TestClient) -> None:
    payload = {"items": [{"product_id": 99999, "qty": 1}]}
    resp = client.post("/api/cart", json=payload)
    assert resp.status_code == 404


def test_cart_invalid_qty(client: TestClient) -> None:
    payload = {"items": [{"product_id": 1, "qty": 0}]}
    resp = client.post("/api/cart", json=payload)
    assert resp.status_code == 422
