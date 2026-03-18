from fastapi import FastAPI
from .db.database import Base, engine
from app.models import user, product
from app.api import auth, products

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="A simple scalable E-commerce API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}
