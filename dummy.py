import csv
import pandas as pd
import matplotlib.pyplot as pyplot
import numpy as np
from scipy import stats


file_path = 'H1B_efile_FY02.txt'
df = pd.read_csv(file_path)
df3 = df[['WAGE_RATE_1','JOB_CODE']]
df3 = df3[~((df3-df3.mean()).abs()>3*df3.std())]
df3.plot(kind='scatter', x='WAGE_RATE_1', y='JOB_CODE')
pyplot.show()