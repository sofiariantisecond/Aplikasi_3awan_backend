from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id_menu = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10,2), nullable=False)
    image = Column(String, nullable=True)
    id_category = Column(Integer, ForeignKey("menu_category.id_category"))
    status = Column(String, default="available")  # available / unavailable
    created_at = Column(DateTime, default=datetime.utcnow)