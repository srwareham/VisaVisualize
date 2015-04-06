import pandas as pd
import csv

from context import campaignadvisor

"""
Data cleanup utility

May eventually be used to store cleaned tables instead.
"""

# Zip code file-specific constants
# Replacement text for when there is no county name
NO_COUNTY_NAME = "NO_COUNTY_NAME"
# Replacement text for when there is no state name
NO_STATE_NAME = "NO_STATE_NAME"
# Replacement text for when there is no fips code
NO_FIPS_CODE = "-1"
# Extraneous words to be removed from county names
# NOTE: stop words that are substrings of other stop words must appear AFTER them in this list.
COUNTY_STOP_WORDS = [
    'city and municipality of',
    'city of',
    'municipality of',
    'census area',
    'borough',
    'city',
    'county',
]
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

_STATE_ABBREVIATIONS = states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    # NOTE: There are 9 minor outlying islands, collisions may occur
    'UM': 'United States Minor Outlying Islands',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming',
    # Military state codes
    'AA': 'Armed Forces Americas',
    'AE': 'Armed Forces Africa, Canada, Europe, Middle East',
    'AP': 'Armed Forces Pacific'
}

CUSTOM_FIPS = {
    'armed forces americas': "-2",
    'armed forces africa, canada, europe, middle east': "-3",
    'armed forces pacific': "-4"
}


def _get_state_name(state_abbreviation):
    if state_abbreviation in _STATE_ABBREVIATIONS:
        return _STATE_ABBREVIATIONS[state_abbreviation]
    else:
        return NO_STATE_NAME


# TODO: add whitelist when should actually read Kansas City (if that were a real county)
def _get_clean_county_name(dirty_county_name):
    clean_county_name = dirty_county_name.lower()
    for stop_word in COUNTY_STOP_WORDS:
        if stop_word in clean_county_name:
            clean_county_name = clean_county_name.replace(stop_word, "").strip()
    return clean_county_name


def _get_clean_state_name(dirty_state_name):
    return dirty_state_name.lower()


class FIPSMapper:
    def __init__(self, fips_to_state_county, fips_to_state, state_county_to_fips, state_to_fips):
        self.fips_to_state_county = fips_to_state_county
        self.fips_to_state = fips_to_state
        self.state_county_to_fips = state_county_to_fips
        self.state_to_fips = state_to_fips

# Global variables (strictly for optimization purposes)
the_zip_code_map = None
the_fips_mapper = None


def _get_the_zip_code_map():
    global the_zip_code_map
    if the_zip_code_map is None:
        the_zip_code_map = _get_zip_codes_map()
    return the_zip_code_map


def _get_the_fips_mapper():
    global the_fips_mapper
    if the_fips_mapper is None:
        the_fips_mapper = _get_fips_mapper()
    return the_fips_mapper


def _get_zip_codes_map():
    # Mapping of zipcode to county name
    zip_codes = {}
    zip_codes_resource = campaignadvisor.resources.get_resource("zip_code_database.csv")
    with zip_codes_resource.get_file() as csvfile:
        reader = csv.DictReader(csvfile, ZIP_CODES_FIELD_NAMES)
        for row in reader:
            # Look out for types, they're different everywhere and need to be consistent
            zipcode = str(row['zip'])
            state_abbreviation = str(row['state'])
            state_name = _get_state_name(state_abbreviation)
            # Put to lower case for consistency
            state_name = _get_clean_state_name(state_name)
            # Throw away city, borough, county, etc change to lower case
            county = _get_clean_county_name(str(row['county']))
            if len(county) == 0:
                county = NO_COUNTY_NAME

            if len(state_name) == 0:
                state_name = NO_STATE_NAME
            state_county = state_name, county
            zip_codes[zipcode] = state_county
    return zip_codes


def get_state_county_from_zip_code(zip_code):
    """
    Given a zip code, return its corresponding (state, county) tuple
    :param zip_code: A zip code of length 5 or 9
    :return: The zip code's corresponding (state's name, county's name)
    """
    if type(zip_code) != type(" "):
        return NO_STATE_NAME, NO_COUNTY_NAME
    zip_codes_map = _get_the_zip_code_map()
    # Convert long zip codes to short
    if len(zip_code) > SHORT_ZIP_CODE_LENGTH:
        zip_code = zip_code[:SHORT_ZIP_CODE_LENGTH]
    if zip_code in zip_codes_map:
        return zip_codes_map[zip_code]
    else:
        return NO_STATE_NAME, NO_COUNTY_NAME


FIPS_FIELD_NAMES = ["state_abbreviation", "state_fips", "county_fips", "county_name", "fips_class"]


