from sqlalchemy.dialects.sqlite import insert

from db.engine import SessionLocal

session = SessionLocal()


def perform_upsert_do_nothing(orm, data, index_array):
    stmt = insert(orm).values(**data)
    stmt = stmt.on_conflict_do_nothing(index_elements=index_array)
    session.execute(stmt)
    session.commit()
