def hazard_check(item):
    """This function will check the ghs info and determine to give it the max or min safety penalty
    or calculate a total hazard score"""

    if item == 'Not classified as a hazardous substance':
        # this will later get a score of 0, which is the best case
        return 'Minimum Penalty'

    if item == 'No GHS data available':
        # this will later get a score of 100 which is max case for single hazard
        return 'Maximum Penalty'

    else:
        return 'Calculate Score'


def calculate_score(hazard_list, dictionary):
    """This function will take the hazard codes from a list and grab the respectvie hazard scores from a dictionary """

    score_list = []

    for code in hazard_list:

        # some of the codes end with a colon from extarcting from jsons. Remove them here if present.
        if code.endswith(':'):
            # removes last string from item, which will be the colon.
            code = code[:-1]

        for i in dictionary['Code']:  # loop through the dictionary
            if code == dictionary['Code'][i]:  # if code is present in dictionary
                # append the hazard score to the score list
                score_list.append(dictionary['Hazard Score'][i])

    return score_list

#Writing portion that will assign values to health and environmental scores if its nonhazrdous or no ghs info found


def get_hazard_scores(item, health_list, env_list, scoring_table_dict):

    #     for item in GHS_list:
        checks = hazard_check(item)  # performing hazard check function

        if checks == 'Minimum Penalty':  # assign score of zero to both health and environmental lists
            value = 0
            health_list.append(value)
            env_list.append(value)

        elif checks == 'Maximum Penalty':  # assign score of one-hundred to both health and environmental lists
            value = 100
            health_list.append(value)
            env_list.append(value)

        elif checks == 'Calculate Score':  # here we will parse the codes based on if they pertain to a health or env hazard

            # will temp store health hazard codes to be summed and appended to final health score list
            temp_health_list = []
            # will temp store env hazard codes to be summed and appended to final health score list
            temp_env_list = []

            for hazard in item:

                if hazard[1] == '3':  # if the first number in a hazard code is 3, it is a health code

                    value = hazard
                    temp_health_list.append(value)

                elif hazard[1] == '4': #if the first number in a hazard code is 4, it is an environmental code

                    value = hazard
                    temp_env_list.append(value)

            health_scores = calculate_score(temp_health_list, scoring_table_dict)
            env_scores = calculate_score(temp_env_list, scoring_table_dict)

            health_list.append(sum(health_scores))
            env_list.append(sum(env_scores))
