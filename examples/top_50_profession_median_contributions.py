"""
Find the top 50 most frequently occurring professions in the contributions database (using a very coarse approach)
Find the median contribution for each of these professions, print as a list of tuples in descending order.
"""
from collections import Counter
import numpy as np
from context import campaignadvisor
contributions_name = campaignadvisor.dataframe_holder.CONTRIBUTIONS
contributions = campaignadvisor.dataframe_holder.get_dataframe(contributions_name)

occupation_counter = Counter(contributions['contbr_occupation'])

professions = [profession_tuple[0] for profession_tuple in occupation_counter.most_common(59)]

professions.remove(np.NaN)
professions.remove("INFORMATION REQUESTED")
professions.remove("INFORMATION REQUESTED PER BEST EFFORTS")
professions.remove("ATTORNEY")
professions.remove("REGISTERED NURSE")
professions.remove("RN")
professions.remove("SMALL BUSINESS OWNER")
professions.remove("OWNER")
professions.remove("NOT-EMPLOYED")


grouped = contributions.groupby('contbr_occupation')
median = grouped.median()

profession_median_contributions = []
for profession in professions:
    if profession is np.NaN:
        continue
    median_contribution = median['clean_contribution'][profession]
    print median_contribution, profession
    profession_median_contributions.append((profession, median_contribution))

print sorted(profession_median_contributions, key=lambda x: x[1], reverse=True)