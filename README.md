# FastAPI Manga Store

A manga store demo with a catalog, accounts, orders, and user roles. Built with FastAPI, SQLAlchemy, SQLite, and Jinja2. Archived.

## Run

Requires Python 3.10+. Use `python3` if `python` is unavailable.

```sh
git clone https://github.com/drugdamage/fastapi-manga-store.git
cd fastapi-manga-store
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS/Linux or `.\.venv\Scripts\Activate.ps1` in Windows PowerShell, then:

```sh
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [the store](http://127.0.0.1:8000) or [API docs](http://127.0.0.1:8000/docs). Startup creates `manga_store.db` if needed and seeds demo products and accounts.

## Demo accounts

| Login | Password | Access |
|---|---|---|
| `user` | `user123` | Browse, place orders, view own orders |
| `manager` | `manager123` | Also add/edit products and view all orders |
| `admin` | `admin123` | Also manage user roles |

The products API is at `/api/items`.
