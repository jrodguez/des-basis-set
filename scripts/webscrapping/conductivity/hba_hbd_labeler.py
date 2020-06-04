#loop through the name column in the saltname file that contains the HBA and HBD
for i in range(len(json_saltname['name'])):
            #if a halide is present in the name, it is a HBA. Label as such. 
            if 'chloride' in json_saltname['name'][i] or 'bromide' in json_saltname['name'][i]:
                inner_old['HBA']=json_saltname['name'][i]
            #if a halide is not present in the name, it is a HBD, label as such.
            else:
                inner_old['HBD']=json_saltname['name'][i]