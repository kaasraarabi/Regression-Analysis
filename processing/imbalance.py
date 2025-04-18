import pandas as pd

def compute_entries_exits(df_did: pd.DataFrame, metadata: dict) -> pd.DataFrame:
    """
    Map raw DID data to city-level entries and exits per day.
    metadata: dict axis->metadata with 'origin_fa' and 'destination_fa'.
    Returns DataFrame with columns [date, city, entries, exits].
    """
    df = df_did.copy()
    # use Persian city names from metadata
    df['origin'] = df['axis'].astype(str).map(lambda x: metadata.get(x, {}).get('origin_fa', 'Unknown'))
    df['destination'] = df['axis'].astype(str).map(lambda x: metadata.get(x, {}).get('destination_fa', 'Unknown'))
    entries = df.groupby(['date', 'destination'])['ALL'].sum().reset_index().rename(columns={'destination': 'city', 'ALL': 'entries'})
    exits = df.groupby(['date', 'origin'])['ALL'].sum().reset_index().rename(columns={'origin': 'city', 'ALL': 'exits'})
    merged = pd.merge(entries, exits, on=['date', 'city'], how='outer').fillna(0)
    return merged


def compute_imbalance(df_entries_exits: pd.DataFrame) -> pd.DataFrame:
    """
    Compute imbalance = entries - exits for each city per day.
    Returns DataFrame with an 'imbalance' column.
    """
    df = df_entries_exits.copy()
    df['imbalance'] = df['entries'] - df['exits']
    return df


def smooth_spikes(df: pd.DataFrame, window: int = 90) -> pd.DataFrame:
    """
    Smooth spikes in imbalance by rolling mean over given window (days).
    Adds 'smoothed_imbalance' column.
    """
    df_sorted = df.sort_values(['city', 'date'])
    df_sorted['smoothed_imbalance'] = df_sorted.groupby('city')['imbalance'].transform(
        lambda x: x.rolling(window, center=True, min_periods=1).mean()
    )
    return df_sorted