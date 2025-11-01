from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base

class OrderDetail(Base):
    __tablename__ = "order_detail"

    id_detail = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_order = Column(Integer, ForeignKey("orders.id_order"))
    id_menu = Column(Integer, ForeignKey("menu.id_menu"))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)