from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MaterialObj(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    description = Column(String)
