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
            