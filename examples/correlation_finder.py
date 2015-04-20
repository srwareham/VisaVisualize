from context import campaignadvisor
import pandas as pd
import matplotlib.pyplot as pyplot


def plot_columns(df, x_column, y_column):
    df.plot(kind='scatter', x=x_column, y=y_column, logx=True)
    pyplot.show()


def get_correlated_fields(df, field_name, ignored_fields=None, ignore_field_name=True):
    if ignored_fields is None:
        ignored_fields = []
    if ignore_field_name:
        ignored_fields.append(field_name)
    corr = df.corr()
    series = corr[field_name]
    findings = [(str(index), series[index]) for index in series.index if index not in ignored_fields]
    findings = sorted(findings, key=lambda tup: abs(tup[1]), reverse=True)
    return findings


def print_correlated_fields(df, field_name, ignored_fields=None, ignore_field_name=True):
    """
    Print the county features that are most correlated to the given field name
    Sorts by absolute value

    :param df: Dataframe containing columns
    :param field_name: Column name to compare against
    :param ignored_fields: Column names to exclude from comparison
    :return:
    """
    tups = get_correlated_fields(df, field_name, ignored_fields=ignored_fields, ignore_field_name=ignore_field_name)
    rank = 1
    print "Most correlated features for \"", field_name + "\":"
    if ignored_fields != None:
        print "  Ignoring fields:", ignored_fields
    print
    for tup in tups:
        print str(rank) + ".)", tup[0], ":", tup[1]
        rank += 1


def main():
    pd.options.display.max_rows = 1000
    county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)
    county_statistics.index = county_statistics['clean_fips']
    county_statistics['contributions_per_capita'] = county_statistics['contributions_count'] * 1.0 / county_statistics['TotalPopEst2012']


    dependent_variable = "clean_contribution_median"
    print_correlated_fields(county_statistics, dependent_variable, ignored_fields=['clean_contribution_mean'])

if __name__ == "__main__":
    main()