import pandas as pd
import numpy as np
import matplotlib.pyplot as pylot

from context import campaignadvisor

"""
Plots the unemployment rate of counties versus the median contribution in it.
Only counties with both fields are shown.
"""


def print_dataframe_fingerprint(df, name):
    print "DataFrame " + name + ":"
    print "Size:", len(df)
    print "Columns:", df.columns
    print "Index:", df.index
    pass


def zip_to_fips(zip_code):
    state_county = campaignadvisor.data_cleanup.get_state_county_from_zip_code(zip_code)
    fips_code = campaignadvisor.data_cleanup.get_fips_from_state_county(state_county)
    return fips_code

if __name__ == "__main__":
    # Get job data
    rural_atlas_data_10_resource = campaignadvisor.resources.get_resource("RuralAtlasData10.xls")
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")

    jobs['clean_fips'] = jobs['FIPS'].apply(campaignadvisor.data_cleanup.get_clean_fips)

    # Get contributions and aggregate them by state_county
    contributions_resource = campaignadvisor.resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path(), dtype=object)#{'contrb_zip': object,'contb_receipt_amt': np.float64})
    contributions_dataframe['clean_zips'] = contributions_dataframe['contbr_zip'].apply(campaignadvisor.data_cleanup.get_clean_zip)
    contributions_dataframe['clean_fips'] = contributions_dataframe['clean_zips'].apply(zip_to_fips)
    contributions_dataframe['clean_contribution'] = contributions_dataframe['contb_receipt_amt'].apply(np.float64)

    """
    GOAL:
    group by county (using clean_fips)
    have dataframe with columns clean_fips and median_contribution
    that's it !

    """

    grouped = contributions_dataframe.groupby(['clean_fips'], as_index=False)
    print grouped.describe()

    median_contribution_by_county = grouped.median().reset_index()[['clean_fips', 'clean_contribution']]

    # Create new table where each row contains a county's median contribution amount, and its job statistics
    #median_contribution_by_county = contributions_dataframe.groupby('clean_fips')[['clean_fips', 'clean_contribution']].median()


    jobs_counties = list(jobs['clean_fips'])
    contributions_counties =list(median_contribution_by_county['clean_fips'])


    # Join only those with intersection
    joined = pd.merge(median_contribution_by_county, jobs, on="clean_fips", sort=False, how="inner")

    # Count the number of contributions in each county
    joined['ContributionsCount'] = contributions_dataframe.groupby('clean_fips').size()

    #Exclude count from FIPS code 0
    joined = joined[joined['clean_fips'] != 0]

    # Filter out counties with less than 100 contributions
    joined['ContributionsCount'] = contributions_dataframe.groupby('clean_fips').size()
    joined = joined[joined['ContributionsCount'] >= 100]
    
    # Plot scatter plot
    joined.plot(kind='scatter', x='UnempRate2012', y='clean_contribution')
    pylot.show()