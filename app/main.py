from fastapi import FastAPI
from .db.database import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    description="A simple scalable E-commerce API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}

