import pandas as pd
from scipy.stats import ttest_ind

def analyze_wait_time(input_file_path, output_file_path):

    # Load data and prepare columns
    df = pd.read_excel(input_file_path)
    df['wait_time'] = df['wait_time'].str.extract(r'(\d+)').astype(float)
    df['total_shared_rides'] = df[['trips_pool', 'trips_express']].sum(axis=1)
    df['match_proportion'] = df['total_matches'] / df['total_shared_rides']
    df['double_match_proportion'] = df['total_double_matches'] / df['total_shared_rides']
    df['driver_payout_per_trip'] = df['total_driver_payout'] / df['total_shared_rides']
    

    control_group = df[df['treat'] == False]
    metrics = ['total_shared_rides', 'match_proportion', 'double_match_proportion', 
               'driver_payout_per_trip', 'rider_cancellations', 'trips_pool', 'trips_express', 
               'total_matches', 'total_double_matches', 'total_driver_payout']
    
    # t-test commute = TRUE and commute = FALSE
    results = []
    for metric in metrics:
        commute_true = control_group[control_group['commute'] == True][metric].dropna()
        commute_false = control_group[control_group['commute'] == False][metric].dropna()
        t_stat, p_value = ttest_ind(commute_true, commute_false, equal_var=True)  # Student's t-test
        results.append({'Metric': metric, 'T-Statistic': t_stat, 'P-Value': p_value})
    
    commute_subset = df[df['commute'] == True]
    treatment_group = commute_subset[commute_subset['treat'] == True]  # 5 min waiting
    control_group = commute_subset[commute_subset['treat'] == False]  # 2 min waiting
    
    wait_time_results = []
    for metric in metrics:
        treat_values = treatment_group[metric].dropna()
        control_values = control_group[metric].dropna()
        t_stat, p_value = ttest_ind(treat_values, control_values, equal_var=True)  # Student's t-test
        wait_time_results.append({'Metric': metric, 'T-Statistic': t_stat, 'P-Value': p_value})
    
    # Convert results to DataFrame and save
    results_df = pd.DataFrame(results)
    wait_time_results_df = pd.DataFrame(wait_time_results)
    
    with pd.ExcelWriter(output_file_path) as writer:
        results_df.to_excel(writer, sheet_name='Commute vs Non-Commute', index=False)
        wait_time_results_df.to_excel(writer, sheet_name='Wait Time Effect', index=False)
    
    print("Commute vs Non-Commute T-Tests")
    print(results_df.to_string(index=False))
    print("\nWait Time Effect T-Tests")
    print(wait_time_results_df.to_string(index=False))

analyze_wait_time('datasetPage.xlsx', 't_test_results.xlsx')
