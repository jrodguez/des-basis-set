import pandas as pd
import requests
import json
import pubchempy as pcp


def check_GHS_data(request_json):
    """This function checks to see if GHS safety information data is available
    in the pubchem data file for a chemical"""

    if 'Fault' in request_json:  # first key in dict will be Fault if no GHS heading in json data
        return 'No GHS data available'

    else:
        return 'GHS data available'


def hazard_classification(request_json):
    """This function checks if the subsatnce is classified as hazardous or non hazardous if GHS data was found"""

    GHS_status = check_GHS_data(request_json)

    # cas if no data was found in ghs retrieval function
    if GHS_status == 'No GHS data available':
        return GHS_status

    #otherwise, continue to parse through the json file to determine if the substance is hazardous or not
    else:
        if len(request_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information']) == 1:
            return 'Not classified as a hazardous substance'

        else:
            return 'Hazardous substance'


def get_hazard_codes(cid):

    """This is the main wrapper function for retrieving GHS hazard codes"""

    safety_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%s/JSON?heading=GHS+Classification" % str(cid)

    request = requests.get(safety_url)
    request_json = request.json()


    hazard_status = hazard_classification(request_json)

    if hazard_status == 'No GHS data available':
        return hazard_status

    elif hazard_status == 'Not classified as a hazardous substance':
        return hazard_status

    elif hazard_status == 'Hazardous substance':
        
        GHS_information_list = [] #list that contains GHS information in which hazard codes are located.
        
        for i in range(len(request_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][2]['Value']['StringWithMarkup'])):
            temp_list = [] #temporary list each sentance gets added to before appending to GHS list
            temp_list.append(request_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][2]['Value']['StringWithMarkup'][i]['String'])
            GHS_information_list.append(temp_list)
            
        #this portion checks for lists with empty string '' that will break the code if not removed
        for item in GHS_information_list:
            if '' not in item: 
                pass
        
            elif '' in item:
                index = GHS_information_list.index(item)
                GHS_information_list[index].remove('')
        
            
        hazard_description_list = [] #list that will contain the hazard codes and their descriptions. 
        
        for item in GHS_information_list:
            temp_haz = [idx for idx in item if idx[0] == 'H'] #list comprehension, keeps lists that start with H, i.e. the hazard code
            hazard_description_list.append(temp_haz)
            #There will be empty lists so this step removes them
            for item in hazard_description_list:
                if len(item) == 0:
                    hazard_description_list.remove(item)
                    
        hazard_code_list = [] #list that contains all of the hazard codesfor the chemcial
        
        for item in hazard_description_list:
            string = item[0]
            hazard = string.split(' ', 1)[0]
            hazard_code_list.append(hazard)
            
        return hazard_code_list
                    
