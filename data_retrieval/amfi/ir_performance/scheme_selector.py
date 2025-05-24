import difflib
import re

from db.db_functions import session
from models import MFScheme


def process_scheme_code_map(scheme_code_map):
    cleaned_scheme_map = {}
    pattern_keywords = re.compile(r'\b(GROWTH|REGULAR|PLAN|OPTION)\b|[-]', re.IGNORECASE)
    pattern_formerly = re.compile(r'\(\s*FORMERLY.*?\)', re.IGNORECASE)
    pattern_empty_parentheses = re.compile(r'\(\s*\)')  # Specifically remove empty ()
    for name, code in scheme_code_map.items():
        cleaned_name = re.sub(pattern_formerly, '', name)
        cleaned_name = re.sub(pattern_keywords, '', cleaned_name)
        cleaned_name = re.sub(pattern_empty_parentheses, '', cleaned_name)
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
        cleaned_scheme_map[cleaned_name] = code
    return cleaned_scheme_map


def get_all_schemes_in_subcategory(subcategory):
    # TODO: Organise this function
    schemes = session.query(MFScheme.scheme_name, MFScheme.amfi_code) \
        .filter(MFScheme.sub_category == subcategory).all()
    scheme_code_map = {scheme.scheme_name: scheme.amfi_code for scheme in schemes}
    return process_scheme_code_map(scheme_code_map)


def get_amfi_code_from_scheme_name(scheme_code_map, scheme_name):
    closest_matches = difflib.get_close_matches(scheme_name, scheme_code_map.keys(), n=1, cutoff=0.80)
    if closest_matches:
        best_match = closest_matches[0]
        if scheme_name.strip().split()[0].lower() == best_match.strip().split()[0].lower():
            scheme_code = scheme_code_map[best_match]
            print(f"SchemeName: {scheme_name}")
            print(f"Best match: {best_match}")
            print(f"Scheme code: {scheme_code}")
            return scheme_code
        return None
    else:
        print(f"No close match found. {scheme_name}")
        return None
