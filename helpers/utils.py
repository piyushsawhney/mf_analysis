from datetime import date, timedelta


def get_last_month_last_date():
    today = date.today()
    first_day_this_month = today.replace(day=1)
    return first_day_this_month - timedelta(days=1)

def get_last_month_last_working_day():
    today = date.today()
    first_day_this_month = today.replace(day=1)
    last_day_prev_month = first_day_this_month - timedelta(days=1)
    while last_day_prev_month.weekday() >= 5:
        last_day_prev_month -= timedelta(days=1)
    return last_day_prev_month

def safe_float(value, default=0.0):
    try:
        return float(value or default)
    except (ValueError, TypeError):
        return default
