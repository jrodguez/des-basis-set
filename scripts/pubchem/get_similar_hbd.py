import pubchempy as pcp
import pandas as pd
import numpy as np
import requests
import json

def get_similar_hbd(dataframe, source_column):

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

        #note no actual screening is being done for the HBD, unlike the HBA
        screened_cid_list = []  # empty list to append screened cid's into
        screened_smiles_list = []  # empty list to append screened smiles into

        for cid in range(len(smiles_list)):
            screened_cid_list.append(smiles_list[cid][0]['CID'])

        for smiles in range(len(smiles_list)):
            screened_smiles_list.append(
                smiles_list[smiles][0]['CanonicalSMILES'])

        # creating an empty temporary dataframe to put screened results in
        temp_dataframe = pd.DataFrame()

        #adding screened cid and smiles to the temporary dataframe
        temp_dataframe['HBD_cid'] = screened_cid_list
        temp_dataframe['HBD_smiles'] = screened_smiles_list

        print(temp_dataframe)

        # appending to final dataframe
        final_df = final_df.append(temp_dataframe)

    return final_df
