from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class MovementOutObj(Base):
    __tablename__ = "materials"

    movement_nr = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_cli = Column(String, ForeignKey("suppliers.cod_cli"))

    products = relationship("ProductObj", back_populates="movements_out")
    clients = relationship("ClientObj", back_populates="movements_out")
