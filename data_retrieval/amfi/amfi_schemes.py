import requests

from data_retrieval.amfi.skip_amfi_codes import skip_codes_list
from db.db_functions import perform_upsert_update_on_conflict
from helpers.urls import AMFI_DAILY_NAV
from models import MFScheme


def download_amfi_schemes(download_file_path):
    response = requests.get(AMFI_DAILY_NAV)
    if response.status_code == 200:
        with open(download_file_path, 'w', encoding='latin1') as f:
            f.write(response.text)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def process_idcw_scheme(amfi_code, isin1, isin2, scheme_name):
    scheme1 = {
        "isin1": isin1.strip() if len(isin1.strip()) > 3 else None,
        "isin2": isin2.strip() if len(isin2.strip()) > 3 else None,
        "amfi_code": amfi_code.strip(),
        "scheme_name": scheme_name.strip().upper(),
        "plan": get_scheme_plans(scheme_name),
        "option": "IDCW"}

    return scheme1


def get_scheme_plans(scheme_name):
    if "direct" in scheme_name.lower():
        scheme_plan = "DIRECT"
    elif "retail" in scheme_name.lower():
        scheme_plan = "RETAIL"
    elif "institutional" in scheme_name.lower():
        scheme_plan = "INSTITUTIONAL"
    elif "bonus" in scheme_name.lower():
        scheme_plan = "BONUS"
    elif "wealth" in scheme_name.lower():
        scheme_plan = "WEALTH"
    else:
        scheme_plan = "REGULAR"
    return scheme_plan


def process_growth_schmes(amfi_code, isin1, scheme_name):
    scheme1 = {
        "isin1": isin1.strip() if len(isin1.strip()) > 3 else None,
        "amfi_code": amfi_code.strip(),
        "scheme_name": scheme_name.strip().upper(),
        "plan": get_scheme_plans(scheme_name),
        "option": "GROWTH",
    }
    return scheme1


def is_scheme_correct(scheme_name):
    if any(k in scheme_name.lower() for k in ["income distribution", "idcw", "index", "payout","dividend option"]):
        return False
    return True


def process_scheme_from_isin(file_line):
    scheme_values = file_line.split(";")
    amfi_code, isin1, isin2, scheme_name = scheme_values[0], scheme_values[1], scheme_values[2], scheme_values[3]
    # TODO Remove segregated details
    if get_scheme_plans(scheme_name) == "REGULAR" and is_scheme_correct(
            scheme_name) and amfi_code not in skip_codes_list:
        if len(isin2) > 3:
            # For now only processing regular plans
            # return process_idcw_scheme(amfi_code, isin1, isin2, scheme_name)
            return None
        else:
            return process_growth_schmes(amfi_code, isin1, scheme_name)
    return None


def parse_scheme_line(line, scheme_type, scheme_asset_class, scheme_subcategory):
    if "Schemes(" in line:
        scheme_values = line.split("(")
        scheme_type = scheme_values[0].strip().upper()
        if "-" in scheme_values[1]:
            scheme_asset_class = scheme_values[1].split("-")[0].strip().upper()
            scheme_subcategory = scheme_values[1].split("-")[1].strip()[:-1].upper()
        else:
            scheme_asset_class = scheme_values[1].strip()[:-1].upper()
            scheme_subcategory = ""
    return scheme_type, scheme_asset_class, scheme_subcategory


def update_amfi_schemes_to_db(nav_file_path):
    with open(nav_file_path, 'r', encoding="utf-8") as nav_file:
        nav_file.readline()
        scheme_type, scheme_asset_class, scheme_subcategory = "", "", ""
        for line in nav_file:
            stripped = line.strip()
            line = line.rstrip("\n")
            if stripped:
                scheme_type, scheme_asset_class, scheme_subcategory = parse_scheme_line(line, scheme_type,
                                                                                        scheme_asset_class,
                                                                                        scheme_subcategory)
                # Only Open ended equity, hybrid or solution oriented regular growth schemes
                if "open" in scheme_type.lower():
                    if any(k in scheme_asset_class.lower() for k in ["equity", "hybrid", "solution"]):
                        if scheme_subcategory and all(
                                k not in scheme_subcategory.lower() for k in ["arbitrage", "sectoral", "thematic"]):
                            if ';' in stripped:
                                scheme1 = process_scheme_from_isin(line)
                                if scheme1 is not None:
                                    scheme1["type"] = scheme_type if scheme_type != "" else None
                                    scheme1["asset_class"] = scheme_asset_class if scheme_asset_class != "" else None
                                    scheme1["sub_category"] = scheme_subcategory if scheme_subcategory != "" else None
                                    perform_upsert_update_on_conflict(MFScheme, [scheme1], ["amfi_code"])
