from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..models import cart as cart_model
from ..models import product as product_model
from ..schemas import cart as cart_schema


def add_to_cart(db: Session, user_id: int, cart_item: cart_schema.CartAdd):
    product = db.query(product_model.Product).filter(product_model.Product.id == cart_item.product_id).first()
    if not product:
        raise NotFoundError("Product not found")

    existing_item = db.query(cart_model.Cart).filter(
        cart_model.Cart.user_id == user_id,
        cart_model.Cart.product_id == cart_item.product_id,
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_cart_item = cart_model.Cart(
        user_id=user_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
    )
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item


def list_cart_items(db: Session, user_id: int):
    return db.query(cart_model.Cart).filter(cart_model.Cart.user_id == user_id).all()


def remove_from_cart(db: Session, cart_id: int, user_id: int):
    cart_item = db.query(cart_model.Cart).filter(
        cart_model.Cart.id == cart_id,
        cart_model.Cart.user_id == user_id,
    ).first()

    if not cart_item:
        raise NotFoundError("Cart item not found")

    db.delete(cart_item)
    db.commit()
