import numpy as np
import pandas as pd
from context import campaignadvisor

"""
Contribution classification by quartile population size buckets
"""

def get_state_county(fips_code):
    return campaignadvisor.data_cleanup.get_state_county_from_fips(fips_code)

def get_population_series(county_statistics):
	#return county_statistics['CivPop18ONum']
	return county_statistics['TotalPopEst2013']

def get_bins(serie, num_buckets):
	bucket_size = (serie.max()-serie.min())/num_buckets
	bucket_list = []
	for n in range(0, num_buckets+1):
		bucket_list.append(n*bucket_size)
	return bucket_list

def run_county_statistics_examples(num_buckets=4):
	county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
	county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)

	#counts, bins = np.histogram(get_population_series(county_statistics))	
	serie = get_population_series(county_statistics)
	#bins = get_bins(serie, num_buckets)
	#counts, division = np.histogram(serie, bins = bins)
	#print pd.Series(counts, index=division[:-1])

	print serie.groupby(pd.cut(serie,num_buckets)).count()

	# percentages
	serie_pct = serie.value_counts(normalize=True, bins=num_buckets)
	print serie_pct
	
def main():
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)
    pops = county_statistics['CivPop18ONum']

    """
    tiny:
    1 - 4078
    small:
    4078 - 50000
    medium:
    50000 - 100000
    large:
    10000 - 691487
    huge:
    691487+
    """

    def get_county_size(population_size):
        tiny_ceiling = pops.quantile(.10)
        small_ceiling = 40000
        medium_ceiling = 100000
        large_ceiling = pops.quantile(.97)

        if population_size <= 0:
            return -1
        elif 0 < population_size <= tiny_ceiling:
            return "tiny"
        elif tiny_ceiling < population_size <= small_ceiling:
            return "small"
        elif small_ceiling < population_size <= medium_ceiling:
            return "medium"
        elif medium_ceiling < population_size <= large_ceiling:
            return "large"
        else:
            return "huge"

    county_size_type = "county_size_type"
    county_statistics[county_size_type] = county_statistics['CivPop18ONum'].apply(get_county_size)

    by_size = county_statistics.groupby(county_size_type)

    total = county_statistics['contribution_sum'].sum()

    print "Counts:"
    print by_size['contribution_sum'].count()
    print
    print "Contribution Percentages:"
    print by_size['contribution_sum'].sum() / total


if __name__ == "__main__":
    main()
