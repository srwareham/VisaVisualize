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
    # this should give the median value by clean fips
    median_contributions = contributions_dataframe.groupby("clean_fips").median()
    # this assigns the clean_fips column as the index (clean fips was made the index in the groupby step)
    median_contributions['clean_fips'] = median_contributions.index
    # reset the index to the row number to prevent confusion
    median_contributions.index = range(len(median_contributions.index))



    median_contribution_by_county = median_contributions

    # Create new table where each row contains a county's median contribution amount, and its job statistics
    #median_contribution_by_county = contributions_dataframe.groupby('clean_fips')[['clean_fips', 'clean_contribution']].median()


    jobs_counties = list(jobs['clean_fips'])
    contributions_counties =list(median_contribution_by_county['clean_fips'])


    # Join only those with intersection
    joined = pd.merge(median_contribution_by_county, jobs, on="clean_fips", sort=False, how="inner")

    # Count the number of contributions in each county
    contributions_size_series = contributions_dataframe.groupby('clean_fips').size()
    contributions_size_dataframe = pd.DataFrame(contributions_size_series, columns=['contributions_count'])
    contributions_size_dataframe['clean_fips'] = contributions_size_dataframe.index
    joined = pd.merge(joined, contributions_size_dataframe, on="clean_fips", sort=False, how="inner")

    #Exclude count from FIPS code 0
    joined = joined[joined['clean_fips'] != 0]

    # Filter out counties with less than 100 contributions
    joined = joined[joined['contributions_count'] >= 100]
    
    # Plot scatter plot
    joined.plot(kind='scatter', x='UnempRate2012', y='clean_contribution')
    pylot.show()