from typing import Optional

from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..models import product as product_model
from ..schemas import product as product_schema


def create_product(db: Session, product_data: product_schema.ProductCreate):
    new_product = product_model.Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def list_products(
    db: Session,
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
):
    query = db.query(product_model.Product)

    if category:
        query = query.filter(product_model.Product.category == category)
    if search:
        query = query.filter(product_model.Product.name.ilike(f"%{search}%"))

    offset = (page - 1) * limit
    return query.order_by(product_model.Product.id).offset(offset).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    if not product:
        raise NotFoundError("Product not found")
    return product


def update_product(db: Session, product_id: int, updated_product: product_schema.ProductUpdate):
    product = get_product_by_id(db, product_id)

    update_data = updated_product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()
