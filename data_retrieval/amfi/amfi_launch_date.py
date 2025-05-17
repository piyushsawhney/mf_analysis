import pandas as pd

from db.db_functions import perform_insert_on_one_cell
from helpers.urls import AMFI_SCHEMES_CSV
from models import MFScheme


def update_launch_dates():
    df = pd.read_csv(AMFI_SCHEMES_CSV)
    df['Launch Date'] = pd.to_datetime(df['Launch Date'], format='%d-%b-%Y').dt.date
    df = df.dropna(subset=['Code','Launch Date'])
    for _, row in df.iterrows():
        perform_insert_on_one_cell(MFScheme, "amfi_code", row['Code'], "launch_date", row["Launch Date"])
