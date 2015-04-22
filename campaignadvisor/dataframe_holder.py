
"""
Module for accessing relevant data tables.
Contains logic for storing locally serialized caches to *greatly* speed up all accesses after the initial one
"""

import os

try:
    import cPickle as pickle
except ImportError:
    import pickle
import numpy as np
import pandas as pd

import resources
import data_cleanup.data_cleanup
import data_cleanup.vote_holder

PROJECT_ROOT_PATH = os.path.abspath(__file__ + "/../../")
SERIALIZED_DATA_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "serialized_data")


# TODO: limit visibility once know which should be public?
# Dataframe access names
VOTES = "votes"
JOBS = "jobs"
INCOME = "income"
PEOPLE = "people"
VETERANS = "veterans"
CONTRIBUTIONS = "contributions"
JOBS_VS_CONTRIBUTIONS = "jobs_vs_contributions"
COUNTY_STATISTICS = "county_statistics"

# Serialized version names
VOTES_SERIALIZED_NAME = "votes.pik"
JOBS_SERIALIZED_NAME = "jobs.pik"
INCOME_SERIALIZED_NAME = "income.pik"
PEOPLE_SERIALIZED_NAME = "people.pik"
VETERANS_SERIALIZED_NAME = "veterans.pik"
CONTRIBUTIONS_SERIALIZED_NAME = "contributions.pik"
JOBS_VS_CONTRIBUTIONS_SERIALIZED_NAME = "jobs_vs_contributions.pik"
COUNTY_STATISTICS_SERIALIZED_NAME = "county_statistics.pik"


# Resource names
CONTRIBUTIONS_CSV = "contributions.csv"
RURAL_ATLAS_DATA__XLS = "RuralAtlasData10.xls"

# Predefined pandas column names
CONTRIBUTION_ZIP = "contbr_zip"
CONTRIBUTION_AMOUNT = "contb_receipt_amt"
CLEAN_CONTRIBUTION = "clean_contribution"
CONTRIBUTIONS_COUNT = "contributions_count"
CLEAN_FIPS = "clean_fips"
CLEAN_ZIPS = "clean_zips"
FIPS = "FIPS"

# Logic constants
CUTOFF_PERCENTILE = 25


class DataFrameWrapper:
    def __init__(self, name, path, creation_function, use_pickle=True):
        self.name = name
        self.path = path
        self.creation_function = creation_function
        self.use_pickle = use_pickle


def _create_jobs():
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")
    jobs[CLEAN_FIPS] = jobs[FIPS].apply(data_cleanup.data_cleanup.get_clean_fips)
    return jobs


def _create_people():
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    people = workbook.parse(u"People")
    people[CLEAN_FIPS] = people[FIPS].apply(data_cleanup.data_cleanup.get_clean_fips)
    return people


def _create_contributions():
    contributions_resource = resources.get_resource(CONTRIBUTIONS_CSV)
    # MUST read in all as objects. Presumed bug in pandas implementation truncates significant information if not
    # read in as a string 0001 becomes 1
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path(), dtype=object)
    contributions_dataframe[CLEAN_ZIPS] = contributions_dataframe[CONTRIBUTION_ZIP].apply(
        data_cleanup.data_cleanup.get_clean_zip)
    contributions_dataframe[CLEAN_FIPS] = contributions_dataframe[CLEAN_ZIPS].apply(
        data_cleanup.data_cleanup.get_fips_from_zip_code)
    contributions_dataframe[CLEAN_CONTRIBUTION] = contributions_dataframe[CONTRIBUTION_AMOUNT].apply(np.float64)
    return contributions_dataframe


def _index_to_column(df, new_column_name):
    # assign the new_column_name as the index (whatever was given in the group by step)
    df[new_column_name] = df.index
    # reset the index to the row number to prevent confusion
    df.index = range(len(df.index))
    return df


def _create_jobs_vs_contributions():
    # Get job data
    jobs = get_dataframe(JOBS)

    # Get all contributions
    contributions_dataframe = get_dataframe(CONTRIBUTIONS)

    # Group by clean_fips
    grouped = contributions_dataframe.groupby(CLEAN_FIPS)
    # Create dataframe with median contributions as a column
    median_contributions = _index_to_column(grouped.median(), CLEAN_FIPS)
    # Create dataframe with mean contributions as a column
    mean_contributions = _index_to_column(grouped.mean(), CLEAN_FIPS)

    # Create dataframe with columns: clean_fips clean_contribution_mean and clean_contribution_median (county by county)
    contributions_by_county = pd.merge(median_contributions, mean_contributions, on=CLEAN_FIPS, sort=False,
                                       how="inner", suffixes=('_median', '_mean'))

    # Merge jobs data into contributions by county (joins only those with an intersection)
    joined = pd.merge(contributions_by_county, jobs, on=CLEAN_FIPS, sort=False, how="inner")

    # Count the number of contributions in each county
    contributions_size_series = grouped.size()
    contributions_size_dataframe = pd.DataFrame(contributions_size_series, columns=[CONTRIBUTIONS_COUNT])
    contributions_size_dataframe[CLEAN_FIPS] = contributions_size_dataframe.index
    # Add the number of contributions by county as a column
    joined = pd.merge(joined, contributions_size_dataframe, on=CLEAN_FIPS, sort=False, how="inner")

    # Exclude count from FIPS code 0
    # Exclude invalid fips (00000 is entire US, -1 is error, -2 and below are special cases without matching data)
    joined = joined[joined[CLEAN_FIPS] > 0]

    # Throw out data that don't meet a minimum number of contributions
    # (don't want to over weigh input based on law of small numbers)
    # Cutoff is implemented as 25th percentile of occurrences
    count_cutoff = np.percentile(joined[CONTRIBUTIONS_COUNT], CUTOFF_PERCENTILE)

    # Filter out counties with less than cutoff contributions
    joined = joined[joined[CONTRIBUTIONS_COUNT] >= count_cutoff]
    return joined


