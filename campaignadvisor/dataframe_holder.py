
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
CONTRIBUTIONS = "contributions"
JOBS_VS_CONTRIBUTIONS = "jobs_vs_contributions"

# Serialized version names
VOTES_SERIALIZED_NAME = "votes.pik"
JOBS_SERIALIZED_NAME = "jobs.pik"
CONTRIBUTIONS_SERIALIZED_NAME = "contributions.pik"
JOBS_VS_CONTRIBUTIONS_SERIALIZED_NAME = "jobs_vs_contributions.pik"


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


class DataFrameWrapper:
    def __init__(self, name, path, creation_function, use_pickle=True):
        self.name = name
        self.path = path
        self.creation_function = creation_function
        self.use_pickle = use_pickle


def _create_jobs():
    rural_atlas_data_10_resource = resources.get_resource("%s" % RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")
    jobs[('%s' % CLEAN_FIPS)] = jobs[('%s' % FIPS)].apply(data_cleanup.data_cleanup.get_clean_fips)
    return jobs


def _create_contributions():
    contributions_resource = resources.get_resource("%s" % CONTRIBUTIONS_CSV)
    # MUST read in all as objects. Presumed bug in pandas implementation truncates significant information if not
    # read in as a string 0001 becomes 1
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path(), dtype=object)
    contributions_dataframe[('%s' % CLEAN_ZIPS)] = contributions_dataframe[('%s' % CONTRIBUTION_ZIP)].apply(
        data_cleanup.data_cleanup.get_clean_zip)
    contributions_dataframe[('%s' % CLEAN_FIPS)] = contributions_dataframe[CLEAN_ZIPS].apply(
        data_cleanup.data_cleanup.get_fips_from_zip_code)
    contributions_dataframe[('%s' % CLEAN_CONTRIBUTION)] = contributions_dataframe[('%s' % CONTRIBUTION_AMOUNT)].apply(
        np.float64)
    return contributions_dataframe


def _index_to_column(df, new_column_name):
    # assign the new_column_name as the index (whatever was given in the group by step)
    df[new_column_name] = df.index
    # reset the index to the row number to prevent confusion
    df.index = range(len(df.index))
    return df


def _create_jobs_vs_contributions():
    # Get job data
    jobs = get_dataframe('%s' % JOBS)

    # Get all contributions
    contributions_dataframe = get_dataframe('%s' % CONTRIBUTIONS)

    # Group by clean_fips
    grouped = contributions_dataframe.groupby("%s" % CLEAN_FIPS)
    # Create dataframe with median contributions as a column
    median_contributions = _index_to_column(grouped.median(), '%s' % CLEAN_FIPS)
    # Create dataframe with mean contributions as a column
    mean_contributions = _index_to_column(grouped.mean(), '%s' % CLEAN_FIPS)

    # Create dataframe with columns: clean_fips clean_contribution_mean and clean_contribution_median (county by county)
    contributions_by_county = pd.merge(median_contributions, mean_contributions, on=CLEAN_FIPS, sort=False,
                                       how="inner", suffixes=('_median', '_mean'))

    # Merge jobs data into contributions by county (joins only those with an intersection)
    joined = pd.merge(contributions_by_county, jobs, on=CLEAN_FIPS, sort=False, how="inner")

    # Count the number of contributions in each county
    contributions_size_series = grouped.size()
    contributions_size_dataframe = pd.DataFrame(contributions_size_series, columns=[CONTRIBUTIONS_COUNT])
    contributions_size_dataframe[('%s' % CLEAN_FIPS)] = contributions_size_dataframe.index
    # Add the number of contributions by county as a column
    joined = pd.merge(joined, contributions_size_dataframe, on=CLEAN_FIPS, sort=False, how="inner")

    # Exclude count from FIPS code 0
    # Exclude invalid fips (00000 is entire US, -1 is error, -2 and below are special cases without matching data)
    joined = joined[joined[('%s' % CLEAN_FIPS)] > 0]

    # Throw out data that don't meet a minimum number of contributions
    # (don't want to over weigh input based on law of small numbers)
    # Cutoff is implemented as 25th percentile of occurrences
    count_cutoff = np.percentile(joined[CONTRIBUTIONS_COUNT], 25)

    # Filter out counties with less than cutoff contributions
    joined = joined[joined[('%s' % CONTRIBUTIONS_COUNT)] >= count_cutoff]
    return joined


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
    Produce a dictionary of dataframewrapper name to the dataframe wrapper object
    :return:
    """
    # Only add the name for the path field.  The full path will automatically be substituted
    df_definitions = [
        DataFrameWrapper(JOBS, "%s" % JOBS_SERIALIZED_NAME, _create_jobs),
        DataFrameWrapper(CONTRIBUTIONS, CONTRIBUTIONS_SERIALIZED_NAME, _create_contributions, use_pickle=False),
        DataFrameWrapper("%s" % JOBS_VS_CONTRIBUTIONS, JOBS_VS_CONTRIBUTIONS_SERIALIZED_NAME,
                         _create_jobs_vs_contributions, use_pickle=True),
        DataFrameWrapper("%s" % VOTES, "%s" % VOTES_SERIALIZED_NAME, data_cleanup.vote_holder.get_county_dataframe)
    ]

    dfs = {}
    for df in df_definitions:
        df.path = os.path.join(SERIALIZED_DATA_DIRECTORY, df.path)
        dfs[df.name] = df
    return dfs


DATA_FRAME_WRAPPERS = _get_data_frames()


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
    if name not in DATA_FRAME_WRAPPERS:
        print "ERROR " + name + " not defined!"
    else:
        dataframe = DATA_FRAME_WRAPPERS[name]
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
    df = get_dataframe(JOBS_VS_CONTRIBUTIONS)
    print len(df)
    print df.head()


if __name__ == "__main__":
    debug()