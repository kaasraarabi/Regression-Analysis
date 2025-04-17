import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, feature_col: str = 'ALL', contamination: float = 0.01) -> pd.DataFrame:
    """
    Flag anomalies in the given feature column using IsolationForest.
    Adds 'anomaly' column: 1 = normal, -1 = anomaly.
    """
    iso = IsolationForest(contamination=contamination, random_state=42)
    df = df.copy()
    values = df[[feature_col]].fillna(0)
    df['anomaly'] = iso.fit_predict(values)
    return df

def cluster_traffic(df: pd.DataFrame, eps: float = 0.5, min_samples: int = 5, feature_cols: list = None) -> pd.DataFrame:
    """
    Cluster traffic patterns per city/date using DBSCAN.
    feature_cols: list of column names to use for clustering.
    Adds 'cluster' column.
    """
    df = df.copy()
    if feature_cols is None:
        # default to ALL or imbalance
        feature_cols = ['ALL'] if 'ALL' in df.columns else df.select_dtypes(include='number').columns.tolist()
    X = df[feature_cols].fillna(0)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    df['cluster'] = db.fit_predict(X)
    return df
