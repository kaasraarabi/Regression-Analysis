import pandas as pd


def aggregate_by_period(df: pd.DataFrame, date_col: str = 'date', value_col: str = 'ALL', period: str = 'D') -> pd.DataFrame:
    """
    Aggregate traffic by given period: 'D' daily, 'M' monthly, 'Q' seasonal(quarterly), 'Y' yearly.
    Returns DataFrame with period index and sum of value_col grouped by axis.
    """
    df = df.copy()
    df.set_index(date_col, inplace=True)
    # map 'M' to 'ME' to avoid pandas deprecation warning
    freq = 'ME' if period == 'M' else period
    grouped = df.groupby([pd.Grouper(freq=freq), 'axis'])[value_col].sum().reset_index()
    return grouped


def holiday_vs_weekday_flow(df: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    """
    Compare total flows on holidays vs weekdays per axis.
    Returns DataFrame with axis, holiday_flow, weekday_flow.
    """
    merged = df.merge(calendar, on='date', how='left')
    result = merged.groupby(['axis', 'is_holiday'])[ 'ALL'].sum().unstack(fill_value=0)
    result.columns = ['weekday_flow', 'holiday_flow'] if 0 in result.columns and 1 in result.columns else result.columns
    result = result.reset_index()
    return result


def day_before_after_holiday_flow(df: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    """
    Compute traffic flows on the day before and after each holiday for each axis.
    Returns DataFrame with axis, flow_before, flow_after averaged across holidays.
    """
    cal = calendar[calendar.is_holiday == 1]
    days = pd.DataFrame({
        'date': cal['date'],
        'before': cal['date'] - pd.Timedelta(days=1),
        'after': cal['date'] + pd.Timedelta(days=1)
    })
    df_indexed = df.set_index('date')
    records = []
    for _, row in days.iterrows():
        axis_before = df_indexed.loc[row['before']].groupby('axis')['ALL'].sum().rename('before') if row['before'] in df_indexed.index else pd.Series(dtype=int)
        axis_after = df_indexed.loc[row['after']].groupby('axis')['ALL'].sum().rename('after') if row['after'] in df_indexed.index else pd.Series(dtype=int)
        temp = pd.concat([axis_before, axis_after], axis=1).fillna(0)
        records.append(temp)
    if records:
        combined = pd.concat(records)
        avg = combined.groupby(combined.index).mean().reset_index().rename(columns={'before':'flow_before', 'after':'flow_after'})
    else:
        avg = pd.DataFrame(columns=['axis', 'flow_before', 'flow_after'])
    return avg
