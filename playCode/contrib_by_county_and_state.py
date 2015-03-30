import csv
import pandas as pd
import matplotlib.pyplot as pyplot
import numpy as np
from scipy import stats
import sys
sys.path.append('../data_cleanup') 
import data_cleanup as dc

file_path = '../data/P00000001-ALL.csv'

dataframe = pd.read_csv(file_path)

dataframe['contrb_county'] = dataframe['contbr_zip'].apply(dc.get_county)
county_state_group_contrib = dataframe.groupby(['contbr_st','contrb_county'])['contb_receipt_amt'].mean()

county_state_group_contrib.to_csv('contrib_by_county_and_state.csv')

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
    
print_full(state_group_contrib)