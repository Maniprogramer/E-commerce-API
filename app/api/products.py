from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas import product as product_schema
from ..services import product_service
from ..api.auth import get_current_admin_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=product_schema.ProductResponse)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    return product_service.create_product(db, product)

@router.get("/", response_model=List[product_schema.ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
):
    return product_service.list_products(db, category=category, search=search, page=page, limit=limit)

@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)

@router.put("/{product_id}", response_model=product_schema.ProductResponse)
def update_product(product_id: int, updated_product: product_schema.ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    return product_service.update_product(db, product_id, updated_product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_admin_user)):
    product_service.delete_product(db, product_id)
