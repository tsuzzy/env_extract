import pandas as pd
import xarray as xr
import sys

def merge_data(year, month):
    '''
    Merge daily environmental values at quarter-grid sample points
    '''
    solar_month = [1,3,5,7,8,10,12]
    lunar_month = [4,6,9,11]
    if int(year) % 4 == 0: # leap year
        max_day = 29
    else:
        max_day = 28
    if int(month) in solar_month:
        max_day = 31
    elif int(month) in lunar_month:
        max_day = 30
    
    host = None # the df which holds all records of the current month
    for day in range(1, max_day+1):
        filename = f'oisst-avhrr-v02r01.{year}{month.zfill(2)}{str(day).zfill(2)}.nc'
        data = xr.open_dataset(filename, engine='netcdf4')
        df = data.to_dataframe().reset_index().drop(['anom','err','ice','time','zlev'],axis=1)
        if day == 1:
            host = df.rename(columns={'sst':'sst_1'})
        else:
            host['sst_'+str(day)] = host.merge(df, how='left', on=['lat','lon'])['sst'].values
        print(f'Processing day {day} out of {max_day} days...')
    
    return host

def calculate_min_max_mean(df):
    df['min'] = df.iloc[:, 2:14].min(axis=1)
    df['max'] = df.iloc[:, 2:14].max(axis=1)
    df['mean'] = df.iloc[:, 2:14].mean(axis=1)

    return df

if __name__ == "__main__":
    merged_df = merge_data(sys.argv[1], sys.argv[2])
    month_data = calculate_min_max_mean(merged_df)
    month_data.to_csv(f'./temp_data/SST{sys.argv[1]}{sys.argv[2].zfill(2)}.csv', index=False)


'''(Done) To-do: find ways to manipulate multiple nc datasets'''
'''(Done) To-do: run the script to test merge_data'''
'''(Done) To-do: calculate mean, max, min at each geo point'''