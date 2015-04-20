import pandas as pd
import numpy as np
import csv
from context import campaignadvisor
from sklearn import preprocessing


class Normalizer():
	MIN_VAL = 0
	MAX_VAL = 1

	"""
	input: Series
	output: Series
	"""

	def __init__(self, df, feature, alg):
		self.df = df
		self.alg = alg
		self.feature = feature
		# algorithm types =
		# 'minmax' is rescaling,
		# 'std' is standardization,
		# 'unit' is scaling to unit length

	def print_normalization(self):
		if self.alg == 'minmax':
			return normalize_minmax()
		elif self.alg == 'std':
			return normalize_std()
		else:
			return self.df

	def normalize_minmax(self, feature):
		self.MAX_VAL = self.df[feature].max()
		self.MIN_VAL = self.df[feature].min()
		feature_minmax = feature + '_zscore'
		self.df[feature_minmax] = (self.df[feature] - self.MIN_VAL) / (self.MAX_VAL - self.MIN_VAL)
		return self.df

	def normalize_std(self, feature):
		feature_zscore = feature + '_zscore'
		self.df[featire_zscore] = (self.df[feature] - self.df[feature].mean())/self.df[feature].std(ddof=0)
		return self.df

	# check if column min and max equals the global min and max
	def is_normalized(self, feature):
		if self.MAX_VAL != self.df[feature].max() and self.MIN_VAL != self.df[feature].min():
			return False
		return True

def main():
	"""
	jobs_name = campaignadvisor.dataframe_holder.JOBS
    votes_name = campaignadvisor.dataframe_holder.VOTES
    jobs = campaignadvisor.dataframe_holder.get_dataframe(jobs_name)
    votes = campaignadvisor.dataframe_holder.get_dataframe(votes_name)
    votes['clean_fips'] = votes['fips_code']

    county_statistics = pd.merge(votes, jobs, on='clean_fips', sort=False, how="inner")
	"""

	# example dataframe
	df = pd.DataFrame({'a': [2, 4, 5], 'b': [3, 9, 4]}, dtype=np.float)
	print(df)
	
	# get feature list
	features_to_scale = list(df.columns)
	for feature in df.columns:
		if feature == 'clean_fps' or feature == 'fips_code':
			features_to_scale.remove(feature)

	# instantiate Normalizer object
	n = Normalizer(df, alg='minmax')

	print test_normalize(df, features_to_scale, alg='minmax')
	
	for feature in features_to_scale:
		print n

def test_normalize(df, features, alg):
	if alg == 'minmax':
		scale = preprocessing.MinMaxScaler().fit(df[features])
	elif self.alg == 'std':
		scale = preprocessing.StandardScaler().fit(df[features])
	df_scaled = scale.transform(df[features])
	return df_scaled

if __name__ == "__main__":
    main()

"""
County statistics dataframe (normalize)

example:
	def normalize(col, algorithm='lin'):
		input: series
		output: series

ignore clean_fps column
# round function to approximate to closest tenths value

Normalization algorithm (linear, logarithmic,) --> expressed as a parameter
"""