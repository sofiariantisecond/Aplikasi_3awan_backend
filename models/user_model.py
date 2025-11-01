from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, default="customer")  # customer / admin
    created_at = Column(DateTime, default=datetime.utcnow)