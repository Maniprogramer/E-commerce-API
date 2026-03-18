from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..db.database import get_db
from ..models import user as user_model
from ..schemas import cart as cart_schema
from ..api.auth import get_current_user
from ..services import cart_service

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=cart_schema.CartResponse)
def add_to_cart(
    cart_item: cart_schema.CartAdd, 
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_user)
):
    return cart_service.add_to_cart(db, current_user.id, cart_item)

@router.get("/", response_model=List[cart_schema.CartResponse])
def view_cart(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return cart_service.list_cart_items(db, current_user.id)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(cart_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    cart_service.remove_from_cart(db, cart_id, current_user.id)
