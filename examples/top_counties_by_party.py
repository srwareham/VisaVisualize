from context import campaignadvisor


def get_state_county(fips_code):
    return campaignadvisor.data_cleanup.get_state_county_from_fips(fips_code)


def pretty_print(series):
    rank = 1
    for index in series.index:
        print str(rank) + ".)", get_state_county(index), series.loc[index]
        rank += 1


def print_top_counties(county_statistics):
    """
    Print which counties contributed the most to each party. Both in terms of counts of contributions,
    and total $ amount.
    :param county_statistics:
    :return:
    """
    to_keep = 20
    most_gop_count = county_statistics.sort('gop_contributions_count', ascending=False)['gop_contributions_count'].head(to_keep)
    most_gop_sum = county_statistics.sort('gop_contributions_sum', ascending=False)['gop_contributions_sum'].head(to_keep)

    # In one but not the other
    #print set(most_gop_count.index).difference(most_gop_sum.index)
    most_dem_count = county_statistics.sort('dem_contributions_count', ascending=False)['dem_contributions_count'].head(to_keep)
    most_dem_sum = county_statistics.sort('dem_contributions_sum', ascending=False)['dem_contributions_sum'].head(to_keep)

    print "DEM:"
    print "Count:"
    pretty_print(most_dem_count)
    print "Sum:"
    pretty_print(most_dem_sum)
    print "GOP:"
    print "Count:"
    pretty_print(most_gop_count)
    print "Sum:"
    pretty_print(most_gop_sum)


def run_county_statistics_examples():
    county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)
    print_top_counties(county_statistics)


def main():
    run_county_statistics_examples()

if __name__ == "__main__":
    main()