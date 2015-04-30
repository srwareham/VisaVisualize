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
COUNTY_CONTRIBUTIONS = 'county_contributions'
COUNTY_STATISTICS = "county_statistics"
MAP_DATA = "map_data"

# Serialized version names
VOTES_SERIALIZED_NAME = "votes.pik"
JOBS_SERIALIZED_NAME = "jobs.pik"
INCOME_SERIALIZED_NAME = "income.pik"
PEOPLE_SERIALIZED_NAME = "people.pik"
VETERANS_SERIALIZED_NAME = "veterans.pik"
CONTRIBUTIONS_SERIALIZED_NAME = "contributions.pik"
COUNTY_CONTRIBUTIONS_SERIALIZED_NAME = "county_contributions.pik"
COUNTY_STATISTICS_SERIALIZED_NAME = "county_statistics.pik"
MAP_DATA_SERIALIZED_NAME = "map_data.pik"


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
# Is removed from relevant tables
COUNTY = "County"
# Is removed from relevant tables
STATE = "State"
CANDIDATE_NAME = 'cand_nm'
CONTRIBUTION_MEDIAN = 'contribution_median'
CONTRIBUTION_MEAN = 'contribution_mean'
CONTRIBUTION_SUM = 'contribution_sum'
CONTRIBUTION_COUNT = 'contribution_count'
CONTRIBUTIONS_PER_CAPITA = 'contributions_per_capita'
POPULATION_2012 = 'TotalPopEst2012'
TOTAL_VOTES = 'total_votes'
GOP_CONTRIBUTIONS_MEDIAN = 'gop_contributions_median'
DEM_CONTRIBUTIONS_MEDIAN = 'dem_contributions_median'
GOP_CONTRIBUTIONS_MEAN = 'gop_contributions_mean'
DEM_CONTRIBUTIONS_MEAN = 'dem_contributions_mean'
GOP_CONTRIBUTIONS_SUM = 'gop_contributions_sum'
DEM_CONTRIBUTIONS_SUM = 'dem_contributions_sum'
GOP_CONTRIBUTIONS_COUNT = 'gop_contributions_count'
DEM_CONTRIBUTIONS_COUNT = 'dem_contributions_count'

# Logic constants
CUTOFF_PERCENTILE = 25

# String literals
MITT_ROMNEY = 'Romney, Mitt'
BARACK_OBAMA = 'Obama, Barack'


class DataFrameWrapper:
    def __init__(self, name, path, creation_function, use_pickle=True):
        self.name = name
        self.path = path
        self.creation_function = creation_function
        self.use_pickle = use_pickle


def _cleanup_dataframe(dataframe):
    """
    Remove state, county, and fips columns
    set index to be cleanfips
    :param dataframe:
    :return:
    """
    dataframe[CLEAN_FIPS] = dataframe[FIPS].apply(data_cleanup.data_cleanup.get_clean_fips)
    dataframe.index = dataframe[CLEAN_FIPS]
    del dataframe[FIPS]
    del dataframe[STATE]
    del dataframe[COUNTY]
    del dataframe[CLEAN_FIPS]
    return dataframe


def _create_jobs():
    """
    Returns a dataframe with an index for every county in the us. (5 character string always)

    Columns are:
    ['State', 'County', 'NumCivEmployed0812', 'PctEmpAgriculture0812', 'PctEmpManufacturing0812', 'PctEmpServices0812',
    'PctEmpGovt0812', 'PctEmpChange0809', 'UnempRate2009', 'PctEmpChange0910', 'UnempRate2010', 'NumCivLaborForce2008',
    'NumEmployed2008', 'NumUnemployed2008', 'UnempRate2008', 'NumCivLaborForce2009', 'NumEmployed2009',
    'NumUnemployed2009', 'NumCivLaborForce2010', 'NumEmployed2010', 'NumUnemployed2010', 'UnempRate2011',
    'PctEmpChange1011', 'NumCivLaborForce2011', 'NumEmployed2011', 'NumUnemployed2011', 'PctEmpChange0711',
    'NumCivLaborForce2012', 'UnempRate2012', 'NumEmployed2012', 'NumUnemployed2011.1', 'PctEmpChange1012',
    'PctEmpChange0712']

    :return:
    """
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    jobs = workbook.parse(u"Jobs")
    return _cleanup_dataframe(jobs)


