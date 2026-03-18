# Scalable E-commerce API

A simple portfolio backend project built with FastAPI. It covers user authentication, products, cart management, orders, mock payments, Docker setup, and basic automated tests.

## Features

- User signup and login with JWT authentication
- Protected profile route
- Product CRUD APIs
- Product filtering, search, and pagination
- Cart management for logged-in users
- Order placement and mock payment flow
- Simple service layer for cleaner business logic
- Docker and Docker Compose setup
- Basic pytest test suite

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- SQLite for tests
- Passlib with bcrypt
- JWT with `python-jose`
- Pytest
- Docker

## Project Structure

```text
ecommerce-api/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Local Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Copy `.env.example` to `.env` and update the values if needed.
5. Run the API.

```bash
git clone https://github.com/Maniprogramer/E-commerce-API.git
cd E-commerce-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

## Environment Variables

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce
SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Run With Docker

```bash
docker compose up --build
```

This starts:

- FastAPI app on port `8000`
- PostgreSQL on port `5432`

## Run Tests

```bash
pytest
```

The tests use SQLite so they can run without PostgreSQL.

## Main API Endpoints

### Auth

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/profile`

### Products

- `POST /products/`
- `GET /products/`
- `GET /products/{product_id}`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

Query examples:

- `/products/?category=electronics`
- `/products/?search=iphone`
- `/products/?page=1&limit=10`

### Cart

- `POST /cart/`
- `GET /cart/`
- `DELETE /cart/{cart_id}`

### Orders

- `POST /orders/`
- `GET /orders/`
- `POST /orders/pay`

## Deployment Notes

This project is ready to deploy on platforms like Render or Railway. The easiest path is to:

1. Create a PostgreSQL database on the platform.
2. Set the environment variables from `.env.example`.
3. Start the app with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
