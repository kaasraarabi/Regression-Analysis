import pandas as pd
import jdatetime

def load_tourism(path: str) -> pd.DataFrame:
    """
    Load tourism-pro_filtered.csv with columns [SHAHR, START, END, PRO-TOURISM] and flag tourism hubs.
    A city is a hub if >70% of its PRO-TOURISM values > 0.
    """
    df = pd.read_csv(path, dtype={"SHAHR": str, "START": str, "END": str, "PRO-TOURISM": float})
    hub_ratio = df.groupby('SHAHR')['PRO-TOURISM'].apply(lambda x: (x > 0).mean())
    hubs = hub_ratio[hub_ratio > 0.7].index.tolist()
    df['is_hub'] = df['SHAHR'].isin(hubs)
    # Convert Jalali START string to Gregorian date and parse as pandas datetime
    df['date'] = df['START'].apply(
        lambda s: jdatetime.date(int(s[:4]), int(s[4:6]), int(s[6:8])).togregorian()
    )
    df['date'] = pd.to_datetime(df['date'])
    # Rename tourism count column to 'flow'
    df.rename(columns={'PRO-TOURISM': 'flow'}, inplace=True)
    return df