def _create_people():
    """
    Returns a dataframe with an index for every county in the us. (5 character string always)

    Columns are:
    ['State', 'County', 'PopChangeRate1013', 'NetMigrationRate1013', 'NaturalChangeRate1013', 'PopChangeRate0010',
    'NetMigrationRate0010', 'NaturalChangeRate0010', 'PopDensity2010', 'Under18Pct2010', 'Age65AndOlderPct2010',
    'WhiteNonHispanicPct2010', 'BlackNonHispanicPct2010', 'AsianNonHispanicPct2010', 'NativeAmericanNonHispanicPct2010',
    'HispanicPct2010', 'MultipleRacePct2010', 'NonHispanicWhitePopChangeRate0010', 'NonHispanicBlackPopChangeRate0010',
    'NonHispanicAsianPopChangeRate0010', 'NonHispanicNativeAmericanPopChangeRate0010', 'HispanicPopChangeRate0010',
    'MultipleRacePopChangeRate0010', 'WhiteNonHispanicNum2010', 'BlackNonHispanicNum2010', 'AsianNonHispanicNum2010',
    'NativeAmericanNonHispanicNum2010', 'HispanicNum2010', 'MultipleRaceNum2010', 'ForeignBornPct0812',
    'ForeignBornEuropePct0812', 'ForeignBornMexPct0812', 'NonEnglishHHPct0812', 'Ed1LessThanHSPct0812',
    'Ed2HSGradOnlyPct0812', 'Ed3SomeCollegePct0812', 'Ed4CollegePlusPct0812', 'AvgHHSize0812', 'FemaleHHPct0812',
    'HH65PlusAlonePct0812', 'OwnHomePct0812', 'Ed2HSGradOnlyNum0812', 'Ed3SomeCollegeNum0812', 'Ed1LessThanHSNum0812',
    'TotalPop25Plus0812', 'ForeignBornCentralSouthAmPct0812', 'NonEnglishHHNum0812', 'HH65PlusAloneNum0812',
    'OwnHomeNum0812', 'FemaleHHNum0812', 'ForeignBornNum0812', 'TotalOccHU0812', 'Ed4CollegePlusNum0812',
    'ForeignBornCentralSouthAmNum0812', 'ForeignBornCaribPct0812', 'ForeignBornCaribNum0812', 'TotalPopACS0812',
    'ForeignBornAfricaNum0812', 'ForeignBornAsiaPct0812', 'ForeignBornAsiaNum0812', 'TotalHH0812',
    'ForeignBornMexNum0812', 'ForeignBornEuropeNum0812', 'ForeignBornAfricaPct0812', 'LandAreaSQMiles2010',
    'TotalPop2010', 'Under18Num2010', 'Age65AndOlderNum2010', 'NetMigrationNum0010', 'NaturalChangeNum0010',
    'TotalPopEst2011', 'TotalPopEstBase2010', 'TotalPopEst2012', 'TotalPopEst2013', 'TotalPopEst2010']

    :return:
    """
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    people = workbook.parse(u"People")
    return _cleanup_dataframe(people)


def _create_income():
    """
    Returns a dataframe with an index for every county in the us. (5 character string always)

    ['State', 'County', 'PovertyAllAgesPct2012', 'PovertyAllAgesNum2012', 'MedHHInc2012', 'PerCapitaInc0812',
    'PovertyUnder18Num2012', 'PovertyUnder18Pct2012', 'Deep_Pov_All', 'Deep_Pov_Children']

    :return:
    """
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    income = workbook.parse(u"Income")
    return _cleanup_dataframe(income)


