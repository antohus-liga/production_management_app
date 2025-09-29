from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from sql.tables import (ClientObj, MaterialObj, MovementInObj, MovementOutObj,
                        ProductObj, SupplierObj, engine)

Session = sessionmaker(bind=engine)
session = Session()


def insert(obj):
    try:
        session.add(obj)
        session.commit()
    except IntegrityError:
        print(f"[ERROR] Key already exists, tried to insert {obj}.")


def load_table(table: str):
    table_map = {
        "clients": session.query(ClientObj).all(),
        "materials": session.query(MaterialObj).all(),
        "suppliers": session.query(SupplierObj).all(),
        "products": session.query(ProductObj).all(),
        "movements_out": session.query(MovementOutObj).all(),
        "movements_in": session.query(MovementInObj).all(),
    }

    try:
        return table_map[table]
    except KeyError:
        return None


# insert(
#     ClientObj(
#         cod_cli="ASKH879J",
#         name="David Novo Gonçalves",
#         city="Póvoa de Varzim",
#         country="Portugal",
#         phone="986187368",
#         email="davidnovo1408@gmail.com",
#     )
# )
