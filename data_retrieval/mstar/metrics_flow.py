import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from data_retrieval.mstar.drawdown_metrics import get_drawdown_metrics
from data_retrieval.mstar.risk_metrics import get_risk_metrics
from data_retrieval.mstar.volatility_metrics import get_volatility_metrics
from db.db_functions import perform_upsert_update_on_conflict
from mf_selenium.selenium_setup import driver
from models.metrics import SchemeMetric, SchemeDrawdown


def navigate_to_period(period):
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"button#for{period}Year"))
    )
    element.click()
    time.sleep(2)


def update_risk_metrics_to_db(amfi_code, metrics, period):
    for item in metrics:
        metric_name = item['Capture Ratios'].replace('\n', ' ').strip()
        investment = float(item['Investment'])
        category = float(item['Category'])
        index = float(item['Index'])
        data_array = [{
            "amfi_code": amfi_code,
            "time_horizon": period,
            "metric_name": metric_name.upper(),
            "investment": investment,
            "category": category,
            "index": index
        }]
        perform_upsert_update_on_conflict(SchemeMetric, data_array, ['amfi_code', 'time_horizon', 'metric_name'])


def update_volatility_metrics_to_db(amfi_code, metrics, period):
    for item in metrics:
        metric_name = item['Capture Ratios'].replace('\n', ' ').strip()
        investment = float(item['Investment'])
        category = float(item['Category'])
        index = float(item['Index'])
        data_array = [{
            "amfi_code": amfi_code,
            "time_horizon": period,
            "metric_name": metric_name.upper(),
            "investment": investment,
            "category": category,
            "index": index
        }]
        perform_upsert_update_on_conflict(SchemeMetric, data_array, ['amfi_code', 'time_horizon', 'metric_name'])


def update_drawdown_metrics_to_db(amfi_code, metrics, period):
    for item in metrics:
        peak_date = str(item['Peak'])
        valley_date = str(item['Valley'])
        max_duration = str(item['Max Duration']).upper()
        data_array = [{
            "amfi_code": amfi_code,
            "time_horizon": period,
            "peak_date": datetime.strptime(peak_date, '%m/%d/%Y').date(),
            "valley_date": datetime.strptime(valley_date, '%m/%d/%Y').date(),
            "max_duration": max_duration
        }]
        perform_upsert_update_on_conflict(SchemeDrawdown, data_array, ['amfi_code', 'time_horizon'])


def retrieve_scheme_metrics(url, amfi_code):
    driver.get(url)
    time.sleep(4)
    for period in ['3', '5', '10']:
        navigate_to_period(period)
        update_risk_metrics_to_db(amfi_code, get_risk_metrics(), period)
        update_volatility_metrics_to_db(amfi_code, get_volatility_metrics(), period)
        update_drawdown_metrics_to_db(amfi_code, get_drawdown_metrics(), period)

#
# try:
#     retrieve_scheme_metrics(
#         "https://www.morningstar.in/mutualfunds/f0gbr06s9j/aditya-birla-sun-life-frontline-equity-fund-growth/risk-ratings.aspx",
#         "103174")
# finally:
#     driver.quit()
