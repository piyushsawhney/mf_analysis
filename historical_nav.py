import requests

url = "https://api.mfapi.in/mf/{{scheme_code}}"

import pandas as pd

# Load the Excel file
excel_file = 'test.xlsx'

# Read all sheet names
sheet_names = pd.ExcelFile(excel_file).sheet_names

for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    scheme_codes = df['amfi_scheme_code'].astype(str).tolist()
    nav_df = pd.DataFrame(columns=scheme_codes)

    # print(df)
    for row in df.itertuples():
        scheme_code = str(row.amfi_scheme_code)
        print(row.amfi_scheme_code)
        updated_url = url.replace("{{scheme_code}}", scheme_code)
        response = requests.get(updated_url)

        if response.status_code == 200:
            data = response.json()
            nav_data = data.get('data', [])  # 'data' key holds historical NAVs

            for entry in nav_data:
                date_str = entry.get('date')  # format: 'DD-MM-YYYY'
                nav_value = entry.get('nav')

                # Parse date and nav
                date = pd.to_datetime(date_str,
                                      format='%d-%m-%Y').date()  # .date() removes the time part
                nav = float(nav_value)

                # Update or add row
                if date in nav_df.index:
                    nav_df.at[date, scheme_code] = nav
                else:
                    # Create a new row with NaNs and set the specific scheme's NAV
                    nav_df.loc[date] = pd.Series({scheme_code: nav})


        else:
            print(f"Failed to fetch data for scheme {scheme_code}")
        # break
    nav_df.sort_index(inplace=True)
    nav_df.to_excel("test1.xlsx")
    break
    # print(nav_df)

# # Read each sheet into a DataFrame and combine them
# df_combined = pd.concat(pd.read_excel(excel_file, sheet_name=sheet) for sheet in sheet_names)
#
# # Optional: reset the index
# df_combined.reset_index(drop=True, inplace=True)
#
# # Show the combined DataFrame
# print(df_combined)
#
#
# # Read a specific sheet by name
# df = pd.read_excel('your_file.xlsx', sheet_name='Sheet2')
#
# # Or read by sheet index (0-based)
# df = pd.read_excel('your_file.xlsx', sheet_name=1)
