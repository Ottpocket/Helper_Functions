import numpy as np
import pandas as pd

def reduce_mem_usage(df, obj_to_cat=False, copy=False):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
        obj_to_cat: turn 'object' cols to 'category'
        copy: copies dataframe to not mess with original df.
    """
    if copy:
        df = df.copy()

    for col in df.columns:
        col_type = df[col].dtype.name
        if 'datetime' in col_type:
            pass
        elif col_type == 'object':
            if obj_to_cat:
                df[col] = df[col].astype('category')
        elif col_type == 'category':
            pass
        else:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    return df
