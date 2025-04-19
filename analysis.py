import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import matplotlib as mpl

CITY_FOLDER = 'City_Files'
OUTPUT_FOLDER = 'Output_By_Year'
MAP_FILE = 'data/maps/ne_110m_admin_0_countries.shp'
MIN_DAYS_IN_YEAR = 340
MIN_DAYS_IN_MONTH = 25
N_CLUSTERS = 4


ostan_centers = [
    {'city': 'تهران', 'lat': 35.6892, 'lon': 51.3890},
    {'city': 'مشهد', 'lat': 36.2605, 'lon': 59.6168},
    {'city': 'اصفهان', 'lat': 32.6539, 'lon': 51.6660},
    {'city': 'شیراز', 'lat': 29.5918, 'lon': 52.5836},
    {'city': 'تبریز', 'lat': 38.0962, 'lon': 46.2738},
    {'city': 'کرمانشاه', 'lat': 34.3142, 'lon': 47.0650},
    {'city': 'اهواز', 'lat': 31.3203, 'lon': 48.6692},
    {'city': 'رشت', 'lat': 37.2808, 'lon': 49.5832},
    {'city': 'یزد', 'lat': 31.8974, 'lon': 54.3569},
    {'city': 'ارومیه', 'lat': 37.5485, 'lon': 45.0725},
    {'city': 'کرمان', 'lat': 30.2839, 'lon': 57.0834},
    {'city': 'ساری', 'lat': 36.5633, 'lon': 53.0601},
    {'city': 'زاهدان', 'lat': 29.4963, 'lon': 60.8629},
    {'city': 'بندرعباس', 'lat': 27.1832, 'lon': 56.2666},
    {'city': 'قم', 'lat': 34.6399, 'lon': 50.8759},
    {'city': 'بوشهر', 'lat': 28.9220, 'lon': 50.8371},
    {'city': 'ایلام', 'lat': 33.6374, 'lon': 46.4227},
    {'city': 'سنندج', 'lat': 35.3219, 'lon': 46.9862},
    {'city': 'خرمآباد', 'lat': 33.4878, 'lon': 48.3558},
    {'city': 'قزوین', 'lat': 36.2708, 'lon': 50.0041},
    {'city': 'زنجان', 'lat': 36.6765, 'lon': 48.4963},
    {'city': 'اردبیل', 'lat': 38.2498, 'lon': 48.2933},
    {'city': 'همدان', 'lat': 34.7992, 'lon': 48.5146},
    {'city': 'گرگان', 'lat': 36.8416, 'lon': 54.4435},
    {'city': 'شهرکرد', 'lat': 32.3266, 'lon': 50.8644},
    {'city': 'بیرجند', 'lat': 32.8663, 'lon': 59.2211},
    {'city': 'یاسوج', 'lat': 30.6681, 'lon': 51.5877},
    {'city': 'بجنورد', 'lat': 37.4747, 'lon': 57.3290},
    {'city': 'اراک', 'lat': 34.0917, 'lon': 49.6892},
    {'city': 'سمنان', 'lat': 35.5701, 'lon': 53.3973}
]
city_coords = pd.DataFrame(ostan_centers)

all_dfs = []
for row in ostan_centers:
    city = row['city']
    filename = city.replace(' ', '_') + '.csv'
    path = os.path.join(CITY_FOLDER, filename)

    if os.path.exists(path):
        df = pd.read_csv(path)
        df['City'] = city
        df['Year'] = df['Date'].astype(str).str[:4]
        df['Month'] = df['Date'].astype(str).str[:6]
        all_dfs.append(df)

all_data = pd.concat(all_dfs, ignore_index=True)


valid_years = (
    all_data.groupby(['City', 'Year'])['Date']
    .nunique().reset_index(name='Day_Count')
    .query('Day_Count >= @MIN_DAYS_IN_YEAR')
)
filtered = all_data.merge(valid_years[['City', 'Year']], on=['City', 'Year'], how='inner')


days_per_month = (
    filtered.groupby(['City', 'Year', 'Month'])['Date']
    .nunique().reset_index(name='Days_In_Month')
)
invalid_months = days_per_month[days_per_month['Days_In_Month'] < MIN_DAYS_IN_MONTH]
invalid_city_years = invalid_months[['City', 'Year']].drop_duplicates()

filtered = filtered.merge(invalid_city_years, on=['City', 'Year'], how='left', indicator=True)
filtered = filtered[filtered['_merge'] == 'left_only'].drop(columns=['_merge'])


os.makedirs(OUTPUT_FOLDER, exist_ok=True)
years = filtered['Year'].unique()

world = gpd.read_file(MAP_FILE)
iran = world[world['NAME'] == 'Iran']

for year in years:
    yearly = filtered[filtered['Year'] == year]

    pivot_entries = yearly.groupby(['City', 'Month'])['Total_Entries'].sum().unstack(fill_value=0)
    pivot_exits = yearly.groupby(['City', 'Month'])['Total_Exits'].sum().unstack(fill_value=0)
    features_1 = pd.concat([pivot_entries, pivot_exits], axis=1)
    features_1 = features_1.loc[:, sorted(features_1.columns)]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_1)

    kmeans_1 = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init='auto')
    cluster_labels_1 = kmeans_1.fit_predict(features_scaled)

    result_1 = pd.DataFrame({'City': features_1.index, 'Cluster': cluster_labels_1})
    result_1 = result_1.merge(city_coords, left_on='City', right_on='city')

    fig, ax = plt.subplots(figsize=(10, 8))
    iran.plot(ax=ax, color='lightgray')
    sns.scatterplot(data=result_1, x='lon', y='lat', hue='Cluster', palette='tab10', s=100, ax=ax)
    plt.title(f'Cluster of Entries and Exits (Normalized) - {year}')
    plt.savefig(os.path.join(OUTPUT_FOLDER, f'{year}_cluster_io_normalized_map.png'))
    plt.close()

    result_1.to_csv(os.path.join(OUTPUT_FOLDER, f'{year}_cluster_io_normalized.csv'), index=False, encoding='utf-8-sig')

    ratio = yearly.groupby(['City', 'Month'])[['Total_Entries', 'Total_Exits']].sum()
    ratio['Ratio'] = 10 * ratio['Total_Entries'] / (ratio['Total_Exits'] + 1e-5)
    ratio_pivot = ratio['Ratio'].unstack(fill_value=0)

    kmeans_2 = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init='auto')
    cluster_labels_2 = kmeans_2.fit_predict(ratio_pivot)

    result_2 = pd.DataFrame({'City': ratio_pivot.index, 'Cluster': cluster_labels_2})
    result_2 = result_2.merge(city_coords, left_on='City', right_on='city')

    fig, ax = plt.subplots(figsize=(10, 8))
    iran.plot(ax=ax, color='lightgray')
    sns.scatterplot(data=result_2, x='lon', y='lat', hue='Cluster', palette='Set2', s=100, ax=ax)
    plt.title(f'Cluster of Entry/Exit Ratio ×10 - {year}')
    plt.savefig(os.path.join(OUTPUT_FOLDER, f'{year}_cluster_ratio10_map.png'))
    plt.close()

    result_2.to_csv(os.path.join(OUTPUT_FOLDER, f'{year}_cluster_ratio10.csv'), index=False, encoding='utf-8-sig')

print("done")
