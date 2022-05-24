import pandas as pd
import xarray as xr
import numpy as np

def merge_data(year, month):
    '''
    Merge daily environmental values at quarter-grid sample points
    '''
    solar_month = [1,3,5,7,8,10,12]
    lunar_month = [4,6,9,11]
    if year % 4 == 0: # leap year
        max_day = 29
    else:
        max_day = 28
    if month in solar_month:
        max_day = 31
    elif month in lunar_month:
        max_day = 30
    
    host = None # the df which holds all records of the current month
    for day in range(1, max_day+1):
        filename = f'oisst-avhrr-v02r01.{year}{str(month).zfill(2)}{str(day).zfill(2)}.nc'
        data = xr.open_dataset(filename, engine='netcdf4')
        df = data.to_dataframe().reset_index().drop(['anom','err','ice','time','zlev'],axis=1)
        if day == 1:
            host = df.rename(columns={'sst':'sst_1'})
        else:
            host['sst_'+str(day)] = host.merge(df, how='left', on=['lat','lon'])['sst'].values
    
    return host



'''(Done) To-do: find ways to manipulate multiple nc datasets'''
'''(Done) To-do: run the script to test merge_data'''
'''To-do: calculate mean, max, min at each geo point'''