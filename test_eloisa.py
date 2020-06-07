from tqdm import tqdm
import pandas as pd
import numpy as np
import seaborn as sns

from backend import get_cmte_scorecard, load_df_from_openFEC, compute_candidate_overall_score, split_donations

pbar = tqdm(leave=False)

# Load open FEC data
pbar.reset(total=4)
pbar.set_description("Loading datafiles")

# donations_df = load_df_from_openFEC(
#     "https://www.fec.gov/files/bulk-downloads/2020/pas220.zip", "itpas2.txt",
#     "https://www.fec.gov/files/bulk-downloads/data_dictionaries/pas2_header_file.csv")
# pbar.update()
#
# cmte_df = load_df_from_openFEC(
#     "https://www.fec.gov/files/bulk-downloads/2020/cm20.zip", "cm.txt",
#     "https://www.fec.gov/files/bulk-downloads/data_dictionaries/cm_header_file.csv")
# cmte_df = cmte_df.set_index('CMTE_ID')
# pbar.update()
#
# cand_df = load_df_from_openFEC(
#     "https://www.fec.gov/files/bulk-downloads/2020/cn20.zip", "cn.txt",
#     "https://www.fec.gov/files/bulk-downloads/data_dictionaries/cn_header_file.csv")
# cand_df = cand_df.set_index('CAND_ID')
# pbar.update()

scorecard_file = './congressional_scorecards/complete_scorecard.csv'
scorecard_df = pd.read_csv(scorecard_file, sep=",", header=0, low_memory=False, index_col=3)
# scorecard_df.drop(['candidate_score'])

# ## Store to pickle
# donations_df.to_pickle('pickle/donations_df.pkl')
# cmte_df.to_pickle('pickle/cmte_df.pkl')
# cand_df.to_pickle('pickle/cand_df.pkl')
# scorecard_df.to_pickle('pickle/scorecard_df.pkl')

pbar.update()
pbar.close()

## Load from pickle
donations_df = pd.read_pickle('pickle/donations_df.pkl')
cmte_df = pd.read_pickle('pickle/cmte_df.pkl')
cand_df = pd.read_pickle('pickle/cand_df.pkl')
# scorecard_df = pd.read_pickle('pickle/scorecard_df.pkl')

## Do other stuff
# def get_cmte_scorecard():
#     num_possible_scores = 3
#     scorecard_df['candidate_score'] = \
#         sum(scorecard_df['2017_aclu_score', '2019_environment_score', '2017_naacp_score']) \
#         / (num_possible_scores - sum(
#             scorecard_df['2017_aclu_score', '2019_environment_score', '2017_naacp_score'].isna()))
#     return scorecard_df
#
# scorecard_df = get_cmte_scorecard()

cmte_id = 'C00360354'
cmte_scorecard = get_cmte_scorecard(cmte_id, donations_df, cand_df, scorecard_df)

[new_cand_scorecard, existing_cand_scorecard] = split_donations(cmte_scorecard)
existing_cand_scorecard = compute_candidate_overall_score(existing_cand_scorecard)

existing_cand_scorecard = existing_cand_scorecard.sort_values(by=['CAND_OFFICE','candidate_score','CAND_OFFICE_ST','CAND_NAME'])
new_cand_scorecard = new_cand_scorecard.sort_values(by=['CAND_OFFICE','CAND_OFFICE_ST','CAND_NAME'])

# Styling function
def format_score(val):
    import math
    if math.isnan(val):
        return ''
    else:
        return '{v:.1f}%'.format(v=val * 100)

existing_cand_scorecard = existing_cand_scorecard.reset_index(drop=True)

existing_cand_scorecard[['2017_aclu_score','2019_environment_score', '2017_naacp_score']] = existing_cand_scorecard[['2017_aclu_score','2019_environment_score', '2017_naacp_score']] * 100

display_columns = ['CAND_NAME', 'CAND_OFFICE_ST','CAND_OFFICE','TRANSACTION_AMT','candidate_score', '2017_aclu_score',
                   '2019_environment_score', '2017_naacp_score']

existing_cand_scorecard = existing_cand_scorecard.rename(columns={"CAND_NAME": "Candidate Name", "CAND_OFFICE_ST": "State","TRANSACTION_AMT": "Total Donation Amount","candidate_score": "Overall Voting Score", "2017_aclu_score":"2017 ACLU Score","2019_environment_score":"2019 LCV Score", "2017_naacp_score":"2017 NAACP Score"})
cm = sns.light_palette("green", as_cmap=True)

display_columns = ["Candidate Name", "State","Total Donation Amount","Overall Voting Score", "2017 ACLU Score","2019 LCV Score", "2017 NAACP Score"]

print_df = existing_cand_scorecard[display_columns]
#print_df[['2017_aclu_score', '2019_environment_score', '2017_naacp_score']] = print_df[['2017_aclu_score', '2019_environment_score', '2017_naacp_score']].applymap(format_score)

# .format("{:.1f}%",  subset=['2017_aclu_score','2019_environment_score', '2017_naacp_score'], na_rep=' ') \
# .format("{:.1f}%",  subset=['candidate_score'], na_rep=' ') \
# .format("$ {:.0f}", subset=['TRANSACTION_AMT']) \

html = print_df.style\
    .format("{:.1f}%", subset=['2017 ACLU Score', '2019 LCV Score', '2017 NAACP Score'], na_rep=' ') \
    .format("{:.1f}%", subset=['Overall Voting Score'], na_rep=' ') \
    .format("${:.0f}", subset=['Total Donation Amount']) \
    .background_gradient(cmap=cm)\
    .render()
#
Html_file = open("table.html", "w")
Html_file.write(html)
Html_file.close()


#print(cmte_scorecard[display_columns])

pass
