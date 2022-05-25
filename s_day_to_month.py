from os.path import exists
import sys
import xarray as xr
import datetime
from day_to_month import calculate_min_max_mean


def get_file(year, month, day):
    # fillday = str(day).zfill(3)
    day_of_year = datetime.datetime(year, month, day).strftime('%j')
    filename = f'SP_D{year}{day_of_year}_Map_SATSSS_data_1day.nc'
    if exists(filename): # in case the record of the day does not exist
        data = xr.open_dataset(filename, engine='netcdf4')
        df = data.to_dataframe().reset_index().drop_duplicates(['lat','lon'], ignore_index=True)
        df = df[['lat','lon','sss']]
    else:
        df = None
    return df

def merge_data(year):
    solar_month = [1,3,5,7,8,10,12]
    lunar_month = [4,6,9,11]

    for month in range(6,13):
        if month in solar_month:
            max_day = 31
        elif month in lunar_month:
            max_day = 30
        else:
            if year % 4 == 0:
                max_day = 29
            else:
                max_day = 28
        
        host = None # the df which holds all records of the current month
        valid_day = 0 # the day of the month which SSS record exists
        for day in range(1, max_day+1):
            df = get_file(year, month, day)
            if df is not None:
                valid_day += 1
                if valid_day == 1:
                    host = df.rename(columns={'sss':'sss'+str(day)})
                else:
                    host['sss_'+str(day)] = host.merge(df, how='left', on=['lat','lon'])['sss'].values
                print(f'Processing day {day} out of {max_day} days...')
        
        calculate_min_max_mean(host, max_day)
        host.to_csv(f'./sal_data/SSS{year}{str(month).zfill(2)}.csv', index=False)
        print(f'Finish month {month}!')
    
    print(f'Year {year} done!!!')
        

if __name__ == "__main__":
    merge_data(int(sys.argv[1]))