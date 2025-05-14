from nsepython import nse_get_index_list

from db.db_functions import perform_upsert_update_on_conflict
from models import MFBenchmark

def get_nse_benchmarks():
    raw_indices = nse_get_index_list()

    records = [{
        'code': index.upper(),
        'name': f'{index.title().upper()} TRI',
        'index_provider': 'NSE'
    } for index in raw_indices]

    perform_upsert_update_on_conflict(MFBenchmark, records, ["code"])
