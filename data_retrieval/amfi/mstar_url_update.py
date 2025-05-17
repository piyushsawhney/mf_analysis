import pandas as pd

from db.db_functions import perform_upsert_on_one_cell
from models import MFScheme


def update_scheme_urls(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['mstar_url'])
    for _, row in df.iterrows():
        perform_upsert_on_one_cell(MFScheme, "amfi_code", row['amfi_code'], "mstar_url", row["mstar_url"])
