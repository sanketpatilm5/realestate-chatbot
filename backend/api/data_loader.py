import os
import pandas as pd
from django.conf import settings

_df_cache = None

def get_dataset():
    global _df_cache
    if _df_cache is None:
        # dataset/Sample_data.xlsx is one level above backend/
        base_dir = settings.BASE_DIR.parent  # project root that contains dataset/
        file_path = os.path.join(base_dir, 'dataset', 'Sample_data.xlsx')
        _df_cache = pd.read_excel(file_path)
    return _df_cache.copy()
