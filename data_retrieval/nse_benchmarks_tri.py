from datetime import datetime
from decimal import Decimal

from nsepython import index_total_returns

from db.db_functions import perform_upsert_update_on_conflict
from models import MFBenchmarkValue


# symbol = "NIFTY 50"
# start_date = "01-May-2000"
# end_date = "14-May-2025"
# # tri_data = index_total_returns(symbol,start_date,end_date)
# # tri_data.to_csv("tri_data.csv")
# # print(type(index_total_returns(symbol,start_date,end_date)))
#
# df = pd.read_csv('tri_data.csv')
# #
# # from datetime import datetime
# # from decimal import Decimal
# #
# #
# benchmark_values = []
# #
# for _, row in df.iterrows():
#     benchmark_value = MFBenchmarkValue(
#         code=row["Index Name"].upper(),
#         date=datetime.strptime(row["Date"], "%d %b %Y").date(),
#         value=Decimal(str(row["TotalReturnsIndex"]))
#     )
#     benchmark_values.append(benchmark_value)


def download_historical_tri(benchmark_code, start_date, end_date):
    parsed_start_date = start_date.strftime("%d-%b-%Y")
    parsed_end_date = end_date.strftime("%d-%b-%Y")
    tri_data = index_total_returns(benchmark_code, parsed_start_date, parsed_end_date)
    # tri_data = pd.read_csv('tri_data.csv')
    benchmark_values = []

    for _, row in tri_data.iterrows():
        benchmark_values.append({
            "code": row["Index Name"].upper(),
            "date": datetime.strptime(row["Date"], "%d %b %Y").date(),
            "value": Decimal(str(row["TotalReturnsIndex"]))
        })
    perform_upsert_update_on_conflict(MFBenchmarkValue, benchmark_values, ["code", "date"])
