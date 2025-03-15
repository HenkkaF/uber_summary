import pandas as pd

def analyze_wait_time(input_file_path, output_file_path):
    # Load data and prepare columns
    df = pd.read_excel(input_file_path)
    df['wait_time'] = df['wait_time'].str.extract(r'(\d+)').astype(float)
    df['total_shared_rides'] = df[['trips_pool', 'trips_express']].sum(axis=1)
    df['match_proportion'] = df['total_matches'] / df['total_shared_rides']
    df['double_match_proportion'] = df['total_double_matches'] / df['total_shared_rides']
    df['driver_payout_per_trip'] = df['total_driver_payout'] / df['total_shared_rides']

    # Compute summary statistics
    summary = df.groupby('wait_time').agg(
        total_shared_rides=('total_shared_rides', 'sum'),
        avg_match_proportion=('match_proportion', 'mean'),
        avg_double_match_proportion=('double_match_proportion', 'mean'),
        avg_driver_payout_per_trip=('driver_payout_per_trip', 'mean'),
        avg_rider_cancellations=('rider_cancellations', 'mean'),
        avg_trips_pool=('trips_pool', 'mean'),
        avg_trips_express=('trips_express', 'mean'),
        avg_matches=('total_matches', 'mean'),
        avg_double_matches=('total_double_matches', 'mean'),
        avg_driver_payout=('total_driver_payout', 'mean'),
        unique_cities=('city_id', 'nunique'),
        avg_treat=('treat', 'mean'),
        avg_commute=('commute', 'mean')
    ).reset_index()

    # Calculate p% difference
    if len(summary) > 1:
        percent_diff = ((summary.iloc[1] - summary.iloc[0]) / summary.iloc[0]) * 100
        percent_diff['wait_time'] = 'Difference (%)'
        summary = pd.concat([summary, percent_diff.to_frame().T], ignore_index=True)

    # Save result and print
    summary.to_excel(output_file_path, index=True)
    print(summary.to_string(index=False))


analyze_wait_time('datasetPage.xlsx', 'summary.xlsx')