def _create_veterans():
    """
    Returns a dataframe with an index for every county in the us. (5 character string always)

    ['State', 'County', 'Vets18OPct', 'GulfWar2VetsPct', 'GulfWar1VetsPct', 'VietnamEraVetsPct', 'KoreanWarVetsPct',
    'WW2VetsPct', 'MaleVetsPct', 'FemaleVetsPct', 'WhiteNonHispVetsPct', 'BlackVetsPct', 'HispanicVetsPct',
    'OtherRaceVetsPct', 'MedianVetsInc', 'LessThanHSVetsPct', 'HighSchOnlyVetsPct', 'SomeCollegeVetsPct',
    'CollegeDegreeVetsPct', 'LFPVetsRate', 'UEVetsRate', 'Vets18ONum', 'CivPop18ONum', 'CivPopVets18to64Num',
    'CLFVets18to64Num', 'MedianNonVetsInc']

    :return:
    """
    rural_atlas_data_10_resource = resources.get_resource(RURAL_ATLAS_DATA__XLS)
    workbook = pd.ExcelFile(rural_atlas_data_10_resource.get_local_path())
    veterans = workbook.parse(u"Veterans")
    return _cleanup_dataframe(veterans)


def _create_contributions():
    """
    Returns a dataframe with index = range(0, ~5 million); each row corresponds to a contribution made

    Columns are: ['cmte_id', 'cand_id', 'cand_nm', 'contbr_nm', 'contbr_city', 'contbr_st', 'contbr_zip',
    'contbr_employer', 'contbr_occupation', 'contb_receipt_amt', 'contb_receipt_dt', 'receipt_desc', 'memo_cd',
    'memo_text', 'form_tp', 'file_num', 'tran_id', 'election_tp', 'clean_zips', 'clean_fips', 'clean_contribution']
    :return:
    """
    contributions_resource = resources.get_resource(CONTRIBUTIONS_CSV)
    # MUST read in *all* as objects. Presumed bug in pandas implementation truncates significant information if any
    # column is read in as something other than object. Ex: a string 0001 becomes 1
    contributions_dataframe = pd.read_csv(contributions_resource.get_local_path(), dtype=object)
    contributions_dataframe[CLEAN_ZIPS] = contributions_dataframe[CONTRIBUTION_ZIP].apply(
        data_cleanup.data_cleanup.get_clean_zip)
    contributions_dataframe[CLEAN_FIPS] = contributions_dataframe[CLEAN_ZIPS].apply(
        data_cleanup.data_cleanup.get_fips_from_zip_code)
    contributions_dataframe[CLEAN_CONTRIBUTION] = contributions_dataframe[CONTRIBUTION_AMOUNT].apply(np.float64)
    return contributions_dataframe


