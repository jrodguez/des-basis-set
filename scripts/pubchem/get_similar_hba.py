import pubchempy as pcp
import pandas as pd
import numpy as np
import requests
import json

#function for screening HBA


def hba_screen(smiles_list):

    temp_list = []  # temporary list to append firs round of screening to

    for i in range(len(smiles_list)):

        # checking if ammonium group is present in smiles string
        if '[N+]' in smiles_list[i][0]['CanonicalSMILES']:

            temp_list.append(smiles_list[i][0])

    new_smiles_list = []  # list that will store final screened HBA

    for i in range(len(temp_list)):
        if '.[Cl-]' in temp_list[i]['CanonicalSMILES']:  # check if contains chloride
            new_smiles_list.append(temp_list[i])

        elif '.[Br-]' in temp_list[i]['CanonicalSMILES']:  # check if contains bromide
            new_smiles_list.append(temp_list[i])

        elif '.[I-]' in temp_list[i]['CanonicalSMILES']:  # check if contains iodide
            new_smiles_list.append(temp_list[i])

        elif '.[F-]' in temp_list[i]['CanonicalSMILES']:  # check if contains fluoride
            new_smiles_list.append(temp_list[i])

        else:  # if no halides present, do not append.
            pass

    return new_smiles_list


def get_similar_hba(dataframe, source_column):

    # empty dataframe to continuously append final results to.
    final_df = pd.DataFrame()

    for i, row in dataframe.iterrows():

        # source column contains the cid's for chemical similarity search.
        cid = row[source_column]

        request_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/%s/cids/JSON?Threshold=80&MaxRecords=5000" % str(
            cid)

        request = requests.get(request_url)
        request_json = request.json()

        # adding results from request to a list.
        similarity_list = request_json['IdentifierList']['CID']

        smiles_list = []  # empty list to append smiles strings from results.

        for cid in similarity_list:
            # getting smiles strings and appending to list
            smiles_list.append(pcp.get_properties('canonical_smiles', cid))

        # screening the smiles list for HBA criteria
        screened_list = hba_screen(smiles_list)

        screened_cid_list = []  # empty list to append screened cid's into
        screened_smiles_list = []  # empty list to append screened smiles into

        for cid in range(len(screened_list)):
            screened_cid_list.append(screened_list[cid]['CID'])

        for smiles in range(len(screened_list)):
            screened_smiles_list.append(
                screened_list[smiles]['CanonicalSMILES'])

        # creating an empty temporary dataframe to put screened results in
        temp_dataframe = pd.DataFrame()

        #adding screened cid and smiles to the temporary dataframe
        temp_dataframe['HBA_cid'] = screened_cid_list
        temp_dataframe['HBA_smiles'] = screened_smiles_list

        print(temp_dataframe)

        final_df = final_df.append(temp_dataframe)  # appending to final dataframe

    return final_df
