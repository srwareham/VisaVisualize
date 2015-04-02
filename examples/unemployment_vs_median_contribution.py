import pandas as pd
import numpy as np
import matplotlib.pyplot as pylot

from context import campaignadvisor

"""
Plots the unemployment rate of counties versus the median contribution in it.
Only counties with both fields are shown.
"""


def zip_to_fips(zip_code):
    state_county = campaignadvisor.data_cleanup.get_state_county_from_zip_code(zip_code)
    fips_code = campaignadvisor.data_cleanup.get_fips_from_state_county(state_county)
    return np.float64(fips_code)

if __name__ == "__main__":
    # Get job data
    rural_atlas_data_10_resource = campaignadvisor.resources.get_resource("RuralAtlasData10.xls")
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")

    # Get contributions and aggregate them by state_county
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path())
    # TODO: perhaps throw out counties that have less than 'n' contributions
    contributions_dataframe['FIPS'] = contributions_dataframe['contbr_zip'].apply(zip_to_fips)

    # Create new table where each row contains a county's median contribution amount, and its job statistics
    county_state_group_contrib = contributions_dataframe.groupby('FIPS')[['FIPS', 'contb_receipt_amt']].median()

    # Join only those with intersection
    joined = pd.merge(county_state_group_contrib, jobs, on="FIPS", sort=False, how="inner")

    # Plot scatter plot
    joined.plot(kind='scatter', x='UnempRate2012', y='contb_receipt_amt')
    pylot.show()