def _create_income():
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    income = workbook.parse(u"Income")
    income[CLEAN_FIPS] = income[FIPS].apply(data_cleanup.data_cleanup.get_clean_fips)
    return income


def _create_veterans():
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    veterans = workbook.parse(u"Veterans")
    veterans[CLEAN_FIPS] = veterans[FIPS].apply(data_cleanup.data_cleanup.get_clean_fips)
    return veterans


def _create_county_statistics():
    jobs_vs_contributions = get_dataframe(JOBS_VS_CONTRIBUTIONS)
    people = get_dataframe(PEOPLE)
    votes = get_dataframe(VOTES)
    # Avoid collisions because they get messy beyond 2 duplicates
    people.drop(['State', 'County', FIPS], inplace=True, axis=1)
    income = get_dataframe(INCOME)
    income.drop(['State', 'County', FIPS], inplace=True, axis=1)
    veterans = get_dataframe(VETERANS)
    veterans.drop(['State', 'County', FIPS], inplace=True, axis=1)

    # Merge component dataframes
    county_statistics = pd.merge(jobs_vs_contributions, people, on=CLEAN_FIPS, sort=False, how="inner")
    county_statistics = pd.merge(county_statistics, income, on=CLEAN_FIPS, sort=False, how="inner")
    county_statistics = pd.merge(county_statistics, veterans, on=CLEAN_FIPS, sort=False, how="inner")
    county_statistics = pd.merge(county_statistics, votes, on=CLEAN_FIPS, sort=False, how="inner")

    #Add in contributions_per_capita
    county_statistics['contributions_per_capita'] = county_statistics['contributions_count'] * 1.0 / county_statistics['TotalPopEst2012']

    # Rename to lowercase
    county_statistics['state'] = county_statistics['State']
    county_statistics['county'] = county_statistics['County']
    # Drop unwanted columns
    county_statistics.drop(['State', 'County', FIPS], inplace=True, axis=1)
    # Sort columns for clarity
    county_statistics = county_statistics.reindex_axis(sorted(county_statistics.columns), axis=1)
    county_statistics.index = county_statistics[CLEAN_FIPS]
    return county_statistics


def _save_pickle(data, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as file_out:
        pickle.dump(data, file_out)


def _load_pickle(path):
    with open(path, 'rb') as file_in:
        return pickle.load(file_in)


def _get_data_frames():
    """
    Produce a dictionary of DataFrameWrapper name to the dataframe wrapper object
    :return:
    """
    # Only add the name for the path field.  The full path will automatically be substituted
    df_definitions = [
        DataFrameWrapper(JOBS, JOBS_SERIALIZED_NAME, _create_jobs),
        DataFrameWrapper(CONTRIBUTIONS, CONTRIBUTIONS_SERIALIZED_NAME, _create_contributions, use_pickle=False),
        DataFrameWrapper(PEOPLE, PEOPLE_SERIALIZED_NAME, _create_people),
        DataFrameWrapper(INCOME, INCOME_SERIALIZED_NAME, _create_income),
        DataFrameWrapper(VETERANS, VETERANS_SERIALIZED_NAME, _create_veterans),
        DataFrameWrapper(VOTES, VOTES_SERIALIZED_NAME, data_cleanup.vote_holder.get_county_dataframe),
        DataFrameWrapper(JOBS_VS_CONTRIBUTIONS, JOBS_VS_CONTRIBUTIONS_SERIALIZED_NAME, _create_jobs_vs_contributions),
        DataFrameWrapper(COUNTY_STATISTICS, COUNTY_STATISTICS_SERIALIZED_NAME, _create_county_statistics)
    ]

    dfs = {}
    for df in df_definitions:
        df.path = os.path.join(SERIALIZED_DATA_DIRECTORY, df.path)
        dfs[df.name] = df
    return dfs


def get_dataframe(name):
    """
    Return a pandas dataframe object.

    If the dataframe has been serialized, the cache will be loaded and returned; otherwise the dataframe will be
    constructed, saved serialized, and returned.

    Objects may have definitions that instruct this function to consciously not serialize itself. These directions
    will be followed.

    :param name: Name of the pandas dataframe
    :return: The pandas dataframe
    """
    data_frame_wrappers = _get_data_frames()
    if name not in data_frame_wrappers:
        print "ERROR " + name + " not defined!"
    else:
        dataframe = data_frame_wrappers[name]
        path = dataframe.path
        use_pickle = dataframe.use_pickle
        if use_pickle and os.path.isfile(path):
            return _load_pickle(path)
        else:
            df = dataframe.creation_function()
            if use_pickle:
                _save_pickle(df, path)
            return df


def debug():
    df = get_dataframe(COUNTY_STATISTICS)
    print len(df)
    print df.head()
    print list(df.columns)


if __name__ == "__main__":
    debug()