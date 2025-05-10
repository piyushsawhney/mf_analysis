import re
from collections import OrderedDict
from urllib import request

import pandas as pd

AMFI_URL = 'https://www.amfiindia.com/spages/NAVAll.txt'
DOWNLOAD_FILE_PATH = 'resources/nav.txt'

# Define column names
# columns = ['amfi_scheme_code', 'scheme_name', 'isin_growth' 'scheme_category']
df = pd.DataFrame()
print(df)


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


def update_to_db(row):
    # print(row)
    pass


def clean_sheet_name(name):
    # Remove or replace invalid characters
    name = re.sub(r'[\\/*?:\[\]]', '_', name)
    # Truncate to 31 characters (Excel limit)
    return name[:31]


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
                    scheme_category = scheme_values[1].split("-")[0].strip()
                    scheme_subcategory = scheme_values[1].split("-")[1].strip()[:-1]
                #
                # else:
                #     scheme_category = scheme_values[1].strip()[:-1]
            line = line.rstrip("\n")
            if line.count(";") > 2:
                values = line.split(";")
                # date = datetime.strptime(values[5], '%d-%b-%Y').date()
                # try:
                # print(values[2])
                if len(values[1].strip()) > 2 > len(values[2].strip()):
                    if "equity" in scheme_category.lower() or "hybrid" in scheme_category.lower():
                        if all(keyword not in values[3].lower() for keyword in
                               ["direct", "bonus", "retail", "institutional", "idcw", "cum capital", "payout",
                                "interval","segregated"]):
                            # scheme_name = values[3].split("-")[0].strip().upper()
                            scheme_name = values[3].strip().upper()
                            new_row = {'amfi_scheme_code': values[0].strip(), 'scheme_name': scheme_name,
                                       'isin_growth': values[1].strip(), 'scheme_category': scheme_category.upper(),
                                       'scheme_subcategory': scheme_subcategory.upper()}
                            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.sort_values(by='scheme_name', ascending=True)
    with pd.ExcelWriter('test.xlsx') as writer:
        for subcategory, group in df.groupby('scheme_subcategory'):
            print(subcategory)
            sheet_name = clean_sheet_name(str(subcategory))
            group.to_excel(writer, sheet_name=sheet_name, index=False)
    # df.to_excel("test.xlsx")
    print(df.iloc[0])
    #     float(values[4].strip())
    #     if len(values[1].strip()) == 12 and len(values[2].strip()) == 12:
    #         update_to_db(
    #             get_row(int(values[0].strip()), values[1].strip(), values[2].strip(),
    #                     float(values[4].strip()), date,
    #                     values[3].rstrip(), open_ended, scheme_category.rstrip()))
    #     elif len(values[1].strip()) == 12:
    #         update_to_db(
    #             get_row(int(values[0].strip()), values[1].strip(), None, float(values[4].strip()), date,
    #                     values[3].rstrip(), open_ended, scheme_category.strip()))
    #     elif len(values[2].strip()) == 12:
    #         update_to_db(
    #             get_row(int(values[0].strip()), None, values[2].strip(), float(values[4].strip()), date,
    #                     values[3].rstrip(), open_ended, scheme_category.strip()))
    #     elif len(values[1].strip()) != 12 and len(values[2].strip()) != 12:
    #         update_to_db(
    #             get_row(int(values[0].strip()), None, None, float(values[4].strip()), date,
    #                     values[3].rstrip(), open_ended, scheme_category.strip()))
    # except ValueError:
    #     pass