def _create_county_contributions():
    """
    Returns a dataframe with an index for every county in the us. (5 character string always)
    Columns are:
    ['gop_contributions_count', 'dem_contributions_sum', 'gop_contributions_sum', 'dem_contributions_mean',
    'gop_contributions_mean', 'dem_contributions_median', 'gop_contributions_median']

    :return:
    """
    contributions = get_dataframe(CONTRIBUTIONS)
    grouped = contributions.groupby(CLEAN_FIPS)

    contribution_count = grouped.count()[CLEAN_CONTRIBUTION]
    contribution_sum = grouped.sum()[CLEAN_CONTRIBUTION]
    contribution_mean = grouped.mean()[CLEAN_CONTRIBUTION]
    contribution_median = grouped.median()[CLEAN_CONTRIBUTION]

    county_contributions = pd.concat([contribution_count, contribution_sum, contribution_mean, contribution_median],
                                     axis=1)

    county_contributions.columns = [CONTRIBUTION_COUNT, CONTRIBUTION_SUM, CONTRIBUTION_MEAN, CONTRIBUTION_MEDIAN]


    # could also use 'cand_id'
    county_candidate_groups = contributions.groupby([CLEAN_FIPS, CANDIDATE_NAME])[CLEAN_CONTRIBUTION]

    county_candidate_counts = county_candidate_groups.count()
    county_candidate_sums = county_candidate_groups.sum()
    county_candidate_means = county_candidate_groups.mean()
    county_candidate_medians = county_candidate_groups.median()

    # Yes, very ugly implementation.

    def get_dem_contributions_count(clean_fips):
        try:
            return county_candidate_counts[clean_fips][BARACK_OBAMA]
        except KeyError:
            return 0

    def get_gop_contributions_count(clean_fips):
        try:
            return county_candidate_counts[clean_fips][MITT_ROMNEY]
        except KeyError:
            return 0

    def get_dem_contributions_sum(clean_fips):
        try:
            return county_candidate_sums[clean_fips][BARACK_OBAMA]
        except KeyError:
            return 0

    def get_gop_contributions_sum(clean_fips):
        try:
            return county_candidate_sums[clean_fips][MITT_ROMNEY]
        except KeyError:
            return 0

    def get_dem_contributions_mean(clean_fips):
        try:
            return county_candidate_means[clean_fips][BARACK_OBAMA]
        except KeyError:
            return 0

    def get_gop_contributions_mean(clean_fips):
        try:
            return county_candidate_means[clean_fips][MITT_ROMNEY]
        except KeyError:
            return 0

    def get_dem_contributions_median(clean_fips):
        try:
            return county_candidate_medians[clean_fips][BARACK_OBAMA]
        except KeyError:
            return 0

    def get_gop_contributions_median(clean_fips):
        try:
            return county_candidate_medians[clean_fips][MITT_ROMNEY]
        except KeyError:
            return 0

    temp = 'temp'
    county_contributions[temp] = county_contributions.index
    county_contributions[DEM_CONTRIBUTIONS_COUNT] = county_contributions[temp].apply(get_dem_contributions_count)
    county_contributions[GOP_CONTRIBUTIONS_COUNT] = county_contributions[temp].apply(get_gop_contributions_count)
    county_contributions[DEM_CONTRIBUTIONS_SUM] = county_contributions[temp].apply(get_dem_contributions_sum)
    county_contributions[GOP_CONTRIBUTIONS_SUM] = county_contributions[temp].apply(get_gop_contributions_sum)
    county_contributions[DEM_CONTRIBUTIONS_MEAN] = county_contributions[temp].apply(get_dem_contributions_mean)
    county_contributions[GOP_CONTRIBUTIONS_MEAN] = county_contributions[temp].apply(get_gop_contributions_mean)
    county_contributions[DEM_CONTRIBUTIONS_MEDIAN] = county_contributions[temp].apply(get_dem_contributions_median)
    county_contributions[GOP_CONTRIBUTIONS_MEDIAN] = county_contributions[temp].apply(get_gop_contributions_median)
    del county_contributions[temp]
    return county_contributions


