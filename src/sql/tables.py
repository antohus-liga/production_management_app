import os

from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "appdata",
)
db_path = os.path.join(data_path, "prod_info.db")

engine = create_engine(f"sqlite:///{db_path}")
Base = declarative_base()


class ClientObj(Base):
    __tablename__ = "clients"

    cod_cli = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)

    def __repr__(self) -> str:
        return (
            f"(cod_cli={self.cod_cli}, "
            f"name={self.name}, "
            f"city={self.city}, "
            f"country={self.country}, "
            f"phone={self.phone}, "
            f"email={self.email})"
        )


class MaterialObj(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)

    def __repr__(self) -> str:
        return (
            f"(id={self.id}, "
            f"description={self.description}, "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price})"
        )


class MovementInObj(Base):
    __tablename__ = "movements_in"

    movement_nr = Column(Integer, primary_key=True)
    material_id = Column(String, ForeignKey("materials.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_sup = Column(String, ForeignKey("suppliers.cod_sup"))

    def __repr__(self) -> str:
        return (
            f"(movement_nr={self.movement_nr}, "
            f"material_id={self.material_id}, "
            f"quantity={self.quantity}, "
            f"total_price={self.total_price}, "
            f"cod_sup={self.cod_sup})"
        )


class MovementOutObj(Base):
    __tablename__ = "movements_out"

    movement_nr = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    cod_cli = Column(String, ForeignKey("clients.cod_cli"))

    def __repr__(self) -> str:
        return (
            f"(movement_nr={self.movement_nr}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"total_price={self.total_price}, "
            f"cod_cli={self.cod_cli})"
        )


class ProductObj(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    description = Column(String)
    quantity = Column(Integer)
    selling_price = Column(Float)

    def __repr__(self) -> str:
        return (
            f"(id={self.id}, "
            f"description={self.material_id}, "
            f"quantity={self.quantity}, "
            f"selling_price={self.cod_sup})"
        )


class SupplierObj(Base):
    __tablename__ = "suppliers"

    cod_sup = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)

    def __repr__(self) -> str:
        return (
            f"(cod_sup={self.cod_sup}, "
            f"name={self.name}, "
            f"city={self.city}, "
            f"country={self.country}, "
            f"phone={self.phone}, "
            f"email={self.email})"
        )


Base.metadata.create_all(bind=engine)
