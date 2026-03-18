from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..models import order as order_model, cart as cart_model, product as product_model, user as user_model
from ..schemas import order as order_schema
from ..api.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=order_schema.OrderResponse)
def place_order(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    cart_items = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == current_user.id).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0.0
    for item in cart_items:
        product = db.query(product_model.Product).filter(product_model.Product.id == item.product_id).first()
        if product:
            total_price += product.price * item.quantity

    new_order = order_model.Order(user_id=current_user.id, total_price=total_price, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Empty the cart
    db.query(cart_model.Cart).filter(cart_model.Cart.user_id == current_user.id).delete(synchronize_session=False)
    db.commit()

    return new_order

@router.get("/", response_model=List[order_schema.OrderResponse])
def get_order_history(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    orders = db.query(order_model.Order).filter(order_model.Order.user_id == current_user.id).all()
    return orders

@router.post("/pay", response_model=order_schema.OrderResponse)
def simulate_payment(payment: order_schema.PaymentRequest, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    order = db.query(order_model.Order).filter(order_model.Order.id == payment.order_id, order_model.Order.user_id == current_user.id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.status == "paid":
        raise HTTPException(status_code=400, detail="Order is already paid")

    if payment.success:
        order.status = "paid"
    else:
        order.status = "failed"
        
    db.commit()
    db.refresh(order)
    return order