def _create_county_statistics():
    """
     Returns a dataframe with an index for every county in the us. (5 character string always)

    Columns:
    ['Age65AndOlderNum2010', 'Age65AndOlderPct2010', 'AsianNonHispanicNum2010', 'AsianNonHispanicPct2010', 'AvgHHSize0812',
    'BlackNonHispanicNum2010', 'BlackNonHispanicPct2010', 'BlackVetsPct', 'CLFVets18to64Num', 'CivPop18ONum',
    'CivPopVets18to64Num', 'CollegeDegreeVetsPct', 'Deep_Pov_All', 'Deep_Pov_Children', 'Ed1LessThanHSNum0812',
    'Ed1LessThanHSPct0812', 'Ed2HSGradOnlyNum0812', 'Ed2HSGradOnlyPct0812', 'Ed3SomeCollegeNum0812',
    'Ed3SomeCollegePct0812', 'Ed4CollegePlusNum0812', 'Ed4CollegePlusPct0812', 'FemaleHHNum0812', 'FemaleHHPct0812',
    'FemaleVetsPct', 'ForeignBornAfricaNum0812', 'ForeignBornAfricaPct0812', 'ForeignBornAsiaNum0812',
    'ForeignBornAsiaPct0812', 'ForeignBornCaribNum0812', 'ForeignBornCaribPct0812', 'ForeignBornCentralSouthAmNum0812',
    'ForeignBornCentralSouthAmPct0812', 'ForeignBornEuropeNum0812', 'ForeignBornEuropePct0812', 'ForeignBornMexNum0812',
    'ForeignBornMexPct0812', 'ForeignBornNum0812', 'ForeignBornPct0812', 'GulfWar1VetsPct', 'GulfWar2VetsPct',
    'HH65PlusAloneNum0812', 'HH65PlusAlonePct0812', 'HighSchOnlyVetsPct', 'HispanicNum2010', 'HispanicPct2010',
    'HispanicPopChangeRate0010', 'HispanicVetsPct', 'KoreanWarVetsPct', 'LFPVetsRate', 'LandAreaSQMiles2010',
    'LessThanHSVetsPct', 'MaleVetsPct', 'MedHHInc2012', 'MedianNonVetsInc', 'MedianVetsInc', 'MultipleRaceNum2010',
    'MultipleRacePct2010', 'MultipleRacePopChangeRate0010', 'NativeAmericanNonHispanicNum2010',
    'NativeAmericanNonHispanicPct2010', 'NaturalChangeNum0010', 'NaturalChangeRate0010', 'NaturalChangeRate1013',
    'NetMigrationNum0010', 'NetMigrationRate0010', 'NetMigrationRate1013', 'NonEnglishHHNum0812', 'NonEnglishHHPct0812',
    'NonHispanicAsianPopChangeRate0010', 'NonHispanicBlackPopChangeRate0010', 'NonHispanicNativeAmericanPopChangeRate0010',
    'NonHispanicWhitePopChangeRate0010', 'NumCivEmployed0812', 'NumCivLaborForce2008', 'NumCivLaborForce2009',
    'NumCivLaborForce2010', 'NumCivLaborForce2011', 'NumCivLaborForce2012', 'NumEmployed2008', 'NumEmployed2009',
    'NumEmployed2010', 'NumEmployed2011', 'NumEmployed2012', 'NumUnemployed2008', 'NumUnemployed2009', 'NumUnemployed2010',
    'NumUnemployed2011', 'NumUnemployed2011.1', 'OtherRaceVetsPct', 'OwnHomeNum0812', 'OwnHomePct0812',
    'PctEmpAgriculture0812', 'PctEmpChange0711', 'PctEmpChange0712', 'PctEmpChange0809', 'PctEmpChange0910',
    'PctEmpChange1011', 'PctEmpChange1012', 'PctEmpGovt0812', 'PctEmpManufacturing0812', 'PctEmpServices0812',
    'PerCapitaInc0812', 'PopChangeRate0010', 'PopChangeRate1013', 'PopDensity2010', 'PovertyAllAgesNum2012',
    'PovertyAllAgesPct2012', 'PovertyUnder18Num2012', 'PovertyUnder18Pct2012', 'SomeCollegeVetsPct', 'TotalHH0812',
    'TotalOccHU0812', 'TotalPop2010', 'TotalPop25Plus0812', 'TotalPopACS0812', 'TotalPopEst2010', 'TotalPopEst2011',
    'TotalPopEst2012', 'TotalPopEst2013', 'TotalPopEstBase2010', 'UEVetsRate', 'Under18Num2010', 'Under18Pct2010',
    'UnempRate2008', 'UnempRate2009', 'UnempRate2010', 'UnempRate2011', 'UnempRate2012', 'Vets18ONum', 'Vets18OPct',
    'VietnamEraVetsPct', 'WW2VetsPct', 'WhiteNonHispVetsPct', 'WhiteNonHispanicNum2010', 'WhiteNonHispanicPct2010',
    'contribution_count', 'contribution_mean', 'contribution_median', 'contribution_sum', 'contributions_per_capita',
    'dem_contributions_count', 'dem_contributions_mean', 'dem_contributions_median', 'dem_contributions_sum', 'dem_votes',
    'gop_contributions_count', 'gop_contributions_mean', 'gop_contributions_median', 'gop_contributions_sum', 'gop_votes',
    'percent_vote_dem', 'percent_vote_gop', 'total_votes', 'winner_name', 'winner_party']

    :return:
    """
    votes = get_dataframe(VOTES)
    county_contributions = get_dataframe(COUNTY_CONTRIBUTIONS)
    county_contributions = county_contributions[np.float64(county_contributions.index) > 0]
    jobs = get_dataframe(JOBS)
    income = get_dataframe(INCOME)
    people = get_dataframe(PEOPLE)
    veterans = get_dataframe(VETERANS)

    county_statistics = pd.concat([votes, county_contributions, jobs, income, people, veterans], axis=1)
    county_statistics = county_statistics[pd.notnull(county_statistics[TOTAL_VOTES])]
    county_statistics = county_statistics[pd.notnull(county_statistics[CONTRIBUTION_COUNT])]
    county_statistics = county_statistics[pd.notnull(county_statistics[POPULATION_2012])]
    county_statistics[CONTRIBUTIONS_PER_CAPITA] = np.true_divide(county_statistics[CONTRIBUTION_COUNT],
                                                                 county_statistics[POPULATION_2012])
    county_statistics = county_statistics.reindex_axis(sorted(county_statistics.columns), axis=1)
    return county_statistics


