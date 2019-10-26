import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from itertools import combinations
from math import pi, ceil
from matplotlib_venn import venn2, venn3

#---------------------------------------------------------------------
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

#---------------------------------------------------------------------
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


#---------------------------------------------------------------------
def round10(x):
    """
    Round integer up to nearest 10
    
    Paramters
    ---------
    x: int
    """
    rounded = ceil(x/10)*10
    return rounded


#---------------------------------------------------------------------
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

#---------------------------------------------------------------------
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


#---------------------------------------------------------------------
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


#---------------------------------------------------------------------
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
    temp_dict = {}
    for option in option_list:
        total = option_value_df[option]*option_value_df['percent']
        temp_dict[option] = round(total.sum()*10)
    for option_value in sorted(temp_dict.items(), key=lambda x: x[1], reverse=True):
        print(f'{option_value[0]} meets {option_value[1]}% of your desired features.')
    return


#---------------------------------------------------------------------
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


#---------------------------------------------------------------------
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


#---------------------------------------------------------------------
def create_venn2(df, comparison_pair):
    """
    Create a 2 circle Venn Diagram
    
    Parameters
    ----------
    df: DataFrame
        df contains all option ratings for each feature
    
    comparison_pair: list
        Two strings. Determines which options to compare. 
    """
    
    list_of_dicts = df[comparison_pair].T.to_dict('records')
    
    list_of_strings = []
    for key, value in list_of_dicts[0].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_A = set(list_of_strings)
    
    try:
        list_of_strings = []
        for key, value in list_of_dicts[1].items():
            list_of_strings.append(str(key)+':'+str(value))
        set_B = set(list_of_strings)
    except:
        set_B=set_A
    
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


#---------------------------------------------------------------------
def create_venn3(df, comparison_triple):
    """
    Create a 3 circle venn diagram
    
    Parameters
    ----------
    df: DataFrame
        df contains all option ratins for each feature
    
    comparison_pair: list
        Three strings. Determines which options to compare.
    """
    list_of_dicts = df[comparison_triple].T.to_dict('records')
    
    list_of_strings = []
    for key, value in list_of_dicts[0].items():
        list_of_strings.append(str(key)+':'+str(value))
    set_A = set(list_of_strings)
    
    try:
        list_of_strings = []
        for key, value in list_of_dicts[1].items():
            list_of_strings.append(str(key)+':'+str(value))
        set_B = set(list_of_strings)
    except:
        set_B = set_A
    
    try:
        list_of_strings = []
        for key, value in list_of_dicts[2].items():
            list_of_strings.append(str(key)+':'+str(value))
        set_C = set(list_of_strings)
    except:
        set_C = set_A
    
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


#---------------------------------------------------------------------
# DECISION CLASS
#---------------------------------------------------------------------
class Decision():
    """
    A class to easily store previous decisions
    """
    def __init__(self, example=False):
        if example:
            self.feature_list = ['feature1', 'feature3', 'feature4', 'feature2']
            self.feature_dict = {'feature1': {'value': 1, 'percent': 0.1},
     'feature3': {'value': 3, 'percent': 0.3},
     'feature4': {'value': 4, 'percent': 0.4},
     'feature2': {'value': 2, 'percent': 0.2}}
            self.option_list = ['option1', 'option2', 'option3', 'option4']
            self.option_dict = {'option1': {'feature1': 0, 'feature3': 6, 'feature4': 9, 'feature2': 3},
     'option2': {'feature1': 3, 'feature3': 9, 'feature4': 0, 'feature2': 6},
     'option3': {'feature1': 6, 'feature3': 0, 'feature4': 3, 'feature2': 9},
     'option4': {'feature1': 9, 'feature3': 3, 'feature4': 6, 'feature2': 0}}
            self.update_option_value_df()
        else:
            self.feature_list = []
            self.feature_dict = {}
            self.option_list = []
            self.option_dict = {}
        return
        
    def build_decision(self):
        self.feature_list = get_feature_list()
        self.feature_dict = set_feature_importance(self.feature_list)
        self.option_list = get_option_list()
        self.option_dict = rate_each_option(self.feature_list, self.option_list)
        self.update_option_value_df()
        return
        


#---------------------------------------------------------------------
# UPDATING FEATURES AND OPTIONS
#---------------------------------------------------------------------
    def update_option_value_df(self):
        self.option_value_df = pd.DataFrame.from_dict(self.option_dict).merge(
            pd.DataFrame(self.feature_dict).T, left_index=True, right_index=True)
        return 
        
    def update_option_dict(self, feature=None, option=None):
        """
        If the option is not in the keys, option will be added and function will request user input to rate.
        if option is in the keys, option key value pair will be removed.
        
        Parameters
        ----------
        feature: str
            The feature key that will be added or removed. 
            If added, will rate all options on this new feature
        
        option: str
            The key that will be added or removed. 
            If added, will rate all features in this new option
        """
        if feature != None:
            try:
                for k in self.option_dict.keys:
                    self.option_dict[k].pop(feature)
            except:
                for k, v in rate_each_option([feature], self.option_list).items():
                    self.option_dict[k].update(v)
        
        elif option != None:
            try:
                self.option_dict.pop(option)            
            except:
                self.option_dict.update(rate_each_option(self.feature_list, [option]))
        
        print('New option dict:\n', self.option_dict)
        self.update_option_value_df()
        return
    
    def update_option_list(self, option):
        """
        If option is not in the list, option will be added to list
        If option is in list, option will be removed.
        
        Parameters
        ----------
        option: str
            the feature that will be added or removed
        """
        try:
            self.option_list.remove(option)
        except:
            self.option_list.append(option)
                                    
        print('New option list:\n', self.option_list)
        
        self.update_option_dict(None, option)
        return
    
    def update_feature_dict(self, feature):
        """
        If the feature is not in the keys, feature will be added and function will request user input to rate.
        If feature is in the keys, feature key value pair will be removed.
        
        Parameters
        ----------
        feature: str
            the key that will be added or removed
        """
        if feature == 'null':
            self.feature_dict.update(set_feature_importance(self.feature_list))
        else:
            try:
                self.feature_dict.pop(feature)
                self.feature_dict.update(set_feature_importance(self.feature_list))
                self.update_option_dict(None, None)
            except:
                self.feature_dict.update(set_feature_importance(self.feature_list))
                self.update_option_dict(feature, None)
        
        print('New feature dict:\n', self.feature_dict)
        
        return
    
    def update_feature_list(self, feature):
        """
        If feature is not in the list, feature will be added to list
        If feature is in list, feature will be removed.
        
        Parameters
        ----------
        feature: str
            the feature that will be added or removed
        """
        try:
            self.feature_list.remove(feature)
        except:
            self.feature_list.append(feature)
                                    
        print('New feature list:\n', self.feature_list)
        
        self.update_feature_dict(feature)
        return
    
    def feature_list_keep(self, list_of_features):
        """
        Reduces self.feature_list to the provided list of features.
        
        Parameters
        ----------
        list_of_features: list
            List of strings of feature names from self.feature_list.
            These features will remain, all other features will be removed
        """
        try:
            assert set(list_of_features).issubset(set(self.feature_list))
        except:
            print('Please only use features provided in feature_list attribute.')
            return
        self.feature_list = list_of_features
        self.feature_dict = set_feature_importance(self.feature_list)
        self.update_option_value_df()
        
        return


#---------------------------------------------------------------------
# DISPLAYING RESULTS
#---------------------------------------------------------------------
    def print_results(self, option_list=None):
        """
        Prints the percentage match for options in the provided option list. 
        Default prints the percentage match for every option.
        
        Parameters
        ----------
        option_list: list
            List containing the options whose results will be printed. 
            If no option list is provided, all results will be printed.
        """
        if option_list==None:
            option_list=self.option_list
        
        print_scores(self.option_value_df, option_list)
        
    def plot_radar2(self, option_list=None):
        """
        Prints the overlapping radar plots for each pair in the provided option list. 
        Default prints the radar plot for every pair of options. 
        If the provided option list only contains one option, prints this option's radar plot.
        
        Parameters
        ----------
        option_list: list
            List containing the options whose radar plots will be printed. 
            If no option list is provided, all pairs of radar plots will be printed.
        """
        if option_list==None:
            option_list=self.option_list
        
        if len(option_list)==1:
            dual_radar_plot(self.option_value_df, option_list)
        else:
            for pair in list(combinations(option_list, 2)):
                dual_radar_plot(self.option_value_df, pair)
        
    def plot_venn2(self, option_list=None):
        """
        Prints the venn diagram for each pair in the provided option list. 
        Default prints the venn diagram for every pair of options.
        
        Parameters
        ----------
        option_list: list
            List containing the options whose pairs venn diagrams will be printed. 
            If no option list is provided, all pairs of venn diagrams will be printed.
        """
        if option_list==None:
            option_list=self.option_list
        
        for pair in list(combinations(option_list, 2)):
            create_venn2(self.option_value_df, list(pair))
        
    def plot_venn3(self, option_list=None):
        """
        Prints the venn diagram for each triple in the provided option list. 
        Default prints the venn diagram for every triple of options.
        
        Parameters
        ----------
        option_list: list
            List containing the options whose triples venn diagrams will be printed. 
            If no option list is provided, all triples of venn diagrams will be printed.
        """
        if option_list==None:
            option_list=self.option_list
        
        for triple in list(combinations(option_list, 3)):
            create_venn3(self.option_value_df, list(triple))
    