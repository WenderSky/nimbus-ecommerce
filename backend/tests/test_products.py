from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_categories(client: TestClient) -> None:
    resp = client.get("/api/categories")
    assert resp.status_code == 200
    slugs = {c["slug"] for c in resp.json()}
    assert {"notebooks", "perifericos", "monitores", "audio"} <= slugs


def test_list_products(client: TestClient) -> None:
    resp = client.get("/api/products")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 12
    assert {"id", "nome", "preco", "category_id", "estoque"} <= set(data[0].keys())


def test_filter_by_category(client: TestClient) -> None:
    resp = client.get("/api/products", params={"category": "notebooks"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert all("Notebook" in p["nome"] for p in data)


def test_filter_by_unknown_category_returns_empty(client: TestClient) -> None:
    resp = client.get("/api/products", params={"category": "inexistente"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_by_name(client: TestClient) -> None:
    resp = client.get("/api/products", params={"q": "monitor"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 3
    assert all("monitor" in p["nome"].lower() for p in data)


def test_order_price_asc(client: TestClient) -> None:
    resp = client.get("/api/products", params={"order": "price_asc"})
    assert resp.status_code == 200
    precos = [float(p["preco"]) for p in resp.json()]
    assert precos == sorted(precos)


def test_order_price_desc(client: TestClient) -> None:
    resp = client.get("/api/products", params={"order": "price_desc"})
    assert resp.status_code == 200
    precos = [float(p["preco"]) for p in resp.json()]
    assert precos == sorted(precos, reverse=True)


def test_order_rating(client: TestClient) -> None:
    resp = client.get("/api/products", params={"order": "rating"})
    assert resp.status_code == 200
    ratings = [p["rating"] for p in resp.json()]
    assert ratings == sorted(ratings, reverse=True)


def test_get_product_by_id(client: TestClient) -> None:
    resp = client.get("/api/products/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1


def test_get_product_not_found(client: TestClient) -> None:
    resp = client.get("/api/products/99999")
    assert resp.status_code == 404
