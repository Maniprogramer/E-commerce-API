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