def _create_map_data():
    county_statistics = get_dataframe(COUNTY_STATISTICS)
    county_statistics['clean_fips'] = county_statistics.index

    def do_keep(fips):
        if len(fips) != 5:
            return False
        elif fips[-3:] == "000":
            return False
        return True
    county_statistics['do_keep'] = county_statistics['clean_fips'].apply(do_keep)
    # Keep only ones we want to keep
    county_statistics = county_statistics[county_statistics['do_keep']]


    percentages = [str(column_name) for column_name in county_statistics.columns if "Pct" in str(column_name)]
    rates = [str(column_name) for column_name in county_statistics.columns if "Rate" in str(column_name)]

    pre_sort = sorted(percentages + rates)

    populations = county_statistics['TotalPopEst2013']
    lower = populations.quantile(.04)
    upper = populations.quantile(.88)

    def _get_normalized_pop(pop):
        return (pop - lower) / (upper - lower)

    inds = [i / 100.0 for i in range(10, 110, 10)]
    bins = [populations.quantile(i / 100.0) for i in range(0, 110, 10)]

    def get_normalized_pop(pop):
        for i in range(0, len(bins) - 1):
            bin = bins[i]
            next = bins[i+1]
            if bin < pop < next:
                return inds[i]
        return .99


    county_statistics['normalized_population'] = county_statistics['TotalPopEst2013'].apply(get_normalized_pop)
    customs = ['contributions_per_capita', 'percent_vote_dem', 'percent_vote_gop', 'normalized_population']
    to_keep = customs + pre_sort
    map_data = county_statistics[to_keep].copy()
    return map_data


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
        DataFrameWrapper(COUNTY_CONTRIBUTIONS, COUNTY_CONTRIBUTIONS_SERIALIZED_NAME, _create_county_contributions),
        DataFrameWrapper(COUNTY_STATISTICS, COUNTY_STATISTICS_SERIALIZED_NAME, _create_county_statistics),
        DataFrameWrapper(MAP_DATA, MAP_DATA_SERIALIZED_NAME, _create_map_data)
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
    # df = get_dataframe(COUNTY_STATISTICS)
    df = _create_map_data()
    print df.head(30)
    #print len(df)
    #print df.index
    #print list(df.columns)


if __name__ == "__main__":
    debug()