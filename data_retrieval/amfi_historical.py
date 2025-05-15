from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

from db.db_functions import perform_upsert
from helpers.urls import AMFI_HISTORICAL
from models import MFSchemeNAV


# Request payload


def prepare_payload(amc_code, amfi_scheme_code, start_date, end_date):
    payload = {
        'mfID': str(amc_code),
        'scID': str(amfi_scheme_code),
        'fDate': str(start_date.strftime('%d-%b-%Y')),
        'tDate': str(end_date.strftime('%d-%b-%Y'))
    }
    return payload


headers = {
    'User-Agent': 'Mozilla/5.0'
}


def get_historical_nav(amc_code, amfi_code, start_date, end_date):
    if relativedelta(end_date, start_date).years < 5:
        response = requests.post(AMFI_HISTORICAL, data=prepare_payload(amc_code, amfi_code, start_date, end_date),
                                 headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        no_records = soup.find('div', class_='no-records-found')
        if no_records:
            print("No records to display.")
        else:
            table = soup.find('div', id='divExcelPeriod').find('table')
            rows = table.find_all('tr')[5:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 4:
                    nav_str = cols[0].text.strip()
                    date_str = cols[3].text.strip()
                    print(nav_str, date_str)
                    nav_date = datetime.strptime(date_str, '%d-%b-%Y').date()
                    nav_value = Decimal(nav_str)
                    nav_entry = MFSchemeNAV(
                        amfi_code=amfi_code,
                        date=nav_date,
                        nav=nav_value
                    )
                    perform_upsert(nav_entry)
    else:
        print("*************************DATE DIFFERENCE MORE THAN 5 YEARS")
