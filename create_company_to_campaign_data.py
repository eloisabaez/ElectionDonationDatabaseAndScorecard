import pandas as pd

bulk_cmte_data_file = './campaign_finance_data/2019-2020_company_to_campaign_bulk_data.txt'
columns=['CMTE_ID', 'AMNDT_IND', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', 'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID','CAND_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID']
bulk_cmmte_data = pd.read_csv(bulk_cmte_data_file, sep="|", header=None, low_memory=False,names=columns)
bulk_cmmte_data = bulk_cmmte_data.sort_values(by='CMTE_ID')

cmte_id_key_file = './campaign_finance_data/2019-2020_company_master.txt'
cmte_id_cols=['CMTE_ID', 'CMTE_NM', 'TRES_NM', 'CMTE_ST1', 'CMTE_ST2', 'CMTE_CITY', 'CMTE_ST', 'CMTE_ZIP', 'CMTE_DSGN', 'CMTE_TP', 'CMTE_PTY_AFFILIATION','CMTE_FILING_FREQ','ORG_TP','CONNECTED_ORG_NM','CAND_ID']
cmte_id_key = pd.read_csv(cmte_id_key_file, sep="|", header=None, low_memory=False, names=cmte_id_cols, index_col=0)

# find pac name associated with cmte id
unique_cmtes = bulk_cmmte_data['CMTE_ID'].unique()

cmte_names = []
cmte_name_subset = []

bulk_cmmte_data.insert(1, 'CMTE_NM',  cmte_id_key.loc[bulk_cmmte_data['CMTE_ID'], 'CMTE_NM'].tolist())

print(cmte_id_key.loc['C00001461'])

print('hello')