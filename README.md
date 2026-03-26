# 🚀 Scalable E-commerce Backend API

A production-style backend system built with FastAPI, simulating real-world e-commerce workflows including authentication, product management, cart handling, and order processing.

🔗 Live API: https://e-commerce-api-three-henna.vercel.app/  
📄 Swagger Docs: https://e-commerce-api-three-henna.vercel.app/docs  
📦 GitHub: https://github.com/Maniprogramer/E-commerce-API/tree/dev  

---

## ⚡ Key Highlights

- Designed a modular and scalable backend architecture using FastAPI
- Implemented secure JWT-based authentication and protected routes
- Built complete e-commerce workflows (Products, Cart, Orders)
- Optimized API responses with pagination, filtering, and search
- Integrated PostgreSQL using SQLAlchemy ORM
- Containerized the application using Docker & Docker Compose
- Added automated testing using Pytest

---

## 🧠 System Design Overview

- Layered architecture: API → Services → Database
- Stateless authentication using JWT tokens
- Scalable relational database schema for products and orders
- Separation of business logic using service layer pattern
- Environment-based configuration using `.env`

---

## 🧩 Features

### 🔐 Authentication
- User signup and login
- JWT-based secure authentication
- Protected profile route

### 🛍️ Product Management
- Full CRUD operations
- Search, filtering, and pagination support

### 🛒 Cart System
- Add/remove items from cart
- User-specific cart handling

### 📦 Order System
- Order placement workflow
- Mock payment integration

### ⚙️ Backend Engineering
- Service layer architecture
- Clean project structure
- Dockerized setup
- Automated testing with Pytest

---

## 📊 Why This Project Matters

This project demonstrates the ability to:

- Build production-ready backend systems
- Design scalable APIs with real-world use cases
- Implement secure authentication and authorization
- Structure code for maintainability and growth
- Work with databases, deployment, and testing

---

## 🏗️ Project Structure

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

---

## ⚙️ Local Setup

```bash
git clone https://github.com/Maniprogramer/E-commerce-API.git
cd E-commerce-API

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload
```

👉 Open Swagger UI: http://127.0.0.1:8000/docs

---

## 🔐 Environment Variables

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ecommerce
SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Run With Docker

```bash
docker compose up --build
```

Services:
- FastAPI app → port 8000  
- PostgreSQL → port 5432  

---

## 🧪 Run Tests

```bash
pytest
```

- Uses SQLite for lightweight testing
- No need for PostgreSQL during tests

---

## 📡 Main API Endpoints

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

---

## 🚀 Deployment Notes

This project is ready for deployment on platforms like Render, Railway, or Vercel.

Steps:
1. Create a PostgreSQL database
2. Set environment variables from `.env.example`
3. Run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📌 Future Improvements

- Add payment gateway integration (Stripe/Razorpay)
- Implement caching (Redis)
- Add role-based access control (RBAC)
- Improve test coverage
- Add rate limiting and logging

---

## 👨‍💻 Author

**Manikanta Yarramneedi**  
Backend Developer | Python | FastAPI | PostgreSQL  
