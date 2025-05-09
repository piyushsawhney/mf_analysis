from collections import OrderedDict
from datetime import datetime

from urllib import request

AMFI_URL = 'https://www.amfiindia.com/spages/NAVAll.txt'
DOWNLOAD_FILE_PATH = 'resources/nav.txt'


def download_nav_file(url):
    req = request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'python/urllib'
        }
    )
    response = request.urlopen(req)
    open(DOWNLOAD_FILE_PATH, 'wb').write(response.read())


def update_to_db():
    pass

def get_row(code, isin1, isin2, nav, nav_date, scheme_name, open_ended, scheme_category):
    my_row = OrderedDict()
    my_row['amfi_scheme_code'] = code
    my_row['isin1'] = isin1
    my_row['isin2'] = isin2
    my_row['nav'] = nav
    my_row['nav_date'] = nav_date
    my_row['scheme_name'] = scheme_name
    my_row['open_ended'] = open_ended
    my_row['scheme_category'] = scheme_category
    return my_row

if __name__ == '__main__':
    download_nav_file(AMFI_URL)
    with open(DOWNLOAD_FILE_PATH, 'r') as nav_file:
        nav_file.readline()
        open_ended = True
        scheme_category = ""
        for line in nav_file:
            if "Schemes(" in line:
                scheme_values = line.split("(")
                if 'open' not in scheme_values[0].lower():
                    open_ended = False
                if "-" in scheme_values[1]:
                    scheme_category = scheme_values[1].split("-")[1].strip()[:-1]
                else:
                    scheme_category = scheme_values[1].strip()[:-1]
            line = line.rstrip("\n")
            if line.count(";") > 2:

                values = line.split(";")
                date = datetime.strptime(values[5], '%d-%b-%Y').date()
                try:
                    float(values[4].strip())
                    if len(values[1].strip()) == 12 and len(values[2].strip()) == 12:
                        update_to_db(
                            get_row(int(values[0].strip()), values[1].strip(), values[2].strip(),
                                    float(values[4].strip()), date,
                                    values[3].rstrip(), open_ended, scheme_category.rstrip()))
                    elif len(values[1].strip()) == 12:
                        update_to_db(
                            get_row(int(values[0].strip()), values[1].strip(), None, float(values[4].strip()), date,
                                    values[3].rstrip(), open_ended, scheme_category.strip()))
                    elif len(values[2].strip()) == 12:
                        update_to_db(
                            get_row(int(values[0].strip()), None, values[2].strip(), float(values[4].strip()), date,
                                    values[3].rstrip(), open_ended, scheme_category.strip()))
                    elif len(values[1].strip()) != 12 and len(values[2].strip()) != 12:
                        update_to_db(
                            get_row(int(values[0].strip()), None, None, float(values[4].strip()), date,
                                    values[3].rstrip(), open_ended, scheme_category.strip()))
                except ValueError:
                    pass