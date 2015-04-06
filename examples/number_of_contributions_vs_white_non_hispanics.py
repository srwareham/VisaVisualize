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
    jobs = workbook.parse(u"People")

    # Get contributions and aggregate them by state_county
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path())
    # TODO: perhaps throw out counties that have less than 'n' contributions
    contributions_dataframe['FIPS'] = contributions_dataframe['contbr_zip'].apply(zip_to_fips)
    # Count the number of contributions in each county
    jobs['ContributionsCount'] = contributions_dataframe.groupby('FIPS').size()
    #Exclude count from FIPS code 0
    jobs = jobs[jobs['FIPS'] != 0]

    jobs['ContributionsCount'] = contributions_dataframe.groupby('FIPS').size()
    jobs = jobs[jobs['ContributionsCount'] >= 100]
    # Plot scatter plot
    jobs.plot(kind='scatter', x='WhiteNonHispanicPct2010', y='ContributionsCount')
    pylot.show()