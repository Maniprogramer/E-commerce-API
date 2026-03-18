from sqlalchemy.orm import Session

from ..core.exceptions import BadRequestError, NotFoundError
from ..models import cart as cart_model
from ..models import order as order_model
from ..models import product as product_model
from ..schemas import order as order_schema


def place_order(db: Session, user_id: int):
    cart_items = db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).all()
    if not cart_items:
        raise BadRequestError("Cart is empty")

    total_price = 0.0
    for item in cart_items:
        product = db.query(product_model.Product).filter(product_model.Product.id == item.product_id).first()
        if not product:
            raise BadRequestError("Cart contains a product that no longer exists")
        total_price += product.price * item.quantity

    new_order = order_model.Order(user_id=user_id, total_price=total_price, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).delete(synchronize_session=False)
    db.commit()

    return new_order


def list_orders(db: Session, user_id: int):
    return db.query(order_model.Order).filter(order_model.Order.user_id == user_id).order_by(order_model.Order.id.desc()).all()


def process_payment(db: Session, user_id: int, payment: order_schema.PaymentRequest):
    order = db.query(order_model.Order).filter(
        order_model.Order.id == payment.order_id,
        order_model.Order.user_id == user_id,
    ).first()

    if not order:
        raise NotFoundError("Order not found")
    if order.status == "paid":
        raise BadRequestError("Order is already paid")

    order.status = "paid" if payment.success else "failed"
    db.commit()
    db.refresh(order)
    return order
