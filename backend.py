import pandas as pd
import numpy as np

def load_df_from_openFEC(zip_url, zip_file, header_url):
    from io import BytesIO
    from urllib.request import urlopen
    from zipfile import ZipFile

    columns = []
    # Load header data
    with urlopen(header_url) as headresp:
        df = pd.read_csv(BytesIO(headresp.read()), sep=',', header=None)
        columns = df.iloc[0].to_list()

    # Load contents
    with urlopen(zip_url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            df = pd.read_csv(zfile.open(zip_file), sep="|", header=None, low_memory=False, names=columns)
            return df

def count_num_cand_votes(scorecard_df):
    return scorecard_df[['2017_aclu_score', '2019_environment_score', '2017_naacp_score']].count(axis=1)

def split_donations(cmte_scorecard):
    how_many_votes = count_num_cand_votes(cmte_scorecard)
    new_candidates_df = cmte_scorecard[how_many_votes == 0]
    existing_candidates = cmte_scorecard[how_many_votes != 0]
    return [new_candidates_df, existing_candidates]

def compute_candidate_overall_score(scorecard_df):
    scorecard_df['candidate_score'] = \
        scorecard_df[['2017_aclu_score','2019_environment_score','2017_naacp_score']].sum(axis=1) \
        / ( count_num_cand_votes(scorecard_df) )
    scorecard_df['candidate_score'] = scorecard_df['candidate_score'] * 100
    return scorecard_df

def get_cmte_scorecard(cmte_id, donations_df, cand_df, scorecard_df):
    cmte_donations_df = donations_df[donations_df.CMTE_ID == cmte_id]  # Select all donations where the CMTE_ID == cmte_id_sel

    cmte_donations_df = cmte_donations_df.groupby('CAND_ID').TRANSACTION_AMT.sum()  # Sum transactions
    cmte_donations_df = pd.DataFrame(cmte_donations_df)
    cmte_donations_df = cmte_donations_df.merge(cand_df, how='left', left_index=True, right_index=True,
                                                suffixes=('', ''))  # Merge candidate data into result
    cmte_donations_df = cmte_donations_df.merge(scorecard_df, how='left', left_index=True, right_index=True,
                                                suffixes=('', ''))

    return cmte_donations_df