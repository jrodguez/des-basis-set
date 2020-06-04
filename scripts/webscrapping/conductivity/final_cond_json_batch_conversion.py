outer_old = pd.DataFrame()
outer_new = pd.DataFrame()

for i in range(31):
    with open("nist_data/conductivity/%s.json" % str(i+1)) as json_file:

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

        #print(inner_old.columns)

        #add the DES components, i.e. HBA and HBD
        # they are not always listed in the same order on nist data, i.e., HBA always first. Will figure out later.
        for i in range(len(json_saltname['name'])):
            if 'chloride' in json_saltname['name'][i] or 'bromide' in json_saltname['name'][i]:
                inner_old['HBA']=json_saltname['name'][i]
            else:
                inner_old['HBD']=json_saltname['name'][i]
                
        #loop through the column names of the dataframe
        for j in range(len(inner_old.columns)):
            #if the words Mole fraction and a halogen are contained, values are correct and no value editing 
            #necessary and column is simply renamed to HBA mole fraction.
            if 'Mole fraction' in inner_old.columns[j] and 'chloride' in inner_old.columns[j] or 'Mole fraction' in inner_old.columns[j] and 'bromide' in inner_old.columns[j]:
                inner_old = inner_old.rename(columns={inner_old.columns[j]:'HBA Mole Fraction'})
            #if the words Mole Ratio and a halogen are contained, dataset was mislabeled but values are correct.
            #only need to rename column to HBA mole fraction.
            elif 'Mole ratio' in inner_old.columns[j] and 'chloride' in inner_old.columns[j] or 'Mole ratio' in inner_old.columns[j] and 'bromide' in inner_old.columns[j]:
                inner_old = inner_old.rename(columns={inner_old.columns[j]:'HBA Mole Fraction'})
            #if the words mole ratio are present, but no halogens, the ratio of the HBD is displayed and needs
            #to be changed to HBA mole fraction. First relabel the colum as HBA mole fraction.
            elif 'Mole ratio' in inner_old.columns[j] and not 'chloride' in inner_old.columns[j] or 'Mole ratio' in inner_old.columns[j] and not 'bromide' in inner_old.columns[j]:
                inner_old = inner_old.rename(columns={inner_old.columns[j]:'HBA Mole Fraction'})
                #apparently the numbers are strings so change to integer. May need to do this for every other column
                inner_old['HBA Mole Fraction'] = inner_old['HBA Mole Fraction'].astype(int)
                #next make an empty list that will hold all the new HBA mole fractions
                mole_fractions_list = []
                #loop through every HBD ratio in the column
                for k in range(len(inner_old['HBA Mole Fraction'])):
                    #Calculate the HBA mole fraction from every HBD ratio and append to the list
                    mole_fractions_list.append(1/(1+inner_old['HBA Mole Fraction'][k]))
                #finally make the list the new mole fraction column in the dataframe
                inner_old['HBA Mole Fraction'] = mole_fractions_list
            #in the last case, if the word mole fraction is present but not a halogen, HBD mole fraction is displayed.
            #Follow simialr process as before
            elif 'Mole fraction' in inner_old.columns[j] and not 'chloride' in inner_old.columns[j] or 'Mole fraction' in inner_old.columns[j] and not 'bromide' in inner_old.columns[j]:
                inner_old = inner_old.rename(columns={inner_old.columns[j]:'HBA Mole Fraction'})
                #convert to float instead since it is a decimal
                inner_old['HBA Mole Fraction'] = inner_old['HBA Mole Fraction'].astype(float)
                #empty list
                mole_fractions_list = []
                #loop through column
                for k in range(len(inner_old['HBA Mole Fraction'])):
                    #subtract 1 from HBD mole fraction to get HBA mole fraction and append to list
                    mole_fractions_list.append(1 - inner_old['HBA Mole Fraction'][k])
                #replace column   
                inner_old['HBA Mole Fraction'] = mole_fractions_list


        #add to the growing dataframe
        outer_new = pd.concat([inner_old, outer_old], axis = 0, ignore_index = True)
        outer_old = outer_new
 
outer_old.head(50)