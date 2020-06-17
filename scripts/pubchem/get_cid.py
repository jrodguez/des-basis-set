import pandas as pd
import pubchempy as pcp

def get_cid (dataframe, source_column, new_column):
    
    """This function will retrieve the pubchem cid's for chemicals in a dataframe. The dataframe, source column
    for which to retrieve cid's and name of a new column to append to the dataframe"""
    
    cid_results = [] #temporary empty list that will contain the cid's retrieved by pubchem  
    final_cid = []   #empty list that will contain the final cid's
    
    for i, row in dataframe.iterrows():
        
        names = row[source_column]
        
        #pubchempy command for retrieving cid's and appending to temporary list
        #note you need to input how you wish to search for the cid, here we are searching by chemcial 'name'
        cid_results.append(pcp.get_cids(names, 'name', list_return='flat')) 

    for j in cid_results:
    
        if len(j) == 0:                    #case in which no cid was found by pubchempy
            final_cid.append("no cid found") 


        if len(j) >= 1:                    #append only the first cid
            final_cid.append(j[0])
            
    dataframe[new_column] = final_cid
    
    return dataframe
