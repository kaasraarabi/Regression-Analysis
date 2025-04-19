import os
import pandas as pd
import jdatetime
import plotly.express as px
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
    # create a folder for per-axis results and add a note
    results_dir = os.path.join(output_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, 'README.txt'), 'w') as note:
        note.write(
            'Results directory contains subfolders for each experiment and region/city:\n'
            '- <ProvinceName>/monthly_traffic.html: per-province monthly flow plots (HTML)\n'
            '- city_daily_flow/*.png: daily flow per city\n'
            '- city_monthly_flow/*.png: monthly flow per city\n'
            '- city_imbalance/*.png: smoothed imbalance per city\n'
            '- city_holiday_vs_weekday/*.png: holiday vs weekday flow per city\n'
            '- city_before_after_holiday/*.png: avg flow before/after holidays per city\n'
            '- city_tourism_monthly/*.png: monthly tourism flow per city\n'
            '- city_entries_daily/*.png: daily entries per city\n'
            '- city_entries_monthly/*.png: monthly entries per city\n'
            '- city_entries_6M/*.png: semiannual entries per city\n'
            '- city_entries_yearly/*.png: yearly entries per city\n'
        )

    # Load data
    did_path = os.path.join(data_dir, 'DID-ALL.csv')
    meta_path = os.path.join(data_dir, 'codeMehvar.csv')
    cal_path = os.path.join(data_dir, 'calender.csv')
    tour_path = os.path.join(data_dir, 'tpf.csv')

    df_did = load_did_all(did_path)
    metadata_dict = get_axis_metadata(meta_path)
    meta_df = load_metadata(meta_path)
    df_cal = load_calendar(cal_path)
    df_tour = load_tourism(tour_path)

    # Filter experiments to ignore before Jalali year 1398
    start_gregorian = jdatetime.date(1398, 1, 1).togregorian()
    df_did = df_did[df_did['date'] >= pd.to_datetime(start_gregorian)]
    df_cal = df_cal[df_cal['date'] >= pd.to_datetime(start_gregorian)]
    df_tour = df_tour[df_tour['date'] >= pd.to_datetime(start_gregorian)]

    # Load notable cities list
    notable_file = os.path.join(data_dir, 'NotableCities.txt')
    with open(notable_file, 'r', encoding='utf-8') as f:
        notable_cities = [city.strip() for city in f.read().split(',') if city.strip()]
    allowed_cities = set(notable_cities)

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

    # Filter smoothed imbalance for notable cities
    smoothed = smoothed[smoothed['city'].isin(allowed_cities)]

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

    # aggregate monthly traffic by region (province)
    # ensure axis matches metadata type
    monthly['axis'] = monthly['axis'].astype(str)
    monthly_region = monthly.merge(meta_df[['axis','province']], on='axis', how='left')
    monthly_region = monthly_region.groupby(['province','date'])['ALL'].sum().reset_index()

    # Pie charts for regional traffic (raw and per-capita)
    pop_df = pd.read_csv(os.path.join(data_dir, 'population.csv'))
    # strip leading numeric codes from province for clean labels
    monthly_region['province'] = monthly_region['province'].str.replace(r'^\d+\s*', '', regex=True)
    # total traffic per province
    traffic_tot = monthly_region.groupby('province')['ALL'].sum().reset_index()
    # raw pie chart with proper province names
    fig_pie_raw = px.pie(traffic_tot, values='ALL', names='province', title='Total Traffic by Province')
    fig_pie_raw.write_html(os.path.join(output_dir, 'regional_traffic_pie.html'))
    # normalize by population
    merged = traffic_tot.merge(pop_df, left_on='province', right_on='Province', how='left')
    merged['traffic_per_capita'] = merged['ALL'] / merged['Population']
    fig_pie_norm = px.pie(merged, values='traffic_per_capita', names='province', title='Traffic per Capita by Province')
    fig_pie_norm.write_html(os.path.join(output_dir, 'regional_traffic_pie_normalized.html'))

    # generate a monthly time-series plot for each province in its own folder
    for province in monthly_region['province'].unique():
        prov_df = monthly_region[monthly_region['province'] == province]
        fig = plot_time_series(prov_df, 'date', 'ALL', f"Monthly Traffic for {province}")
        # create a folder named after the province (spaces replaced)
        province_folder = os.path.join(results_dir, province.replace(' ', '_'))
        os.makedirs(province_folder, exist_ok=True)
        # name file with Persian province name
        filename = f"{province.replace(' ', '_')}_monthly_traffic.html"
        fig.write_html(os.path.join(province_folder, filename))

    # Prepare per-city experiments
    # compute total flow per city (entries+exits)
    city_flow = entries_exits.copy()
    city_flow['flow'] = city_flow['entries'] + city_flow['exits']

    # Filter city_flow for notable cities only
    city_flow = city_flow[city_flow['city'].isin(allowed_cities)]

    # Create experiment directories
    exp_names = [
        'city_daily_flow', 'city_monthly_flow',
        'city_imbalance', 'city_holiday_vs_weekday',
        'city_before_after_holiday', 'city_tourism_monthly',
        'city_entries_daily', 'city_entries_monthly', 'city_entries_6M', 'city_entries_yearly'
    ]
    for exp in exp_names:
        os.makedirs(os.path.join(results_dir, exp), exist_ok=True)

    # 1) Daily and Monthly flow per city
    # Daily
    for city in city_flow['city'].unique():
        df_city = city_flow[city_flow['city'] == city]
        fig = plot_time_series(df_city, 'date', 'flow', f'Daily Flow for {city}')
        fig.write_image(os.path.join(results_dir, 'city_daily_flow', f'{city}.png'))
    # Monthly
    monthly_city = city_flow.set_index('date').groupby([pd.Grouper(freq='M'), 'city'])['flow'].sum().reset_index()
    for city in monthly_city['city'].unique():
        df_city = monthly_city[monthly_city['city'] == city]
        fig = plot_time_series(df_city, 'date', 'flow', f'Monthly Flow for {city}')
        fig.write_image(os.path.join(results_dir, 'city_monthly_flow', f'{city}.png'))

    # 2) Smoothed imbalance per city
    for city in smoothed['city'].unique():
        df_city = smoothed[smoothed['city'] == city]
        fig = plot_time_series(df_city, 'date', 'smoothed_imbalance', f'Smoothed Imbalance for {city}')
        fig.write_image(os.path.join(results_dir, 'city_imbalance', f'{city}.png'))

    # 3) Holiday vs Weekday per city
    # aggregate flows by city and is_holiday
    hw_city = city_flow.merge(df_cal, on='date', how='left')
    hw_city = hw_city.groupby(['city', 'is_holiday'])['flow'].sum().unstack(fill_value=0).reset_index()
    hw_city.columns = ['city', 'weekday_flow', 'holiday_flow']

    # Filter holiday vs weekday data for notable cities
    hw_city = hw_city[hw_city['city'].isin(allowed_cities)]

    for city in hw_city['city']:
        df_hw = hw_city[hw_city['city'] == city]
        fig = plot_holiday_vs_weekday(df_hw)
        fig.write_image(os.path.join(results_dir, 'city_holiday_vs_weekday', f'{city}.png'))

    # 4) Day Before/After Holiday per city
    from datetime import timedelta
    # get holiday dates
    holidays = df_cal[df_cal['is_holiday'] == 1]['date'].unique()
    records = []
    city_flow_idx = city_flow.set_index('date')
    for hd in holidays:
        bd = hd - timedelta(days=1)
        ad = hd + timedelta(days=1)
        before = city_flow_idx.loc[bd].groupby('city')['flow'].sum().rename('before') if bd in city_flow_idx.index else pd.Series(dtype=float, name='before')
        after = city_flow_idx.loc[ad].groupby('city')['flow'].sum().rename('after') if ad in city_flow_idx.index else pd.Series(dtype=float, name='after')
        rec = pd.concat([before, after], axis=1).fillna(0)
        records.append(rec)
    if records:
        df_ba = pd.concat(records).groupby(level=0).mean().reset_index()
        df_ba.rename(columns={df_ba.columns[0]: 'city'}, inplace=True)
    else:
        df_ba = pd.DataFrame(columns=['city', 'before', 'after'])

    # Filter before/after holiday data for notable cities
    df_ba = df_ba[df_ba['city'].isin(allowed_cities)]

    for city in df_ba['city']:
        vals = df_ba[df_ba['city'] == city].iloc[0]
        fig = px.bar(x=['before', 'after'], y=[vals['before'], vals['after']], title=f'Avg Flow Before/After Holidays for {city}', labels={'x':'Period','y':'Avg Flow'})
        fig.write_image(os.path.join(results_dir, 'city_before_after_holiday', f'{city}.png'))

    # 5) Monthly Tourism per city
    tour = df_tour.copy()
    tour_city = tour.groupby(['SHAHR', pd.Grouper(key='date', freq='M')])['flow'].sum().reset_index().rename(columns={'SHAHR':'city'})

    # Filter tourism data for notable cities
    tour_city = tour_city[tour_city['city'].isin(allowed_cities)]

    for city in tour_city['city'].unique():
        df_t = tour_city[tour_city['city'] == city]
        fig = plot_time_series(df_t, 'date', 'flow', f'Monthly Tourism Flow for {city}')
        fig.write_image(os.path.join(results_dir, 'city_tourism_monthly', f'{city}.png'))

    # 6) City-Level Entries over different time scales
    entries_only = entries_exits[['date','city','entries']].copy()

    # Filter entries data for notable cities
    entries_only = entries_only[entries_only['city'].isin(allowed_cities)]

    # daily entries
    for city in entries_only['city'].unique():
        df_e = entries_only[entries_only['city']==city]
        fig = plot_time_series(df_e, 'date', 'entries', f'Daily Entries for {city}')
        fig.write_image(os.path.join(results_dir, 'city_entries_daily', f'{city}.png'))
    # monthly entries
    entries_monthly = entries_only.set_index('date').groupby([pd.Grouper(freq='M'),'city'])['entries'].sum().reset_index()
    for city in entries_monthly['city'].unique():
        df_e = entries_monthly[entries_monthly['city']==city]
        fig = plot_time_series(df_e, 'date', 'entries', f'Monthly Entries for {city}')
        fig.write_image(os.path.join(results_dir, 'city_entries_monthly', f'{city}.png'))
    # 6-month entries
    entries_6m = entries_only.set_index('date').groupby([pd.Grouper(freq='6M'),'city'])['entries'].sum().reset_index()
    for city in entries_6m['city'].unique():
        df_e = entries_6m[entries_6m['city']==city]
        fig = plot_time_series(df_e, 'date', 'entries', f'Semiannual Entries for {city}')
        fig.write_image(os.path.join(results_dir, 'city_entries_6M', f'{city}.png'))

    # Combined semiannual entries for all cities
    fig_6m_all = px.line(entries_6m, x='date', y='entries', color='city', title='Semiannual Entries Over Time by City')
    fig_6m_all.write_html(os.path.join(output_dir, 'city_entries_6M.html'))

    # yearly entries
    entries_yearly = entries_only.set_index('date').groupby([pd.Grouper(freq='Y'),'city'])['entries'].sum().reset_index()
    for city in entries_yearly['city'].unique():
        df_e = entries_yearly[entries_yearly['city']==city]
        fig = plot_time_series(df_e, 'date', 'entries', f'Yearly Entries for {city}')
        fig.write_image(os.path.join(results_dir, 'city_entries_yearly', f'{city}.png'))

    print(f"Generated outputs in {output_dir}")

if __name__ == '__main__':
    main()