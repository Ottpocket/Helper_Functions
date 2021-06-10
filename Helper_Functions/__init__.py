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



def get_val_test_increments(end_date, test_start, train_months = 6,intervals = 'month'):
    '''
    Outputs a list of tuples of (train_start, test_start, test_end).
    Each tuple increments by the either 1 year or 1 month.
    INPUTS:
        end_date: ("yyyy-mm-dd") final day of testing
        test_start: ("yyyy-mm-dd") beginning day of testing
        train_months: (int)  # of months to train before test_start
        intervals: ('year' or 'month') the difference between train_start in
            2 consecutive tuples.  i.e. 2019-01-01 to 2019-02-01 or
                                        2019-01-01 to 2020-01-01
    '''
    #TODO: val not working
    #TODO: '2week' interval

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
        train_start = current - relativedelta(years=train_months)

        if next_interval > end_date:
            result.append((train_start.isoformat(), current.isoformat(), end_date.isoformat()))
        else:
            result.append((train_start.isoformat(), current.isoformat(), next_interval.isoformat()))
        current = next_interval
    return result
