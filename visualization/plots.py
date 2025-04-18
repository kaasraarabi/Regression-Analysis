import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
import jdatetime

# Visualization functions for traffic analysis

def plot_regional_traffic(aggregated_df: pd.DataFrame, metadata_df: pd.DataFrame) -> Figure:
    """
    Bar chart of total traffic per province.
    aggregated_df must have columns ['axis', 'ALL'] for total flow.
    metadata_df must have ['axis', 'province'].
    """
    # ensure axis dtype matches metadata axis (string)
    aggregated_df = aggregated_df.copy()
    aggregated_df['axis'] = aggregated_df['axis'].astype(str)
    df = aggregated_df.merge(metadata_df[['axis', 'province']], on='axis', how='left')
    summary = df.groupby('province')['ALL'].sum().reset_index()
    fig = px.bar(summary, x='province', y='ALL', title='Regional Traffic Trends', labels={'ALL':'Total Vehicles', 'province':'Province'})
    return fig


def plot_time_series(df: pd.DataFrame, date_col: str, value_col: str, title: str) -> Figure:
    """
    Line chart of a time series for a given value_col.
    df should contain date_col and value_col.
    """
    # convert Gregorian dates to Jalali date strings
    df_copy = df.copy()
    df_copy['jalali_date'] = df_copy[date_col].apply(lambda d: jdatetime.date.fromgregorian(date=d).strftime('%Y-%m-%d'))
    fig = px.line(df_copy, x='jalali_date', y=value_col, title=title)
    return fig


def plot_holiday_vs_weekday(df: pd.DataFrame) -> Figure:
    """
    Bar chart comparing holiday vs weekday flows per axis or city.
    df must have columns ['axis' or 'city', 'weekday_flow', 'holiday_flow'].
    """
    index_col = 'axis' if 'axis' in df.columns else 'city'
    melted = df.melt(id_vars=index_col, value_vars=['weekday_flow', 'holiday_flow'], var_name='type', value_name='flow')
    fig = px.bar(melted, x=index_col, y='flow', color='type', barmode='group', title='Holiday vs Weekday Traffic')
    return fig


def plot_imbalance_time_series(df: pd.DataFrame) -> Figure:
    """
    Line chart of entries-exits imbalance over time for each city.
    df must have ['date', 'city', 'imbalance', 'smoothed_imbalance'].
    """
    # plot smoothed imbalance
    fig = px.line(df, x='date', y='smoothed_imbalance', color='city', title='Smoothed Imbalance Over Time')
    return fig


def plot_tourism_heatmap(df: pd.DataFrame) -> Figure:
    """
    Calendar heatmap of daily flows for tourism hubs.
    df must have ['date', 'flow', 'is_hub'].
    """
    hubs = df[df['is_hub']]
    fig = px.density_heatmap(hubs, x=hubs['date'].dt.month, y=hubs['date'].dt.day,
                               z='flow', facet_col='SHAHR', title='Tourism Hub Daily Heatmap', facet_col_spacing=0.01)
    fig.update_layout(xaxis_title='Month', yaxis_title='Day')
    return fig
