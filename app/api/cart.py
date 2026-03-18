from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..models import cart as cart_model, product as product_model, user as user_model
from ..schemas import cart as cart_schema
from ..api.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=cart_schema.CartResponse)
def add_to_cart(
    cart_item: cart_schema.CartAdd, 
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_user)
):
    product = db.query(product_model.Product).filter(product_model.Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(cart_model.Cart).filter(
        cart_model.Cart.user_id == current_user.id,
        cart_model.Cart.product_id == cart_item.product_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_cart_item = cart_model.Cart(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item

@router.get("/", response_model=List[cart_schema.CartResponse])
def view_cart(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    cart_items = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == current_user.id).all()
    return cart_items

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(cart_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    cart_query = db.query(cart_model.Cart).filter(
        cart_model.Cart.id == cart_id,
        cart_model.Cart.user_id == current_user.id
    )
    cart_item = cart_query.first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_query.delete(synchronize_session=False)
    db.commit()
