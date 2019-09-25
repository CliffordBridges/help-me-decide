import decisions_functions as decisions



feature_list = decisions.get_feature_list()
feature_dict = decisions.set_feature_importance(feature_list)
option_list = decisions.get_option_list()
option_dict = decisions.rate_each_option(feature_list, option_list)
option_value_df = pd.DataFrame.from_dict(option_dict).merge(pd.DataFrame(feature_dict).T, left_index=True, right_index=True)

dual_radar_plot(option_value_df, decisions.get_options_for_radar(option_list))
decisions.print_scores(option_value_df, option_list)
