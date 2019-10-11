import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from math import pi, ceil
from matplotlib_venn import venn2, venn3

def ask_more_values(value):
    """
    Ask the user if they would like to add an additional value
    
    Parameters
    ----------
    value: str
        currently either feature or option
        
    Return
    ------
    resp: str
        whether or not to continue asking for more values
    """ 
    resp = 'yes'
    counter = 0
    while len(resp) > 1 and counter < 3:
        if counter == 0:
            resp = input(f'Would you like to add another {value}? (Y/N)\n')
            counter += 1
        elif counter < 3:
            resp = input('Sorry, I didn\'t understand that. Please enter "Y" or "N".\n')
            counter += 1
        else:
            print('I\'m, having a hard time understanding you. Please try again later.')
            resp = 'quit'
            break
    
    return resp

def get_feature_list():
    """
    Ask the user to enter a feature
    
    Returns
    -------
    feature_list: list
        list of strings of feature names
    """
    # artificial max number of features
    n = 10
    
    # At least one feature is requested
    feature_list = []
    feature_list.append(input('Please enter a feature you will use to make your decision:\n'))
    
    # Set initial response
    resp = ask_more_values('feature')

    # More features are requested one at a time
    while resp.lower() == 'y' and len(feature_list) < n:
        feature_list.append(input('Please enter a feature you will use to make your decision:\n'))
        resp = ask_more_values('feature')
    
    return feature_list


def round10(x):
    """
    Round integer up to nearest 10
    
    Paramters
    ---------
    x: int
    """
    rounded = ceil(x/10)*10
    return rounded


def set_feature_importance(feature_list):
    """
    Set the importance of each feature
    
    Paramters
    ---------
    feature_list: list
        list of feature names
        
    Returns
    -------
    feature_dict: dict
        key value pairs are features and their absolute importance compared to each other
    """
    avg_rating = 3
    
    # Total for feature importances should add up to a round number
    num_features = len(feature_list)
    feature_dict = {}
    if num_features==1:
        feature_dict[feature_list[0]] = {'value': 1, 'percent': 1}
        return feature_dict
    else:
        total_importance = round10(avg_rating*num_features)
        
    print(f'Imagine you have {total_importance} points to assign to your {num_features} features.\n')
    print(f'Assign a nonnegative whole number to each of the following features making sure the total sums to {total_importance}.')
    np.random.shuffle(feature_list)
    points_used = 0
    for index, feature in enumerate(feature_list):
        print(f'You have {total_importance - points_used} points left,')
        print(f'and {num_features - index} more features to value.\n')
        time.sleep(0.2)
        try:
            feature_dict[feature] = input(f'How much do you value {feature}?\t')
            feature_dict[feature] = {'value': int(feature_dict[feature]), 'percent': int(feature_dict[feature])/total_importance}
            points_used += feature_dict[feature]['value']
        except:
            print('You must enter a whole number')
            feature_dict[feature] = input(f'How much do you value {feature}?\t')
            feature_dict[feature] = {'value': int(feature_dict[feature]), 'percent': int(feature_dict[feature])/total_importance}
            points_used += feature_dict[feature]['value']
            
    return feature_dict

def get_option_list():
    """
    Ask the user to enter an option
    
    Returns
    -------
    option_list: list
        list of strings which are the options we need to decide between
    """
    # artificial max number of features
    n = 5
    
    # At least one feature is requested
    option_list = []
    option_list.append(input('Please enter the first option you need to compare:\n'))
    
    # Set initial response
    resp = ask_more_values('option')

    # More features are requested one at a time
    while resp.lower() == 'y' and len(option_list) < n:
        option_list.append(input('Please enter the next option you are comparing:\n'))
        resp = ask_more_values('option')
    
    return option_list


def rate_each_option(feature_list, option_list):
    """
    rate each feature in each option
    
    Parameters
    ----------
    feature_list: list
        list of features on which to rate each option
        
    option_list: list
        list of options which are being pitted against each other
        
    Returns
    -------
    option_dict: dict
        key value pairs are option and a dictionary with a rating (out of 10) for each feature
    """
    option_dict = {}
    for option in option_list:
        feature_rating_dict = {}
        for feature in feature_list:
            feature_rating_dict[feature] = int(input(f'Out of 10, how do you rate {option} in terms of {feature}?\n'))
        option_dict[option] = feature_rating_dict
        
    return option_dict


def print_scores(option_value_df, option_list):
    """
    Calculates and prints the final scores
    
    Paramters
    ---------
    option_value_df: DataFrame
        Rows are features. Columns are options, absolute importances, and percent importances
        
    option_list: list
        list of options. easier to hand in the options list then go back and determine options from column names.
    """
    for option in option_list:
        total = option_value_df[option]*option_value_df['percent']
        print(f'{option}: ', total.sum()/10)
    return


