import pandas as pd
from context import campaignadvisor

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def zip_code_to_county_state(zip_code):
    state_county = campaignadvisor.data_cleanup.get_state_county_from_zip_code(zip_code)
    return str(zip_code) + " " + " ".join(state_county)

if __name__ == "__main__":
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path())
    contributions_dataframe['contrb_county'] = contributions_dataframe['contbr_zip'].apply(zip_code_to_county_state)
    county_state_group_contrib = contributions_dataframe.groupby(['contbr_st', 'contrb_county'])[
        'contb_receipt_amt'].mean()
    # county_state_group_contrib.to_csv('contrib_by_county_and_state.csv')
    print_full(county_state_group_contrib)