import pandas as pd
import csv

# TODO: Look out for circular reference
from context import campaignadvisor


# npid = national politician id
class Politician():
    def __init__(self, npid, first_name, last_name, party):
        self.id = npid
        self.first_name = first_name
        self.last_name = last_name
        self.party = party

    def __repr__(self):
        return self.first_name + " " + self.last_name + " (" + self.party + ")"


class Outcome:
    def __init__(self, did_win, num_votes):
        self.did_win = did_win
        self.num_votes = num_votes

    def __repr__(self):
        result = "Lose"
        if self.did_win:
            result = "Win"
        return result + " with " + str(self.num_votes) + " votes"


class CountyResult():
    def __init__(self, fips_code, total_votes, candidate_outcomes):
        self.fips_code = fips_code
        self.total_votes = total_votes
        self.candidate_outcomes = candidate_outcomes

    def __repr__(self):
        return self.fips_code + ": " + str(self.get_winner())

    def get_winner(self):
        for candidate in self.candidate_outcomes:
            outcome = self.candidate_outcomes[candidate]
            candidate_won = outcome.did_win
            if candidate_won:
                return candidate

    def get_winning_votes(self):
        """
        Return the number of votes the winner recieved
        :return:
        """
        try:
            votes = self.get_winner().votes
        except ValueError:
            votes = -1
        return votes

    def get_party_votes(self, party_name):
        """
        Returns the number of votes a particular party got.

        If multiple people were allowed to run under the same party name, the sum of both is returned
        :param party_name:
        :return:
        """
        votes = 0
        for candidate, outcome in self.candidate_outcomes.iteritems():
            if candidate.party == party_name:
                votes += outcome.num_votes
        return votes


# Turn a row into a map of relevant values, add this map to the argument map with the key fips_code
def process_row(county_results, row, fields):
    cell_list = [cell for cell in row]
    # state_abbreviation = str(cell_list[0])
    dirty_fips_code = cell_list[3]
    fips_code = campaignadvisor.data_cleanup.get_clean_fips(dirty_fips_code)
    try:
        # total_precincts = int(cell_list[8])
        total_votes = int(cell_list[10])
    # TODO: Throw out row if any value fails
    except ValueError:
        # total_precincts = 0
        total_votes = 0
        raise

    candidates_outcomes = {}
    for index in range(0, len(cell_list)):
        cell = cell_list[index]
        field_name = fields[index]
        if field_name == "Order":
            # Ignore blank cells
            try:
                int(cell)
            except ValueError:
                continue

            candidate_party = str(cell_list[index+1])
            first_name = str(cell_list[index+2])
            last_name = str(cell_list[index+4])
            candidate_votes = int(cell_list[index+8])
            candidate_won = str(cell_list[index+9]) == "X"
            politician_id = int(cell_list[index+10])

            politician = Politician(politician_id, first_name, last_name, candidate_party)
            outcome = Outcome(candidate_won, candidate_votes)

            # Should never be the case, but we check nonetheless
            if politician not in candidates_outcomes:
                candidates_outcomes[politician] = outcome

    county_result = CountyResult(fips_code, total_votes, candidates_outcomes)
    county_results[fips_code] = county_result


def get_county_results_dict():
    # Get votes
    votes_resource = campaignadvisor.resources.get_resource("2012_president_county_votes.csv")
    row_number = 0
    fields = []
    county_votes_dict = {}
    with votes_resource.get_file() as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row_number == 0:
                fields = [field for field in row]
            else:
                process_row(county_votes_dict, row, fields)
            row_number += 1
    return county_votes_dict


def get_county_dataframe():
    county_results_dict = get_county_results_dict()
    data = []

    # TODO: change to use gets so can return nulls
    for county, result in county_results_dict.iteritems():
        fips_code = result.fips_code
        total_votes = result.total_votes
        gop_votes = result.get_party_votes("GOP")
        dem_votes = result.get_party_votes("Dem")
        winner = result.get_winner()
        winner_name = winner.first_name + " " + winner.last_name
        winner_party = winner.party
        data.append([fips_code, total_votes, gop_votes, dem_votes, winner_name, winner_party])
    header = ["clean_fips", "total_votes", "gop_votes", "dem_votes", "winner_name", "winner_party"]
    df = pd.DataFrame(data, columns=header)
    df['percent_vote_gop'] = df['gop_votes'] / df['total_votes']
    df['percent_vote_dem'] = df['dem_votes'] / df['total_votes']
    return df


def debug():
    print get_county_dataframe()

if __name__ == "__main__":
    debug()

