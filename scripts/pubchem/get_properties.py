import pandas as pd
import pubchempy as pcp




def get_properties(dataframe, properties_list, source_column, name_prefix):
    """This function will retrieve chemical properties from the pubchem database by searching from their cid's. 
    Must input a dataframe, properties list, a source column for which to search based on cid, and a name to give as
    a prefix for the new columns"""

    empty_df = pd.DataFrame()  # empty df to append results to

    for i, row in dataframe.iterrows():

        # make sure the source column contains the cid's you want to obtain proeprties for
        cids = row[source_column]

        # will return the properties as seperate df
        temporary_df = pcp.get_properties(
            properties_list, cids, listkey_count=3, as_dataframe=True)

        # append result to empty dataframe
        empty_df = temporary_df.append(empty_df)

    # need to keep original order of results so this will fix that
    empty_df = empty_df.iloc[::-1]

    empty_df = empty_df.reset_index()  # also resetting index

    # dropping the cid column from dataframe
    empty_df = empty_df.drop(['CID'], axis=1)

    # adding prefix to column names
    empty_df = empty_df.add_prefix(name_prefix)

    # concatenating to original dataframe
    dataframe = pd.concat([dataframe, empty_df], axis=1)

    return dataframe
