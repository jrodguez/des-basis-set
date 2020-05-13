import pandas as pd
import requests
import json
import pubchempy as pcp

#Using the url below, we can access the GHS classifictaion data for a compound on pubchem
#testing with retrieving ghs classifications for choline chloride (cid = 6209)
safety_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/6209/JSON?heading=GHS+Classification"

request = requests.get(safety_url)
request_json = request.json()

#The data is basially a giant dictionary and there is a specific block that contains the GHS information we want. 
# Parsing through the dictionary to get to the desired block of text, each sentance is looped through and added to a list
GHS_information_list = []  # this list will contain the block of GHS information
for i in range(len(request_json['Record']['Section'][0]['Section'][0]['Section'][0]['Information'][2]['Value']['StringWithMarkup'])):
    temp_list = []  # temporary list each sentance gets added to before appending to GHS list
    temp_list.append(request_json['Record']['Section'][0]['Section'][0]['Section']
                     [0]['Information'][2]['Value']['StringWithMarkup'][i]['String'])
    GHS_information_list.append(temp_list)

#While this is all important information, we want to specifically extract the statements that contain the GHS hazard codes
# list that will contain the hazrad codes and their descriptions.
hazard_description_list = []
for item in GHS_information_list:
    # list comprehension, keeps lists that start with H, i.e. the hazard code
    temp_haz = [idx for idx in item if idx[0] == 'H']
    hazard_description_list.append(temp_haz)
    #There will be empty lists so this step removes them
    for item in hazard_description_list:
        if len(item) == 0:
            hazard_description_list.remove(item)

#Now that we have the hazard code and description, 
# we can go in and extract the hazard code to a list by splitting the string and retrieving the 1st substring, which is the hazard code
hazard_code_list = []
for item in hazard_description_list:
    string = item[0]
    hazard = string.split(' ', 1)[0]
    hazard_code_list.append(hazard)
