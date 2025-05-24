import pandas as pd


def get_category_average(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df[column_name].mean()
