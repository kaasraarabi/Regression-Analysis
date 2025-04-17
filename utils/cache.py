from joblib import Memory

# configure disk cache
memory = Memory(location='cache_dir', verbose=0)