import os
import pandas as pd
import csv

# Directory path constants
ROOT_PATH = os.path.abspath(__file__ + "/../../")
DATA_DIR_PATH = os.path.join(ROOT_PATH, "data_files")

# File path constants
CONTRIBUTIONS_PATH = os.path.join(DATA_DIR_PATH, "contributions.csv")
ZIP_CODES_PATH = os.path.join(DATA_DIR_PATH, "zip_code_database.csv")
COUNTY_VOTES_PATH = os.path.join(DATA_DIR_PATH, "county_votes.csv")

# Zip code file-specific constants
# Replacement text for when there is no county name
NO_COUNTY_NAME = "NO_COUNTY_NAME"
# Extraneous words in the zip code file
ZIP_STOP_WORDS = ['County', 'City']
# Length of zip codes provided in zip code file
SHORT_ZIP_CODE_LENGTH = 5
# Length of zip codes that can occur in contributions
LONG_ZIP_CODE_LENGTH = 9

# References points for field names in datasets
ZIP_CODES_FIELD_NAMES = ["zip", "type", "primary_city", "acceptable_cities", "unacceptable_cities", "state", "county",
                         "timezone", "area_codes", "latitude", "longitude", "world_region", "country", "decommissioned",
                         "estimated_population", "notes"]

CONTRIBUTIONS_FIELD_NAMES = ["cmte_id", "cand_id", "cand_nm", "contbr_nm", "contbr_city", "contbr_st", "contbr_zip",
                             "contbr_employer", "contbr_occupation", "contb_receipt_amt", "contb_receipt_dt",
                             "receipt_desc", "memo_cd", "memo_text", "form_tp", "file_num", "tran_id", "election_tp"]

# Mapping of zipcode to county name
zip_codes = {}

with open(ZIP_CODES_PATH, 'rb') as csvfile:
    reader = csv.DictReader(csvfile, ZIP_CODES_FIELD_NAMES)
    for row in reader:
        # Look out for types, they're different everywhere and need to be consistent
        zipcode = str(row['zip'])
        # Change in implementation may require state being passed as well
        # state = row['state']
        county = str(row['county'])
        # Cannot split no length strings
        if len(county) == 0:
            continue
        split = county.split()
        # TODO: will cause errors when city is valid.
        # TODO: add city whitelist, perhaps don't use it at all
        # Throw out stop words at the end of the county name
        if split[-1] in ZIP_STOP_WORDS:
            county = " ".join(split[:-1]).strip()
        zip_codes[zipcode] = county


def get_county(zip_code):
    try:
        zip_code = str(int(zip_code))
    except:
        return "%s" % NO_COUNTY_NAME

    # Convert long zip codes to short
    if len(zip_code) == LONG_ZIP_CODE_LENGTH:
        zip_code = zip_code[:SHORT_ZIP_CODE_LENGTH]
    if zip_code in zip_codes:
        return zip_codes[zip_code]
    else:
        return "%s" % NO_COUNTY_NAME


def example_zip_to_county():
    # Rename CONTRIBUTIONS_PATH if you would like to use a smaller test file
    # CONTRIBUTIONS_PATH = os.path.join(DATA_DIR_PATH, "VA.csv")
    contributions = pd.read_csv(CONTRIBUTIONS_PATH)
    print contributions["contbr_zip"].apply(get_county)