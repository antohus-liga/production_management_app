from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class MovementInObj(Base):
    __tablename__ = "materials"

    movement_nr = Column(Integer, primary_key=True)
    material_id = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_sup = Column(String, ForeignKey("suppliers.cod_sup"))

    materials = relationship("MaterialObj", back_populates="movements_in")
    suppliers = relationship("SupplierObj", back_populates="movements_in")
