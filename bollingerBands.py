import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

if __name__ == '__main__':
    dt_start = dt.datetime(2010, 4, 10) 
    dt_end = dt.datetime(2010, 6, 5) 

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_symbols = ["MSFT"]
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_close = d_data['close']
    df_mean = pd.rolling_mean(df_close, 20)
    df_std = pd.rolling_std(df_close, 20)

    df_bands = (df_close - df_mean) / df_std
    df_bands.to_csv('bollinger.csv',',')
    print df_bands

    '''
    with open('bollinger', 'w') as outfile:
        for symbol in ls_symbols:
            for idx, time in enumerate(ldt_timestamps):
            outfile.write("%d,%d,%d,%s,Buy,100,\n" % (time.year, time.month, time.day, symbol))
    '''
    print 'Generating bollinger curves'
    with open('bollinger', 'w') as outfile:
        for band in df_bands:
            outfile.write('%s' % df_bands[band])
            #outfile.write('%s %s %s %s\n' % (band,df_bands[band] )) 
   
