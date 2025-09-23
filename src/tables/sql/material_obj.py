from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class MaterialObj(Base):
    __tablename__ = "materials"

    material_id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    cod_sup = Column(String, ForeignKey("suppliers.cod_sup"))

    movements_in = relationship("MovementInObj", back_populates="materials")
