from datetime import date

from data_retrieval.amfi_historical import get_historical_nav
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
    # download_amfi_schemes("resources/nav.txt")
    # update_amfi_schemes_to_db("resources/nav.txt")
    get_historical_nav("3", "119528", date(2025, 5, 2), date(2025, 5, 14))
    # get_nse_benchmarks()
    # download_historical_tri("NIFTY 50", date(2000, 5, 1), date(2025, 5, 14))