from context import campaignadvisor


def get_state(fips_code):
    state_fips = fips_code[:2]
    return campaignadvisor.data_cleanup.get_state_from_fips(state_fips)


def get_states_per_capita(county_statistics):
    county_statistics['clean_fips'] = county_statistics.index
    county_statistics['state'] = county_statistics['clean_fips'].apply(get_state)
    states = county_statistics.groupby('state')[['contribution_count', 'contribution_sum', 'TotalPopEst2013']].sum()
    states['contribution_per_capita'] = states['contribution_sum'] / states['TotalPopEst2013']
    rankings = [str(s) for s in states.sort(columns='contribution_per_capita', ascending=False).index]
    # Ignore territories and nulls
    return rankings[:-6]


def run_county_statistics_examples():
    county_statistics_name = campaignadvisor.dataframe_holder.COUNTY_STATISTICS
    county_statistics = campaignadvisor.dataframe_holder.get_dataframe(county_statistics_name)
    state_rankings = get_states_per_capita(county_statistics)
    print state_rankings


def main():
    run_county_statistics_examples()

if __name__ == "__main__":
    main()