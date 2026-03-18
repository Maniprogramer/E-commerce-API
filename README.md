# Scalable E-commerce API

This is a backend project for a scalable E-commerce API built with FastAPI.
It includes a clean architecture, database connectivity with PostgreSQL, JWT authentication, product management, and a shopping cart system.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ecommerce-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database:**
   Update your `.env` file with your PostgreSQL credentials.

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Technologies Used
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Passlib (bcrypt)
