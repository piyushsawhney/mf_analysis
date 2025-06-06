# db/init_db.py

from db.base import Base  # Base = declarative_base()
from db.engine import engine


def init_db():
    Base.metadata.create_all(bind=engine)
