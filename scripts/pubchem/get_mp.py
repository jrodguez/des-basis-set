import pubchempy as pcp
import pandas as pd
import requests
import json

def get_mp(dataframe, source_column, new_column_name):

    final_mp_list = [] #empty list to append melting point values to

    for i, row in dataframe.iterrows():

        # source column contains the cid's for chemical similarity search.
        cid = row[source_column]

        request_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%s/JSON?heading=Melting+Point" % str(cid)

        request = requests.get(request_url)
        request_json = request.json() 

      

        if 'Fault' in request_json:  #fault will apear if no melting point data available
            mp = 'no mp data'
            final_mp_list.append(mp)

        else:
            parsed_list = [] #list that contains the mp info from the json file

            for i in range(len(request_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'])):
                temp_list = []
                temp_list.append(request_json['Record']['Section'][0]['Section'][0]['Section']
                                [0]['Information'][i]['Value']['StringWithMarkup'][0]['String'])
                parsed_list.append(temp_list)

            mp_list = [] #list that will only contain the melting points in Celsius from the parsed list

            for i in parsed_list:
                if u'\N{DEGREE SIGN}C' in i[0]: #checking if mp is in Celsius
                    mp = i[0].split(u'\N{DEGREE SIGN}')[0] #splits the string on the degree symbol and grabs the melting point
                    mp_list.append(mp)

            if len(mp_list) == 0: #if list len is zero, only melting point in F available
                temp_list_2 = [] #stores temp mp value in farenheit
                for i in parsed_list:
                    # taking mp in farenheit
                    if u'\N{DEGREE SIGN}F' in i[0]:
                        # splits the string on the degree symbol and grabs the melting point
                        mp = i[0].split(u'\N{DEGREE SIGN}')[0]

                        if len(mp) >3:              #in some cases, the string is a temp range and needs to be split again.
                            mp = mp.split(' ')[0]   # Splits the string on the first space and grabs the first element, which is lowest mp from range.

                        temp_list_2.append(mp)

                for j in temp_list_2:
                    mp_c = (float(j) - 32)*(5/9)
                    mp_list.append(mp_c)

            if len(mp_list) ==0: #if len is still zero, then no mention of C or F and value is not certain.
                mp = 'Units uncertain'
                mp_list.append(mp)

            mp_list.sort() #sorts mp from lowest to highest. Some sources may vary the mp they report
            final_mp_list.append(mp_list[0])

    dataframe[new_column_name] = final_mp_list

    return dataframe




