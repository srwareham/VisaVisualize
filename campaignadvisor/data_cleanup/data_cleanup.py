import pandas as pd
import csv

import campaignadvisor.resources

"""
Data cleanup utility

May eventually be used to store cleaned tables instead.
"""

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


def get_zip_codes_map():
    # Mapping of zipcode to county name
    zip_codes = {}
    zip_codes_resource = campaignadvisor.resources.get_resource("zip_code_database.csv")
    with zip_codes_resource.get_file() as csvfile:
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
    return zip_codes


# TODO: find way that does not take keyword arguments. Makes it look optional when it is not
def get_county(zip_code, zip_codes_map=None):
    if zip_codes_map is None:
        raise
    try:
        zip_code = str(int(zip_code))
    except:
        return "%s" % NO_COUNTY_NAME

    # Convert long zip codes to short
    if len(zip_code) == LONG_ZIP_CODE_LENGTH:
        zip_code = zip_code[:SHORT_ZIP_CODE_LENGTH]
    if zip_code in zip_codes_map:
        return zip_codes_map[zip_code]
    else:
        return "%s" % NO_COUNTY_NAME


def example_zip_to_county():
    # Rename CONTRIBUTIONS_PATH if you would like to use a smaller test file
    # CONTRIBUTIONS_PATH = os.path.join(DATA_DIR_PATH, "VA.csv")
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_resource.download_if_necessary()
    contributions = pd.read_csv(contributions_resource.get_local_path())
    zip_codes_map = get_zip_codes_map()
    # NOTE: keyword argument is not optional. The apply method is just a little hanky
    # Full blown code smell, probably a better way.
    print contributions["contbr_zip"].apply(get_county, zip_codes_map=zip_codes_map)

if __name__ == "__main__":
    example_zip_to_county()