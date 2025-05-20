from data_retrieval.amfi.mstar_url_update import update_scheme_urls
from data_retrieval.mstar.metrics_flow import retrieve_scheme_metrics
from db import init_db
from db.engine import SessionLocal
from models import MFScheme


def filer_by_urls_and_launch_dates():
    from datetime import date, timedelta

    # Calculate date 3 years ago
    three_years_ago = date.today().replace(day=1) - timedelta(days=1)
    three_years_ago = three_years_ago.replace(year=three_years_ago.year - 3)

    # Assuming you already have a session
    schemes = session.query(MFScheme).filter(
        MFScheme.mstar_url.isnot(None),
        MFScheme.last_update_metric.is_(None),
        MFScheme.launch_date <= three_years_ago
    ).all()
    return schemes


if __name__ == '__main__':
    init_db()
    session = SessionLocal()
    # download_amfi_schemes("resources/nav.txt")
    # update_amfi_schemes_to_db("resources/nav.txt")
    # update_launch_dates()
    # update_scheme_urls("resources/scheme_url.csv")
    schemes = filer_by_urls_and_launch_dates()
    for scheme in schemes:
        print(f"AMFI Code: {scheme.amfi_code}, URL: {scheme.mstar_url}, Launch Date: {scheme.launch_date}")

        retrieve_scheme_metrics(scheme.mstar_url, scheme.amfi_code, scheme.launch_date)
