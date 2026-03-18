from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, paid, failed, shipped
