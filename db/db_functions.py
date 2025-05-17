from sqlalchemy import func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError

from db.engine import SessionLocal
from models import MFScheme

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
    session.commit()  # use `merge` to upsert based on PK


def match_string_in_mf_scheme_name(search_string):
    return session.query(MFScheme).filter(
        func.lower(MFScheme.scheme_name).like(f"%{search_string.upper()}%")
    ).all()


def perform_query(orm, field):
    return session.query(orm).filter_by(code=field).first()


def perform_insert(orm_with_data):
    session.add(orm_with_data)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def perform_insert_on_one_cell(orm, key_column, key, target_column, value):
    session.query(orm).filter_by(**{key_column: key}).update({target_column: value})
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


def perform_upsert_on_one_cell(orm, key_column, key, target_column, value):
    instance = session.query(orm).filter_by(**{key_column: key}).first()
    if instance:
        setattr(instance, target_column, value)
    else:
        instance = orm(**{key_column: key, target_column: value})
        session.add(instance)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