def dual_radar_plot(df, comparison_pair):
    """
    Make a radar plot comparing feature values of two options
    
    Parameters
    ----------
    df: DataFrame
        df contains all option ratins for each feature
    
    comparison_pair: list
        two strings. Identify which options to compare. 
        Only use two because more comparisons on a radar plot looks messy.
    """
    # ------- PART 1: Create background
    feature_list = df.index.values

    # number of variable
    N = len(feature_list)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], feature_list)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8], ["2", "4", "6", "8"], color="grey", size=7)
    plt.ylim(0, 10)


    # ------- PART 2: Add plots

    # Plot each individual = each line of the data
    # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
    for option in comparison_pair:
        values = df[option].values.tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=option)
        ax.fill(angles, values, 'b', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()
    return

def get_options_for_radar(option_list):
    """
    Gets 1 or 2 options for the radar plot
    """
    print('Choose up to two options to compare on a radar plot. ')
    print('Remember, the list of options are:\n')
    print(*option_list, sep="\n")
    comparison_list = ['none']
    counter = 0
    time.sleep(1)
    while comparison_list[0] not in option_list:
        comparison_list[0] = input('Enter the first option to compare:\n')
        counter += 1
        if counter > 3:
            print('Sorry, I missed that. I\'ll use the first option.')
            comparison_list[0] = option_list[0]
            break
    
    comparison_list.append(input('Enter the second option to compare, or type "none":\n'))
    while comparison_list[1] not in option_list:
        comparison_list[1] = input('Enter the first option to compare:\n')
        counter += 1
        if counter > 3:
            print('Sorry, I missed that. We\'ll skip this option.')
            comparison_list[1] = 'none'
            break
    
    if comparison_list[1] == 'none':
        return comparison_list[0]
    return comparison_list


def create_venn2(df, comparison_pair):
    """
    Create a 2 circle Venn Diagram
    
    Parameters
    ----------
    df: DataFrame
        df contains all option ratins for each feature
    
    comparison_pair: list
        two strings. Identify which options to compare. 
    """
    
    list_of_dicts = df[comparison_pair].T.to_dict('records')
    list_of_strings = []
    for key, value in list_of_dicts[0].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_A = set(list_of_strings)
    
    list_of_strings = []
    for key, value in list_of_dicts[1].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_B = set(list_of_strings)
    
    list_of_sets = [set_A, set_B]
    
    plt.figure(figsize=(10,10))

    v = venn2(list_of_sets, set_labels=comparison_pair)
    
    alpha_strings = list(set_B.difference(set_A))
    v.get_label_by_id('01').set_text('\n'.join(alpha_strings))
    
    beta_strings = list(set_A.difference(set_B))
    v.get_label_by_id('10').set_text('\n'.join(beta_strings))
    
    intersection_strings = list(set_B.intersection(set_A))
    try:
        v.get_label_by_id('11').set_text('\n'.join(intersection_strings))
    except:
        pass #v.get_label_by_id('11').set_text('no overlap')
    
    plt.title('Venn Diagram')
    plt.show()
    
    return


def create_venn3(df, comparison_triple):
    """
    Create a 3 circle venn diagram
    
    Parameters
    ----------
    df: DataFrame
        df contains all option ratins for each feature
    
    comparison_pair: list
        three strings. Identify which options to compare.
    """
    list_of_dicts = df[comparison_triple].T.to_dict('records')
    list_of_strings = []
    for key, value in list_of_dicts[0].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_A = set(list_of_strings)
    
    list_of_strings = []
    for key, value in list_of_dicts[1].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_B = set(list_of_strings)
    
    list_of_strings = []
    for key, value in list_of_dicts[2].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_C = set(list_of_strings)
    
    list_of_sets = [set_A, set_B, set_C]
    # Careful! set_A is associated with 100, set_B is associated with 010, set_C is associated with 001
    
    strings_100 = list(set_A.difference(set_B).difference(set_C))
    strings_010 = list(set_B.difference(set_A).difference(set_C))
    strings_001 = list(set_C.difference(set_A).difference(set_B))
    strings_110 = list(set_A.intersection(set_B).difference(set_C))
    strings_101 = list(set_A.intersection(set_C).difference(set_B))
    strings_011 = list(set_B.intersection(set_C).difference(set_A))
    strings_111 = list(set_A.intersection(set_B).intersection(set_C))
    
    
    plt.figure(figsize=(10,10))
    
    # Again, careful! the ordering is backwards in the same way as above
    v=venn3(subsets = (len(strings_100),
                       len(strings_010),
                       len(strings_110),
                       len(strings_001),
                       len(strings_101),
                       len(strings_011),
                       len(strings_111)),
                       set_labels = comparison_triple)
    
    v.get_label_by_id('001').set_text('\n'.join(strings_001))
    v.get_label_by_id('010').set_text('\n'.join(strings_010))
    v.get_label_by_id('100').set_text('\n'.join(strings_100))
    
    try:
        v.get_label_by_id('011').set_text('\n'.join(strings_011))
    except:
        pass #v.get_label_by_id('011').set_text('no overlap')
    
    try:
        v.get_label_by_id('101').set_text('\n'.join(strings_101))
    except:
        pass #v.get_label_by_id('101').set_text('no overlap')
    
    try:
        v.get_label_by_id('110').set_text('\n'.join(strings_110))
    except:
        pass #v.get_label_by_id('110').set_text('no overlap')
        
    try:
        v.get_label_by_id('111').set_text('\n'.join(strings_111))
    except:
        pass #v.get_label_by_id('111').set_text('no overlap')
    
    
    plt.title('Venn Diagram')
    
    plt.show()
    
    return