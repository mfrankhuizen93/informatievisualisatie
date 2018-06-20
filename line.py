from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()

def getData():
    if os.path.isfile('data/df_ry.csv'):
        df = pd.read_csv('data/df_line.csv')
        print("--- %s seconds --- Getting optimized country dataset " % (time.time() - start_time))
    else:
        # Reading the dataset and storing it
        df = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
        print("--- %s seconds --- Read dataset" % (time.time() - start_time))

        # Remove all empty elements
        df = df.dropna()
        print("--- %s seconds --- Dropped empty rows" % (time.time() - start_time))

        # Cast string to datetime
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')
        print("--- %s seconds --- Converted dt to datetime" % (time.time() - start_time))

        # Merge all monthly items to one year item
        df = df.groupby([pd.Grouper(key='dt', freq='5Y'), 'Country']).mean().reset_index()
        print("--- %s seconds --- Grouped all by five years" % (time.time() - start_time))

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]
        print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))
        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))
        df.to_csv('data/df_line.csv')

    return df

if __name__ == '__main__':
	df = getData()
	print(df.head(100))
