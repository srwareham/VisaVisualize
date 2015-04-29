from context import campaignadvisor


def print_candidate_contribution_stats(contributions):
    def print_candidate(candidate):
        relevant = contributions[contributions['cand_nm'] == candidate]['clean_contribution']
        print "Statistics for contributions for:", candidate
        print "Number of contributions:", relevant.count()
        print "Contribution sum:", relevant.sum()
        print "Mean Contribution:", relevant.mean()
        print "Median Contribution:", relevant.median()
        print "Contribution standard deviation:", relevant.std()

    print_candidate("Obama, Barack")
    print
    print_candidate("Romney, Mitt")


def run_contributions_examples():
    contributions_name = campaignadvisor.dataframe_holder.CONTRIBUTIONS
    contributions = campaignadvisor.dataframe_holder.get_dataframe(contributions_name)
    print_candidate_contribution_stats(contributions)


def main():
    run_contributions_examples()

if __name__ == "__main__":
    main()