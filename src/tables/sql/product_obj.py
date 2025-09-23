from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class ProductObj(Base):
    __tablename__ = "products"

    prod_id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
