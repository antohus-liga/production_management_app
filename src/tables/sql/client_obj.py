from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from tables.sql.base import Base


class ClientObj(Base):
    __tablename__ = "suppliers"

    cod_cli = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone_number = Column(String)
    email = Column(String)
