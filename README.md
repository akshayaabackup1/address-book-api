# Address Book API

A simple address book REST API built with FastAPI and SQLite. Supports creating, updating, deleting addresses and searching by distance.

## Setup & Run

**1. Clone / download the project**

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate       # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Start the server**
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Swagger docs (interactive): `http://127.0.0.1:8000/docs`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addresses/` | Create a new address |
| GET | `/addresses/` | List all addresses |
| GET | `/addresses/{id}` | Get a specific address |
| PUT | `/addresses/{id}` | Update an address |
| DELETE | `/addresses/{id}` | Delete an address |
| GET | `/addresses/nearby` | Find addresses within a distance |

---

## Nearby Search

```
GET /addresses/nearby?latitude=52.3676&longitude=4.9041&distance_km=5
```

Returns all addresses within `distance_km` kilometers of the given coordinates. Uses geodesic distance (accurate over the Earth's surface).

---

## Example: Create an Address

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
├── main.py          # app entrypoint
├── requirements.txt
└── app/
    ├── database.py  # db engine and session
    ├── models.py    # SQLAlchemy ORM model
    ├── schemas.py   # Pydantic request/response models
    └── routes.py    # all API endpoints
```

## Notes

- The SQLite database file (`addressbook.db`) is auto-created on first run.
- Coordinate validation is handled at the schema level (lat: -90 to 90, lon: -180 to 180).
- Distance calculation uses `geopy`'s `geodesic` method for accuracy.
