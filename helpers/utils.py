from datetime import date, timedelta


def get_last_month_last_date():
    today = date.today()
    first_day_this_month = today.replace(day=1)
    return first_day_this_month - timedelta(days=1)


def safe_float(value, default=0.0):
    try:
        return float(value or default)
    except (ValueError, TypeError):
        return default
