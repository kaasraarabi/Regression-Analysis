import os
import pandas as pd
from data_loader.did_loader import load_did_all
from data_loader.metadata_loader import get_axis_metadata, load_metadata
from data_loader.calendar_loader import load_calendar
from data_loader.tourism_loader import load_tourism
from processing.traffic_flow import aggregate_by_period, holiday_vs_weekday_flow, day_before_after_holiday_flow
from processing.imbalance import compute_entries_exits, compute_imbalance, smooth_spikes
from processing.clustering import detect_anomalies, cluster_traffic
from visualization.plots import plot_regional_traffic, plot_time_series, plot_holiday_vs_weekday, plot_imbalance_time_series, plot_tourism_heatmap

def main(data_dir='.', output_dir='outputs'):
    os.makedirs(output_dir, exist_ok=True)
    # Load data
    did_path = os.path.join(data_dir, 'DID-ALL.csv')
    meta_path = os.path.join(data_dir, 'codeMehvar.csv')
    cal_path = os.path.join(data_dir, 'calender.csv')
    tour_path = os.path.join(data_dir, 'tourism-pro_filtered.csv')

    df_did = load_did_all(did_path)
    metadata_dict = get_axis_metadata(meta_path)
    meta_df = load_metadata(meta_path)
    df_cal = load_calendar(cal_path)
    df_tour = load_tourism(tour_path)

    # Aggregations
    daily = aggregate_by_period(df_did, period='D')
    monthly = aggregate_by_period(df_did, period='M')

    # Holiday comparisons
    hw = holiday_vs_weekday_flow(df_did, df_cal)
    before_after = day_before_after_holiday_flow(df_did, df_cal)

    # Imbalance and smoothing
    entries_exits = compute_entries_exits(df_did, metadata_dict)
    imbalance = compute_imbalance(entries_exits)
    smoothed = smooth_spikes(imbalance)

    # Clustering and anomalies
    anomalies = detect_anomalies(daily, feature_col='ALL')
    clusters = cluster_traffic(daily)

    # Visualizations (examples)
    fig1 = plot_regional_traffic(monthly, meta_df)
    fig1.write_html(os.path.join(output_dir, 'regional_traffic.html'))

    fig2 = plot_holiday_vs_weekday(hw)
    fig2.write_html(os.path.join(output_dir, 'holiday_vs_weekday.html'))

    fig3 = plot_imbalance_time_series(smoothed)
    fig3.write_html(os.path.join(output_dir, 'imbalance.html'))

    fig4 = plot_tourism_heatmap(df_tour)
    fig4.write_html(os.path.join(output_dir, 'tourism_heatmap.html'))

    print(f"Generated outputs in {output_dir}")

if __name__ == '__main__':
    main()