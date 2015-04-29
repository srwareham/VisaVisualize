from context import campaignadvisor


def print_top_contributors(contributions):
    # NOTE: not broken down by party
    contributions['unique'] = contributions['contbr_nm'] + " " + contributions['contbr_zip']
    unique_contributor_group = contributions.groupby('unique')
    contributor_sums = unique_contributor_group.sum()
    contributor_counts = unique_contributor_group.count()

    to_keep = 15

    print "Top " + str(to_keep) + " contributors by count"
    print contributor_counts.sort('clean_contribution', ascending=False).head(to_keep)['clean_contribution']
    print
    print "Top " + str(to_keep) + " contributors by $"
    print contributor_sums.sort('clean_contribution', ascending=False).head(to_keep)


def run_contributions_examples():
    contributions_name = campaignadvisor.dataframe_holder.CONTRIBUTIONS
    contributions = campaignadvisor.dataframe_holder.get_dataframe(contributions_name)
    print_top_contributors(contributions)


def main():
    run_contributions_examples()

if __name__ == "__main__":
    main()