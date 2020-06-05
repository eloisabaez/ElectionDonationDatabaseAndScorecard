import pandas as pd

bulk_cmte_data_file = './campaign_finance_data/2019-2020_company_to_campaign_bulk_data.txt'
columns=['CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','CAND_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID']
donations_df = pd.read_csv(bulk_cmte_data_file, sep="|", header=None, low_memory=False, names=columns)
# bulk_cmmte_data = bulk_cmmte_data.drop(['AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'], axis=1)
# bulk_cmmte_data.dropna(subset=['CAND_ID'],inplace=True)
# non_voided_disbursements_iter = bulk_cmmte_data['TRANSACTION_AMT'] > 0
# bulk_cmmte_data = bulk_cmmte_data[non_voided_disbursements_iter]

cmte_id_key_file = './campaign_finance_data/2019-2020_company_master.txt'
cmte_id_cols=['CMTE_ID', 'CMTE_NM', 'TRES_NM', 'CMTE_ST1', 'CMTE_ST2', 'CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CMTE_DSGN', 'CMTE_TP', 'CMTE_PTY_AFFILIATION','CMTE_FILING_FREQ','ORG_TP','CONNECTED_ORG_NM','CAND_ID']
cmte_df = pd.read_csv(cmte_id_key_file, sep="|", header=None, low_memory=False, names=cmte_id_cols, index_col=0)

cand_id_key_file = './campaign_finance_data/2019-2020_candidate_master.txt'
cand_id_cols=['CAND_ID', 'CAND_NAME', 'CAND_PTY_AFFILIATION', 'CAND_ELECTION_YR', 'CAND_OFFICE_ST', 'CAND_OFFICE', 'CAND_OFFICE_DISTRICT', 'CAND_ICI', 'CAND_STATUS', 'CAND_PCC', 'CAND_ST1','CAND_ST2','CAND_CITY','CAND_ST','CAND_ZIP']
cand_df = pd.read_csv(cand_id_key_file, sep="|", header=None, low_memory=False, names=cand_id_cols, index_col=0)

## Select commitee here
cmte_id_sel = 'C00360354'

## Processing
cmte_donations_df = donations_df[donations_df.CMTE_ID == cmte_id_sel] # Select all donations where the CMTE_ID == cmte_id_sel

cmte_donations_df = cmte_donations_df.groupby('CAND_ID').TRANSACTION_AMT.sum()   # Sum transactions
cmte_donations_df = pd.DataFrame(cmte_donations_df)
cmte_donations_df = cmte_donations_df.merge(cand_df, how='left', left_index=True, right_index=True, suffixes=('',''))   # Merge candidate data into result

# Todo drop columns you don't need
# Todo add scores