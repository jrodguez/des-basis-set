outer_old = pd.DataFrame()
outer_new = pd.DataFrame()

#for i in range(31):
with open("nist_data/conductivity/1.json") as json_file:

    #grab data, data headers (names), the salt name
    json_full = json.load(json_file)                    
    json_data = pd.DataFrame(json_full['data'])
    json_datanames = np.array(json_full['dhead'])        # make names into array to add as columns headers for df
    json_data.columns =  json_datanames
    json_saltname = pd.DataFrame(json_full['components'])#components section contains names of DES components
    #print(json_saltname['name'])                #grabbing the HBD and HBA 

    inner_old = pd.DataFrame()
    inner_new = pd.DataFrame()

    #loop through the columns of the data, note that some of the 
    #json files are missing pressure data. 
    for indexer in range(len(json_data.columns)):        
        grab=json_data.columns[indexer]
        list = json_data[grab]
        my_list = [l[0] for l in list]
        dfmy_list = pd.DataFrame(my_list)
        dfmy_list.columns = [json_datanames[indexer][0]]
        inner_new = pd.concat([dfmy_list, inner_old], axis=1)
        inner_old = inner_new

    #print(inner_new)

    #add the DES components, i.e. HBA and HBD
    # they are not always listed in the same order on nist data, i.e., HBA always first. Will figure out later.
    inner_old['HBA']=json_saltname['name'][1]
    inner_old['HBD']=json_saltname['name'][0]

    #print(inner_old)

    #add to the growing dataframe
    outer_new = pd.concat([inner_old, outer_old], axis=0)
    outer_old = outer_new

outer_old