from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class SupplierObj(Base):
    __tablename__ = "suppliers"

    cod_sup = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone_number = Column(String)
    email = Column(String)

    movements_in = relationship("MovementInObj", back_populates="suppliers")
