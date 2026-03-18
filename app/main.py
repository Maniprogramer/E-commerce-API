from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .db.database import Base, engine
from .models import user, product, cart, order
from .api import auth, products, cart as cart_api, orders
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.exceptions import AppError

def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield

    app = FastAPI(
        title="E-commerce API",
        description="A simple scalable E-commerce API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error": exc.error_code},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "errors": exc.errors()},
        )

    app.include_router(auth.router)
    app.include_router(products.router)
    app.include_router(cart_api.router)
    app.include_router(orders.router)

    @app.get("/api")
    def read_root():
        return {"message": "Welcome to the E-commerce API"}

    import os
    if os.path.exists("frontend"):
        app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

    return app


app = create_app()
