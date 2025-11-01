from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base

class Order(Base):
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    order_code = Column(String, nullable=False, unique=True)
    total_price = Column(DECIMAL(10,2), nullable=False)
    status = Column(String, default="pending")  
    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime, nullable=True)
    qr_code = Column(String, nullable=True)