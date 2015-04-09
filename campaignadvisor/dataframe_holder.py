import os

try:
    import cPickle as pickle
except ImportError:
    import pickle
import numpy as np
import pandas as pd
import resources
import data_cleanup.data_cleanup

PROJECT_ROOT_PATH = os.path.abspath(__file__ + "/../../")
PICKLES_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "pickles")


class DataFrameWrapper:
    def __init__(self, name, path, creation_function, use_pickle=True):
        self.name = name
        self.path = path
        self.creation_function = creation_function
        self.use_pickle = use_pickle


def create_jobs():
    rural_atlas_data_10_resource = resources.get_resource("RuralAtlasData10.xls")
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")
    jobs['clean_fips'] = jobs['FIPS'].apply(data_cleanup.data_cleanup.get_clean_fips)
    return jobs


def create_contributions():
    contributions_resource = resources.get_resource("contributions.csv")
    contributions_dataframe = pd.read_csv(
        contributions_resource.get_local_path(), dtype={'contrb_zip': object, 'contb_receipt_amt': np.float64}
    )
    # TODO: perhaps throw out counties that have less than 'n' contributions
    contributions_dataframe['clean_fips'] = contributions_dataframe['contbr_zip'].apply(
        data_cleanup.data_cleanup.get_fips_from_zip_code)
    return contributions_dataframe


def save_pickle(data, path):
    with open(path, 'wb') as file_out:
        pickle.dump(data, file_out)


def load_pickle(path):
    with open(path, 'rb') as file_in:
        return pickle.load(file_in)


DATAFRAMES = {
    "jobs": DataFrameWrapper("jobs", os.path.join(PICKLES_DIRECTORY, "jobs.pik"), create_jobs),
    "contributions": DataFrameWrapper("contributions", os.path.join(PICKLES_DIRECTORY, "contributions.pik"),
                                      create_contributions, use_pickle=False)
}


def get_dataframe(name):
    """
    Return a pandas dataframe object.

    If the dataframe has been pickled, the pickle will be loaded and returned; otherwise the dataframe will be
    constructed, saved as a pickle, and returned.

    :param name: Name of the pandas dataframe
    :return: The pandas dataframe
    """
    if name not in DATAFRAMES:
        print "ERROR " + name + " not defined!"
    else:
        dataframe = DATAFRAMES[name]
        path = dataframe.path
        use_pickle = dataframe.use_pickle
        if use_pickle and os.path.isfile(path):
            return load_pickle(path)
        else:
            df = dataframe.creation_function()
            if use_pickle:
                save_pickle(df, path)
            return df


def debug():
    df = get_dataframe("contributions")
    print len(df)

if __name__ == "__main__":
    debug()