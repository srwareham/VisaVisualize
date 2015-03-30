import csv
import pandas as pd
import matplotlib.pyplot as pyplot
import numpy as np
from scipy import stats

file_path = 'P00000001-ALL.csv'

dataframe = pd.read_csv(file_path)

state_group_contrib = dataframe.groupby(['contbr_st'])['contb_receipt_amt'].mean()

state_group_contrib.to_csv('contrib_by_state.csv')

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
    
print_full(state_group_contrib)