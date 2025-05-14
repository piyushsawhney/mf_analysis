from datetime import date, datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

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


def process_five_year_nav(isin, amc_code, amfi_scheme_code, start_date, end_date):
    response = requests.post(AMFI_HISTORICAL, data=prepare_payload(amc_code, amfi_scheme_code, start_date, end_date),
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
                    isin=isin,
                    date=nav_date,
                    nav=nav_value
                )
                perform_upsert(nav_entry)


