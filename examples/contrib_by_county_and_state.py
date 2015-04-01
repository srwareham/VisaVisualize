import pandas as pd
from context import campaignadvisor

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


if __name__ == "__main__":
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path())
    zip_codes_map = campaignadvisor.data_cleanup.get_zip_codes_map()
    # NOTE: keyword argument is not optional. The apply method is just a little hanky
    # Full blown code smell, probably a better way while still preserving ability to keep state at right scope
    # print contributions["contbr_zip"].apply(campaignadvisor.data_cleanup.get_county, zip_codes_map=zip_codes_map)
    contributions_dataframe['contrb_county'] = contributions_dataframe['contbr_zip'].apply(
        campaignadvisor.data_cleanup.get_county, zip_codes_map=zip_codes_map)
    county_state_group_contrib = contributions_dataframe.groupby(['contbr_st', 'contrb_county'])[
        'contb_receipt_amt'].mean()
    # county_state_group_contrib.to_csv('contrib_by_county_and_state.csv')
    print_full(county_state_group_contrib)
