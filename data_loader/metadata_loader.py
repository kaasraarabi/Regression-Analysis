import pandas as pd
from functools import lru_cache

def load_metadata(path: str) -> pd.DataFrame:
    """
    Load codeMehvar.csv and return DataFrame with axis metadata.
    Columns: Code-mehvar, Name-Mehvar, Ostan, origin, destination, origin_en, destination_en, filename
    """
    df = pd.read_csv(path, dtype=str)
    df.rename(columns={
        'Code-mehvar': 'axis',
        'Name-Mehvar': 'name',
        'Ostan': 'province',
        'origin': 'origin_fa',
        'destination': 'destination_fa',
        'origin_en': 'origin_en',
        'destination_en': 'destination_en'
    }, inplace=True)
    return df

@lru_cache(maxsize=None)
def get_axis_metadata(metadata_path: str) -> dict:
    """
    Load metadata and return a dict mapping axis code to its metadata dict.
    """
    df = load_metadata(metadata_path)
    df.set_index('axis', inplace=True)
    return df.to_dict('index')
