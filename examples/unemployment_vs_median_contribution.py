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


if __name__ == "__main__":
    df_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    county_statistics = campaignadvisor.dataframe_holder.get_dataframe(df_name)
    plot_columns(county_statistics, 'UnempRate2012', 'contribution_mean')