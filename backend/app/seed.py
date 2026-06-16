from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Category, Product

# Catálogo fictício de tecnologia. (slug_categoria, [produtos]).
CATEGORIES: list[dict] = [
    {"nome": "Notebooks", "slug": "notebooks"},
    {"nome": "Periféricos", "slug": "perifericos"},
    {"nome": "Monitores", "slug": "monitores"},
    {"nome": "Áudio", "slug": "audio"},
]

PRODUCTS: list[dict] = [
    {
        "nome": "Notebook Nimbus Air 14",
        "descricao": "Ultrafino 14'' com 16GB de RAM e SSD NVMe de 512GB.",
        "preco": "6299.90",
        "slug": "notebooks",
        "rating": 4.8,
        "estoque": 12,
        "imagem_url": "https://picsum.photos/seed/nimbus-air14/600/400",
    },
    {
        "nome": "Notebook Nimbus Pro 16",
        "descricao": "Estação de trabalho 16'' com GPU dedicada e 32GB de RAM.",
        "preco": "11499.00",
        "slug": "notebooks",
        "rating": 4.9,
        "estoque": 5,
        "imagem_url": "https://picsum.photos/seed/nimbus-pro16/600/400",
    },
    {
        "nome": "Notebook Nimbus Lite 13",
        "descricao": "Compacto e econômico para o dia a dia, bateria de 18h.",
        "preco": "3799.50",
        "slug": "notebooks",
        "rating": 4.3,
        "estoque": 20,
        "imagem_url": "https://picsum.photos/seed/nimbus-lite13/600/400",
    },
    {
        "nome": "Teclado Mecânico Nimbus K1",
        "descricao": "Switches lineares, layout ABNT2 e retroiluminação RGB.",
        "preco": "459.90",
        "slug": "perifericos",
        "rating": 4.6,
        "estoque": 40,
        "imagem_url": "https://picsum.photos/seed/nimbus-k1/600/400",
    },
    {
        "nome": "Mouse Sem Fio Nimbus M2",
        "descricao": "Sensor de 16.000 DPI, 6 botões e bateria recarregável.",
        "preco": "229.90",
        "slug": "perifericos",
        "rating": 4.5,
        "estoque": 60,
        "imagem_url": "https://picsum.photos/seed/nimbus-m2/600/400",
    },
    {
        "nome": "Webcam Nimbus View 1080p",
        "descricao": "Full HD 60fps com microfone estéreo e foco automático.",
        "preco": "349.00",
        "slug": "perifericos",
        "rating": 4.2,
        "estoque": 25,
        "imagem_url": "https://picsum.photos/seed/nimbus-view/600/400",
    },
    {
        "nome": "Monitor Nimbus 27 QHD",
        "descricao": "27'' IPS 2560x1440, 144Hz e 1ms de tempo de resposta.",
        "preco": "1899.90",
        "slug": "monitores",
        "rating": 4.7,
        "estoque": 15,
        "imagem_url": "https://picsum.photos/seed/nimbus-27qhd/600/400",
    },
    {
        "nome": "Monitor Nimbus 32 4K",
        "descricao": "32'' 4K UHD com cobertura de 98% do espaço DCI-P3.",
        "preco": "3299.00",
        "slug": "monitores",
        "rating": 4.8,
        "estoque": 8,
        "imagem_url": "https://picsum.photos/seed/nimbus-32-4k/600/400",
    },
    {
        "nome": "Monitor Nimbus 24 Office",
        "descricao": "24'' Full HD com painel antirreflexo, ideal para escritório.",
        "preco": "899.90",
        "slug": "monitores",
        "rating": 4.1,
        "estoque": 30,
        "imagem_url": "https://picsum.photos/seed/nimbus-24office/600/400",
    },
    {
        "nome": "Headset Nimbus Sound H3",
        "descricao": "Over-ear com cancelamento de ruído ativo e 40h de bateria.",
        "preco": "799.90",
        "slug": "audio",
        "rating": 4.6,
        "estoque": 18,
        "imagem_url": "https://picsum.photos/seed/nimbus-h3/600/400",
    },
    {
        "nome": "Fones Nimbus Buds Pro",
        "descricao": "In-ear TWS com ANC, estojo de carga e resistência IPX5.",
        "preco": "549.00",
        "slug": "audio",
        "rating": 4.4,
        "estoque": 35,
        "imagem_url": "https://picsum.photos/seed/nimbus-buds/600/400",
    },
    {
        "nome": "Caixa de Som Nimbus Boom",
        "descricao": "Bluetooth 5.3, 30W RMS, à prova d'água e 24h de reprodução.",
        "preco": "639.90",
        "slug": "audio",
        "rating": 4.5,
        "estoque": 22,
        "imagem_url": "https://picsum.photos/seed/nimbus-boom/600/400",
    },
]


def seed(db: Session) -> None:
    """Popula o banco com o catálogo fictício. Idempotente: só roda se vazio."""
    existing = db.scalar(select(func.count()).select_from(Product))
    if existing:
        return

    categories: dict[str, Category] = {}
    for data in CATEGORIES:
        category = Category(nome=data["nome"], slug=data["slug"])
        db.add(category)
        categories[data["slug"]] = category
    db.flush()  # garante os IDs das categorias antes de inserir produtos.

    for data in PRODUCTS:
        category = categories[data["slug"]]
        db.add(
            Product(
                nome=data["nome"],
                descricao=data["descricao"],
                preco=Decimal(data["preco"]),
                category_id=category.id,
                rating=data["rating"],
                estoque=data["estoque"],
                imagem_url=data["imagem_url"],
            )
        )

    db.commit()
