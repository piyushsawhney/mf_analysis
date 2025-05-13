from data_retrieval.amfi_schemes import update_amfi_schemes_to_db
from db import init_db
from db.engine import SessionLocal

#
# # Create tables
# init_db()
#
# # Example: Insert or fetch data
#
# scheme = MFScheme(
#     isin="INF123456789",
#     amfi_code="123456",
#     scheme_name="Test Equity Fund",
#     sebi_scheme_code="EQ123",
#     plan="Direct",
#     option="Growth",
#     category="Equity",
#     sub_category="Large Cap"
# )
#
# session.add(scheme)
# session.commit()
if __name__ == '__main__':
    init_db()
    session = SessionLocal()
    update_amfi_schemes_to_db("resources/nav.txt")