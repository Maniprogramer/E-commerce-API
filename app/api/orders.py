from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..db.database import get_db
from ..models import user as user_model
from ..schemas import order as order_schema
from ..api.auth import get_current_user
from ..services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=order_schema.OrderResponse)
def place_order(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return order_service.place_order(db, current_user.id)

@router.get("/", response_model=List[order_schema.OrderResponse])
def get_order_history(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return order_service.list_orders(db, current_user.id)

@router.post("/pay", response_model=order_schema.OrderResponse)
def simulate_payment(payment: order_schema.PaymentRequest, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return order_service.process_payment(db, current_user.id, payment)
