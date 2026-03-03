# FastAPI WebApp

Backend application built with FastAPI as a foundation for a marketplace-style web platform.

## Tech Stack

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic

## Current Features

- Create item (POST /items)
- Get item by ID (GET /items/{item_id})
- In-memory storage (temporary)
- Automatic OpenAPI documentation

## Run Locally (Windows)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload