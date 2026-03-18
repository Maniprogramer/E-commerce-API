from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..models import product as product_model
from ..schemas import product as product_schema

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=product_schema.ProductResponse)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    new_product = product_model.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

from typing import List, Optional

@router.get("/", response_model=List[product_schema.ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(product_model.Product)
    
    if category:
        query = query.filter(product_model.Product.category == category)
    if search:
        query = query.filter(product_model.Product.name.ilike(f"%{search}%"))
        
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=product_schema.ProductResponse)
def update_product(product_id: int, updated_product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    product_query = db.query(product_model.Product).filter(product_model.Product.id == product_id)
    product = product_query.first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    update_data = updated_product.dict(exclude_unset=True)
    product_query.update(update_data, synchronize_session=False)
    db.commit()
    return product_query.first()

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_query = db.query(product_model.Product).filter(product_model.Product.id == product_id)
    product = product_query.first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    product_query.delete(synchronize_session=False)
    db.commit()
