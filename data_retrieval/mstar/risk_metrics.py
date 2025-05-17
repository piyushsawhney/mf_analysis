from selenium.webdriver.common.by import By

from mf_selenium.selenium_setup import driver


def get_risk_metrics():
    table = driver.find_element(By.CSS_SELECTOR, '.sal-risk-volatility-measures__dataTable table')
    header_row = table.find_element(By.CSS_SELECTOR, 'thead tr')
    headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, 'th')]
    header_indices = {}
    target_columns = ["Capture Ratios", "Investment", "Category", "Index"]
    for col in target_columns:
        if col in headers:
            header_indices[col] = headers.index(col)
    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
    data = []
    for row in rows:
        row_header = row.find_elements(By.TAG_NAME, 'th')
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = {}
        for col_name, idx in header_indices.items():
            if idx < len(cells) + 1:
                if idx == 0:
                    row_data[col_name] = row_header[idx].text.strip()
                else:
                    row_data[col_name] = cells[idx - 1].text.strip()
            else:
                row_data[col_name] = ''
        data.append(row_data)
    return data
