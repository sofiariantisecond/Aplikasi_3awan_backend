from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id_cart = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_menu = Column(Integer, ForeignKey("menu.id_menu"))
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)