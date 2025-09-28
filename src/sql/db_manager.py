from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from sql.tables import engine

Session = sessionmaker(bind=engine)
session = Session()


def insert(obj):
    try:
        session.add(obj)
        session.commit()
    except IntegrityError:
        print(f"[ERROR] Key already exists, tried to insert {obj}.")
