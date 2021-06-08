import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

def reduce_mem_usage(df, obj_to_cat=False, inplace=True):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.
        obj_to_cat: turn 'object' cols to 'category'
        inplace: inplace dataframe to not mess with original df.
    """
    if not inplace:
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
    if not inplace:
        return df



def get_val_test_increments(end_date, test_start, train_years = 5,intervals = 'month'):
    #TODO: val not working
    #TODO: '2week' interval
    #INPUTS:
        #end_date: (str 'yyyy-mm-dd') final date of testing
        #test_start: (str 'yyyy-mm-dd') first date of testing
        #train_years: (int) how many years of data to use in training
        #interval: ('month' or 'year') getting a new interval every month

    result = []

    #Getting DateTime format of last day
    end_y, end_m, end_d = [int(i) for i in end_date.split('-')]
    end_date = datetime.date(end_y, end_m, end_d)#(2010, 8, 1)

    #Getting DateTime format of first testing day
    start_y, start_m, start_d = [int(i) for i in test_start.split('-')]
    current = datetime.date(start_y, start_m, start_d)#(2010, 8, 1)

    TEST_DATES = []
    while current <= end_date:
        if intervals == 'month':
            next_interval = current + relativedelta(months=1)
        elif intervals == 'year':
            next_interval = current + relativedelta(years=1)
        train_start = current - relativedelta(years=train_years)

        if next_interval > end_date:
            result.append((train_start.isoformat(), current.isoformat(), end_date.isoformat()))
        else:
            result.append((train_start.isoformat(), current.isoformat(), next_interval.isoformat()))
        current = next_interval
    return result
