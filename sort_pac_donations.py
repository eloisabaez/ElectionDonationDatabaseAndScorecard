import pandas as pd

def find_candidates_donated_to(file_name):
    company_data = pd.read_csv(file_name)

    company_data = company_data.sort_values(by = 'candidate_name')

    candidate_name_iter = company_data['candidate_name'].notnull()
    candidate_name_subset = company_data[candidate_name_iter]

    non_voided_disbursements_iter = candidate_name_subset['disbursement_amount'] > 0
    non_voided_disbursements = candidate_name_subset[non_voided_disbursements_iter]

    unique_candidates = non_voided_disbursements['candidate_name'].unique()

    candidate_names = []
    candidate_offices = []
    candidate_states = []
    disbursement_amounts = []

    for candidate in unique_candidates:
        # add candidate name
        candidate_names.append(candidate)
        print(candidate)

        # calculate individual disbursement amount
        current_cand_disbursement_iter = non_voided_disbursements['candidate_name'] == candidate
        current_cand_disbursement_array = non_voided_disbursements[current_cand_disbursement_iter]
        current_cand_disbursement = current_cand_disbursement_array['disbursement_amount'].sum()
        disbursement_amounts.append(current_cand_disbursement)
        print(current_cand_disbursement)

        # get individual office
        curr_cand_office = current_cand_disbursement_array.iloc[0,24]
        candidate_offices.append(curr_cand_office)
        print(curr_cand_office)

        # get individual state
        curr_cand_state = current_cand_disbursement_array.iloc[0, 33]
        candidate_states.append(curr_cand_state)
        print(curr_cand_state)


    data = {'candidate_name':candidate_names, 'candidate_office':candidate_offices, 'candidate_state':candidate_states, 'disbursement_amount':disbursement_amounts}
    candidate_data = pd.DataFrame(data)
    print(candidate_data)

file_name = './campaign_finance_data/amazon_campaign_contributions_2020.csv'
find_candidates_donated_to(file_name)