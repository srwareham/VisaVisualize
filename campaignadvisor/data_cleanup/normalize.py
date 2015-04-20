import pandas as pd
import numpy as np
from sklearn import preprocessing


class Normalizer():
    MIN_VAL = 0
    MAX_VAL = 1

    """
    input: Series
    output: Series
    """

    def __init__(self, df, alg="minmax"):
        self.df = df
        self.alg = alg

    # algorithm types =
    # 'minmax' is rescaling,
    # 	'std' is standardization,
    #	'unit' is scaling to unit length

    def __repr__(self):
        return self.df

    def normalize_minmax(self, feature):
        self.MAX_VAL = self.df[feature].max()
        self.MIN_VAL = self.df[feature].min()
        feature_minmax = feature + '_minmax'
        self.df[feature_minmax] = (self.df[feature] - self.MIN_VAL) / (self.MAX_VAL - self.MIN_VAL)

    # return self.df[feature_minmax]

    def normalize_std(self, feature):
        feature_zscore = feature + '_zscore'
        self.df[feature_zscore] = (self.df[feature] - self.df[feature].mean()) / self.df[feature].std(ddof=0)

    # return self.df[feature_zscore]

    def normalize(self, feature):
        # check if column min and max equals the global min and max
        if self.MAX_VAL == self.df[feature].max() and self.MIN_VAL == self.df[feature].min():
            return True
        if self.alg == 'minmax':
            self.normalize_minmax(feature)
        elif self.alg == 'std':
            self.normalize_std(feature)


def main():
    """
    jobs_name = campaignadvisor.dataframe_holder.JOBS
    votes_name = campaignadvisor.dataframe_holder.VOTES
    jobs = campaignadvisor.dataframe_holder.get_dataframe(jobs_name)
    votes = campaignadvisor.dataframe_holder.get_dataframe(votes_name)
    votes['clean_fips'] = votes['fips_code']

    # country statistics dataframe
    df = pd.merge(votes, jobs, on='clean_fips', sort=False, how="inner")
    """

    # example dataframe
    df = pd.DataFrame({'a': [2, 4, 5], 'b': [3, 9, 4]}, dtype=np.float)
    print(df)

    # get feature list
    features_to_scale = list(df.columns)
    for feature in df.columns:
        if feature == 'clean_fps' or feature == 'fips_code':
            features_to_scale.remove(feature)

    # instantiate Normalizer object with given algorithm
    df_scaled = Normalizer(df, alg='minmax')

    # normalize only features to be scaled
    for feature in features_to_scale:
        df_scaled.normalize(feature)

    # testing
    print df_scaled.df
    print test_normalize(df, features_to_scale, alg='minmax')


def test_normalize(df, features, alg):
    if alg == 'minmax':
        scale = preprocessing.MinMaxScaler().fit(df[features])
    elif alg == 'std':
        scale = preprocessing.StandardScaler().fit(df[features])
    df_scaled = scale.transform(df[features])
    return df_scaled


if __name__ == "__main__":
    main()