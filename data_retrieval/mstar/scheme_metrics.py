import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up your webdriver (make sure chromedriver or geckodriver is in PATH)
driver = webdriver.Chrome()

# Replace with the URL containing the target table
url = ''
driver.get(url)
time.sleep(4)
# Locate the table using CSS selector
table = driver.find_element(By.CSS_SELECTOR, '.sal-risk-volatility-measures__dataTable table')

# Extract header to find the column indices of the desired columns
header_row = table.find_element(By.CSS_SELECTOR, 'thead tr')
headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, 'th')]

# Map header names to indexes
header_indices = {}
target_columns = ["Capture Ratios", "Investment", "Category", "Index"]
for col in target_columns:
    if col in headers:
        header_indices[col] = headers.index(col)
print(headers)
print(header_indices)
# Extract table body rows
rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

# Parse table rows and extract relevant columns
data = []
for row in rows:
    row_header = row.find_elements(By.TAG_NAME, 'th')
    cells = row.find_elements(By.TAG_NAME, 'td')
    row_data = {}
    for col_name, idx in header_indices.items():
        cell_index = 0
        # Defensive check in case of mismatch
        if idx < len(cells) + 1:
            if idx == 0:
                row_data[col_name] = row_header[idx].text.strip()
            else:
                row_data[col_name] = cells[idx-1].text.strip()



        else:
            row_data[col_name] = ''
    data.append(row_data)

driver.quit()

# Now the `data` list contains dictionaries with the information you want:
for item in data:
    print(item)
