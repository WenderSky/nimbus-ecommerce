# NIMBUS — E-commerce de tecnologia (full-stack demo)

> ⚠️ **Aviso — código proprietário.** Este repositório é **somente para visualização** (demonstração de portfólio). **Proibido clonar, copiar, usar, modificar ou redistribuir**, no todo ou em parte, sem autorização por escrito. Todos os direitos reservados — ver [LICENSE](LICENSE).


E-commerce de tecnologia que demonstra uma aplicação **full-stack** completa:
uma **API REST** em FastAPI com **arquitetura em camadas**, persistência em
**SQLite** via SQLAlchemy 2.x, validação com **Pydantic v2**, tratamento de
dinheiro com `Decimal` e uma **suíte de testes automatizados** com pytest.
O frontend é uma loja de página única com busca, categorias, avaliações e
carrinho lateral, consumindo a API.

**🔗 Demo ao vivo:** https://devanshelltech.com.br/demos/ecommerce/

---

## Arquitetura

O backend separa responsabilidades em camadas bem definidas, no padrão de uma
aplicação de produção:

- **Routers** (`app/routers/`) — expõem os endpoints HTTP, validam entrada/saída
  e traduzem erros de domínio em respostas HTTP. Sem lógica de negócio.
- **Services** (`app/services.py`) — concentram as regras de negócio: filtros,
  cálculo do carrinho com `Decimal`, validação de estoque e erros de domínio.
- **Repositories** (`app/repositories.py`) — encapsulam o acesso ao banco
  (consultas, filtros e ordenação), isolando o ORM do restante.
- **Models** (`app/models.py`) — entidades SQLAlchemy (`Category`, `Product`).
- **Schemas** (`app/schemas.py`) — contratos de request/response em Pydantic v2.

O fluxo é sempre **router → service → repository → banco**. Todo valor monetário
trafega como `Decimal` quantizado em 2 casas, garantindo que o valor exibido
seja exatamente o valor calculado.

---

## Como rodar

### Backend

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000`. O banco `backend/app.db` é criado e
populado com o catálogo de demonstração automaticamente no primeiro start.
A documentação interativa (OpenAPI) fica em `http://127.0.0.1:8000/docs`.

### Testes

```bash
cd backend
.venv/bin/python -m pytest -q
```

### Frontend

Abra `frontend/index.html` no navegador (página única, sem build).

---

## Endpoints

| Método | Rota                  | Descrição                                                        |
| ------ | --------------------- | ---------------------------------------------------------------- |
| GET    | `/api/health`         | Healthcheck (`{"status":"ok"}`).                                 |
| GET    | `/api/categories`     | Lista as categorias.                                             |
| GET    | `/api/products`       | Lista produtos. Filtros: `category` (slug), `q` (busca), `order` (`price_asc`, `price_desc`, `rating`). |
| GET    | `/api/products/{id}`  | Detalha um produto (404 se inexistente).                        |
| POST   | `/api/cart`           | Calcula subtotais e total do carrinho com `Decimal`, validando estoque (não persiste pedido). |

---

## Stack

Python · FastAPI · SQLAlchemy · SQLite · Pydantic · pytest

---

© 2026 Wender Fernando Azevedo Falido · Devan Shell Tech — Todos os direitos
reservados. Código proprietário, ver [LICENSE](LICENSE).
