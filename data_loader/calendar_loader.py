import pandas as pd
import jdatetime

def load_calendar(path: str) -> pd.DataFrame:
    """
    Load calendar.csv with columns [date_int, weekday, is_holiday].
    Returns DataFrame with date (datetime), weekday (str), is_holiday (int).
    """
    df = pd.read_csv(path, header=None, names=['date_int', 'weekday', 'is_holiday'], dtype={'date_int': str, 'weekday': str, 'is_holiday': int})
    # Convert Jalali date_int string to Gregorian date
    df['date'] = df['date_int'].apply(
        lambda s: pd.to_datetime(
            jdatetime.date(int(s[:4]), int(s[4:6]), int(s[6:8])).togregorian()
        )
    )
    return df[['date', 'weekday', 'is_holiday']]
