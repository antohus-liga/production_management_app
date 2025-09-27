import os

from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "data",
)
db_path = os.path.join(data_path, "stock_info.db")

engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base()


class ClientObj(Base):
    __tablename__ = "clients"

    cod_cli = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone_number = Column(String)
    email = Column(String)


class MaterialObj(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)


class MovementInObj(Base):
    __tablename__ = "movements_in"

    movement_nr = Column(Integer, primary_key=True)
    material_id = Column(String, ForeignKey("materials.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_sup = Column(String, ForeignKey("suppliers.cod_sup"))


class MovementOutObj(Base):
    __tablename__ = "movements_out"

    movement_nr = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_cli = Column(String, ForeignKey("clients.cod_cli"))


class ProductObj(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
    selling_price = Column(Float)


class SupplierObj(Base):
    __tablename__ = "suppliers"

    cod_sup = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone_number = Column(String)
    email = Column(String)


Base.metadata.create_all(bind=engine)
