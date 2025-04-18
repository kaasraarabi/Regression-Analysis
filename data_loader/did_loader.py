import pandas as pd
from utils.errors import InvalidDID
import jdatetime

def load_did_all(path: str) -> pd.DataFrame:
    """
    Load DID-ALL.csv, parse DID into axis, year, month, day, and create a date column.
    Raises InvalidDID on malformed entries.
    """
    df = pd.read_csv(path, dtype={"DID": str, "ALL": int})
    # extract axis (string) and date parts
    parts = df['DID'].str.extract(r'(?P<axis>\d{6})(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})')
    if parts.isnull().any().any():
        raise InvalidDID("Malformed DID entries in DID-ALL.csv")
    # preserve axis as string, convert year/month/day to int for date handling
    parts[['year', 'month', 'day']] = parts[['year', 'month', 'day']].astype(int)
    df = df.join(parts)
    # Convert Jalali date to Gregorian date
    df['date'] = df.apply(lambda row: jdatetime.date(row['year'], row['month'], row['day']).togregorian(), axis=1)
    df['date'] = pd.to_datetime(df['date'])
    return df
