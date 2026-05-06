# address-book-api

A REST API to manage an address book — built with FastAPI, async SQLAlchemy, and SQLite.
Supports full CRUD and finding addresses near a location using real geodesic distance.

---

## Tech Stack

- **FastAPI** — async web framework
- **SQLAlchemy (async)** + **aiosqlite** — non-blocking database layer
- **Pydantic v2** — request validation and serialization
- **Geopy** — geodesic distance calculation (accounts for Earth's curvature)
- **SQLite** — lightweight local database, auto-created on first run

---

## Getting Started

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at → http://127.0.0.1:8000  
Swagger UI → http://127.0.0.1:8000/docs

---

## Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/addresses/` | Add a new address |
| GET | `/addresses/` | List all addresses |
| GET | `/addresses/{id}` | Get one address |
| PUT | `/addresses/{id}` | Update an address |
| DELETE | `/addresses/{id}` | Delete an address |
| GET | `/addresses/nearby` | Find addresses within X km |

---

## Nearby Search

```
GET /addresses/nearby?latitude=12.9716&longitude=77.5946&distance_km=10
```

Returns every address within the given radius.
Uses **geodesic distance** (not straight-line) so it's accurate across the globe.

---

## Sample Payload

```json
POST /addresses/
{
  "label": "Office",
  "street": "Damrak 1",
  "city": "Amsterdam",
  "state": "North Holland",
  "country": "Netherlands",
  "postal_code": "1012 LG",
  "latitude": 52.3745,
  "longitude": 4.8979
}
```

---

## Project Structure

```
address_book/
├── main.py            # app entry point, logging setup
├── requirements.txt
└── app/
    ├── database.py    # async engine + session
    ├── models.py      # SQLAlchemy ORM model
    ├── schemas.py     # Pydantic schemas + coordinate validation
    └── routes.py      # all route handlers
```

---

## Notes

- Database file is auto-created on first run, no setup needed
- Lat/lon validated at schema level (-90/90 and -180/180)
- All routes are fully async
- Structured logging on every operation
