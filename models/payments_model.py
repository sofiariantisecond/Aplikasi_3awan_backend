from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base

class Payment(Base):
    __tablename__ = "payment"

    id_payment = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_order = Column(Integer, ForeignKey("orders.id_order"))
    payment_method = Column(String, default="cash")  
    # cash, qris, debit, ewallet
    payment_status = Column(String, default="unpaid")  
    # unpaid, paid, refunded
    payment_date = Column(DateTime, nullable=True) 