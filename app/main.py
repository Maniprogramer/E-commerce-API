from fastapi import FastAPI
from .db.database import Base, engine
from .models import user, product, cart
from .api import auth, products, cart as cart_api

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="A simple scalable E-commerce API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart_api.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}
