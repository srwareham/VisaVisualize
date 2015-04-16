import pandas as pd
import numpy as np
import csv
from context import campaignadvisor
from sklearn import preprocessing

#def get_normalizer():
#    return Normalizer(algorithm='linear')

class Normalizer:
	def __init__(self, df):
		self.df = df

def normalize(df, feature):
    result = df.copy()
    max_val = df[feature].max()
    min_val = df[feature].min()
    result[feature] = (df[feature] - min_val) / (max_val - min_val)
    return result

#def normalize(col, algorithm='lin'):
#	pd.Series()

def main():
	df = pd.DataFrame({'a': [2, 4, 5], 'b': [3, 9, 4]}, dtype=np.float)
	
	print(df)
	
	x = df.values #returns a numpy array
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(x)
	print(pd.DataFrame(x_scaled))
	
	for feature in df.columns:
		print(normalize(df, feature))

if __name__ == "__main__":
    main()


"""
County statistics dataframe (normalize)
import pandas
import python library alg

setup: vote_holder.py
example:
	def normalize(col, algorithm='lin'):
		input: series
		output: series
main: normalized = normalize[votes['dem_votes']]

conform min=0 and max=1 column by column

check if column min and max equals the global MIN and global MAX

ignore clean_fps column
# round function to approximate to closest tenths value

Normalization algorithm (linear, logarithmic,) --> expressed as a parameter
"""