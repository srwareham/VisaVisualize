import pandas as pd
import numpy as np
import matplotlib.pyplot as pylot

from context import campaignadvisor

"""
Plots the unemployment rate of counties versus the median contribution in it.
Only counties with both fields are shown.
"""


def print_dataframe_fingerprint(df, name=""):
    print "DataFrame " + name + ":"
    print "Size:", len(df)
    print "Columns:", df.columns
    print "Index:", df.index
    pass


def plot_columns(df, x_column, y_column):
    df.plot(kind='scatter', x=x_column, y=y_column)
    pylot.show()


def main():
    jobs_name = campaignadvisor.dataframe_holder.JOBS
    votes_name = campaignadvisor.dataframe_holder.VOTES
    jobs = campaignadvisor.dataframe_holder.get_dataframe(jobs_name)
    votes = campaignadvisor.dataframe_holder.get_dataframe(votes_name)
    votes['clean_fips'] = votes['fips_code']

    county_statistics = pd.merge(votes, jobs, on='clean_fips', sort=False, how="inner")
    print_dataframe_fingerprint(county_statistics)
    plot_columns(county_statistics, 'UnempRate2012', 'total_votes')


if __name__ == "__main__":
    main()