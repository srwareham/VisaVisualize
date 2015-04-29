from context import campaignadvisor


def get_state(fips_code):
    state_fips = fips_code[:2]
    return campaignadvisor.data_cleanup.get_state_from_fips(state_fips)


def get_leading_states(contributions):
    """
    Return state contributions, names as lists in descending order of contribution amount
    :param contributions:
    :return:
    """
    contributions['state'] = contributions['clean_fips'].apply(get_state)
    states = contributions.groupby('state')
    state_sums = states.sum()
    ordered_sums = state_sums.sort('clean_contribution', ascending=False)['clean_contribution']
    names = list(ordered_sums.index)
    values = list(ordered_sums)
    unwanted = ['NO_STATE_NAME', 'american samoa',
                    'northern mariana islands', 'guam', 'virgin islands', 'puerto rico']
    state_contributions = []
    state_names = []
    for i in range(0, len(values)):
        amount = values[i]
        name = names[i]
        if name not in unwanted:
            state_contributions.append(amount)
            state_names.append(name)

    return state_contributions, state_names


def find_top_n_state_influence(n, contributions):
    """
    Print the n top contributing states and they percent they contributed
    :param n:
    :param contributions:
    :return:
    """
    state_contributions, state_names = get_leading_states(contributions)
    total = sum(state_contributions)
    percent = sum(state_contributions[:n]) * 1.0 / total

    print str("{0:.2f}".format(percent * 100)) + "% " "of campaign finances came from the " + str(n) + " states:"
    print " ".join(state_names[:n])


def get_state_bins(contributions):
    state_contributions, state_names = get_leading_states(contributions)
    total = sum(state_contributions)

    def get_dict(lower=0, upper=len(state_names)):
        return {'states': state_names[lower:upper], 'percent': 1.0 * sum(state_contributions[lower:upper]) / total}

    bins = [get_dict(lower=0, upper=6),
            get_dict(lower=6, upper=16),
            get_dict(lower=16, upper=26),
            get_dict(lower=26, upper=51)]
    return bins, total


def get_pie(contributions):
    try:
        import matplotlib.pyplot as pyplot
    except ImportError:
        print "no matplotlib :("
        return
    bins, total = get_state_bins(contributions)
    vals = []
    names = range(0, 4)
    for dic in bins:
        vals.append(dic['percent'] * total)

    pyplot.pie(vals, labels=names, autopct="%1.1f%%")
    pyplot.show()


def run_contributions_examples():
    """
    Run examples that use the contributions resource
    :return:
    """
    contributions_name = campaignadvisor.dataframe_holder.CONTRIBUTIONS
    contributions = campaignadvisor.dataframe_holder.get_dataframe(contributions_name)
    find_top_n_state_influence(6, contributions)
    get_pie(contributions)


def main():
    run_contributions_examples()

if __name__ == "__main__":
    main()