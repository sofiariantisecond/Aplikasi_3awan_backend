from sqlalchemy import Column, String, Integer, DateTime, DECIMAL, Text, ForeignKey
from datetime import datetime
from config.database import Base


class MenuCategory(Base):
    __tablename__ = "menu_category"

    id_category = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)