import pandas as pd

from helpers.urls import AMFI_SCHEMES_CSV

df = pd.read_csv(AMFI_SCHEMES_CSV)
print(df.columns)
