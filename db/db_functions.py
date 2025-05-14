from sqlalchemy.dialects.sqlite import insert

from db.engine import SessionLocal

session = SessionLocal()


def perform_upsert_do_nothing(orm, data, index_array):
    stmt = insert(orm).values(**data)
    stmt = stmt.on_conflict_do_nothing(index_elements=index_array)
    session.execute(stmt)
    session.commit()


def perform_upsert_update_on_conflict(orm, data_array, index_array):
    stmt = insert(orm).values(data_array)
    stmt = stmt.on_conflict_do_update(
        index_elements=index_array,
        set_={col: getattr(stmt.excluded, col) for col in data_array[0] if col not in index_array}
    )
    session.execute(stmt)
    session.commit()


def perform_upsert(orm_data):
    session.merge(orm_data)
    session.commit()# use `merge` to upsert based on PK

