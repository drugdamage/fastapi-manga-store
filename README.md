# FastAPI Manga Store

Backend web application built with **FastAPI** for a manga store project.

The goal of this project is to learn backend development by building a real web application step by step.

---

## Tech Stack

* Python 3.x
* FastAPI
* Uvicorn
* Pydantic
* Jinja2 (HTML templates)
* CSS

---

## Current Features

* Create manga item (`POST /items`)
* Get item by ID (`GET /items/{item_id}`)
* In-memory storage (temporary)
* Automatic OpenAPI documentation
* Basic backend architecture with **routers / services / models**

---

## Run Locally (Windows)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open in browser:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

---

## Project Structure

```
fastapi-manga-store/
│
├── app/
│   ├── models/
│   │   └── product.py
│   │
│   ├── routers/
│   │   ├── items.py
│   │   └── pages.py
│   │
│   ├── services/
│   │   └── catalog_service.py
│   │
│   ├── templates/
│   │
│   └── static/
│
├── main.py
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

---

## Roadmap

Planned development steps:

* Improve manga catalog UI
* Add database (SQLite + SQLAlchemy)
* Add user authentication
* Add shopping cart
* Add order system
* Add admin panel