# TODO: standardize what county names will be
# TODO: add us territories to have custom made fips codes
def _get_fips_mapper():
    national_counties_resource = campaignadvisor.resources.get_resource("national_counties.csv")
    fips_to_state_county = {}
    fips_to_state = {}
    state_county_to_fips = {}
    state_to_fips = {}
    with national_counties_resource.get_file() as csvfile:
        reader = csv.DictReader(csvfile, FIPS_FIELD_NAMES)
        for row in reader:
            # Look out for types, they're different everywhere and need to be consistent
            state_abbreviation = str(row["state_abbreviation"])
            state_name = _get_state_name(state_abbreviation)
            state_name = _get_clean_state_name(state_name)
            state_fips = str(row["state_fips"])
            county_fips = state_fips + str(row["county_fips"])
            county_name = str(row["county_name"])
            county_name = _get_clean_county_name(county_name)

            state_county = (state_name, county_name)

            # TODO:  For all below dictionaries, add error handling for collisions. Should never happen.
            # Build fips_to_state_county
            if county_fips not in fips_to_state_county:
                # TODO: ensure consistent naming convention for counties. This presently lists Fairfax as Fairfax County
                fips_to_state_county[county_fips] = state_county

            # Build fips_to_state
            if state_fips not in fips_to_state:
                fips_to_state[state_fips] = state_name

            # Build state_county_to_fips
            if state_county not in state_county_to_fips:
                state_county_to_fips[state_county] = county_fips

                # Build state_to_fips:
                if state_name not in state_to_fips:
                    state_to_fips[state_name] = state_fips
        for key in CUSTOM_FIPS:
            val = CUSTOM_FIPS[key]
            state_to_fips[key] = val
        return FIPSMapper(fips_to_state_county, fips_to_state, state_county_to_fips, state_to_fips)


def get_state_county_from_fips(fips_code):
    """
    Given a county's fips code , return a tuple of its state's properly capitalized name followed by
    its properly capitalized name.

    NOTE: The formatting of the name returned is currently "alger" rather than "Alger County"
    This is subject to change.

    NOTE: If no county exists but a state can be discerned, the (state_name, NO_COUNTY_NAME) will be returned

    :param fips_code: A county's fips code
    :return: The tuple: (lowercase state name, lowercase county name)
    """
    fips_to_state_county = _get_the_fips_mapper().fips_to_state_county
    fips_to_state = _get_the_fips_mapper().fips_to_state
    state_fips_code = fips_code[:2]
    if fips_code in fips_to_state_county:
        return fips_to_state_county[fips_code]
    elif state_fips_code in fips_to_state:
        return fips_to_state[state_fips_code], NO_COUNTY_NAME
    else:
        return NO_STATE_NAME, NO_COUNTY_NAME


def get_state_from_fips(fips_code):
    """
    Given a state's fips code , return its properly capitalized name
    :param fips_code: A state's fips code
    :return: A state's properly capitalized name
    """
    fips_to_state = _get_the_fips_mapper().fips_to_state
    if fips_code in fips_to_state:
        return fips_to_state[fips_code]
    else:
        return NO_STATE_NAME


# TODO: Standardize how which will be the county name "Alger County" or "Alger"
# TODO: Perhaps add case insensitivity?

def get_fips_from_state_county(state_county):
    """
    Get the fips code of a county in a given state
    If state data is available but county data is not, the state fips code will be returned

    NOTE: This function expects input in the form "COUNTY_NAME + County"
    This implementation may vary

    NOTE: If a state were to have multiple counties with the same name, the return value is not guaranteed to be correct
    NOTE: Some states have municipalities with the same name as the county (Fairfax vs Fairfax County)
    This likely will resolve correctly to the county name, but this is not guaranteed

    :param state_county: A tuple containing the properly capitalized (state, county_ ie:  ("Maryland", "Fairfax County")
    :return: The fips code of the desired city
    """
    # Convert to tuple in case was passed in as a list etc
    # Convert to lowercase to support lookup
    state_name = _get_clean_state_name(state_county[0])
    county_name = _get_clean_county_name(state_county[1])
    state_county = state_name, county_name
    state_county_to_fips = _get_the_fips_mapper().state_county_to_fips
    state_to_fips = _get_the_fips_mapper().state_to_fips
    if state_county in state_county_to_fips:
        return state_county_to_fips[state_county]
    elif state_name in state_to_fips:
        return state_to_fips[state_name]
    else:
        return NO_FIPS_CODE


def get_fips_from_state(state):
    """
    Returns the fips code of a given state.
    :param state: The properly capitalized name of a state
    :return: The state's fips code
    """
    # Lowercase for lookup
    state = _get_clean_state_name(state)
    state_to_fips = _get_the_fips_mapper().state_to_fips
    if state in state_to_fips:
        return state_to_fips[state]
    else:
        return NO_FIPS_CODE


def example_zip_to_county():
    # Rename CONTRIBUTIONS_PATH if you would like to use a smaller test file
    # CONTRIBUTIONS_PATH = os.path.join(DATA_DIR_PATH, "VA.csv")
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions = pd.read_csv(contributions_resource.get_local_path())
    # NOTE: keyword argument is not optional. The apply method is just a little hanky
    # Full blown code smell, probably a better way.
    print contributions["contbr_zip"].apply(get_state_county_from_zip_code)


def debug():
    starting_state_county = ("Virginia", "Fairfax County")
    fips_code = get_fips_from_state_county(starting_state_county)
    state_county = get_state_county_from_fips(fips_code)
    state = state_county[0]
    state_fips = get_fips_from_state(state)

    print "Start:", starting_state_county
    print "County fips:", fips_code
    print "State County found:", state_county
    print "State fips:", state_fips

    # Baltimore city
    print get_state_county_from_fips("24510")


if __name__ == "__main__":
    debug()
    example_zip_to_county()