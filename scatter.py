from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()
ContinentCountries2 = pd.read_csv('data/ContinentCountries3.csv')
Africa = ContinentCountries2[ContinentCountries3['Continent'] == 'Africa']
Europe = ContinentCountries2[ContinentCountries3['Continent'] == 'Europe']
NorthAmerica = ContinentCountries2[ContinentCountries3['Continent'] == 'North America']
SouthAmerica =  ContinentCountries2[ContinentCountries3['Continent'] == 'South America']
Oceania =  ContinentCountries2[ContinentCountries3['Continent'] == 'Oceania']
Asia =  ContinentCountries2[ContinentCountries3['Continent'] == 'Asia']

#df = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
def getData():
    if os.path.isfile('data/GlobalLandTemperaturesByCountryOptimized.csv'):
        gltByCountry = pd.read_csv('data/GlobalLandTemperaturesByCountryOptimized.csv')
        print("--- %s seconds --- Getting optimized dataset " % (time.time() - start_time))
    else:
        # Reading the dataset and storing it
        gltByCountry = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
        print("--- %s seconds --- Read dataset" % (time.time() - start_time))

        # Remove all empty elements
        gltByCountry = gltByCountry.dropna()
        print("--- %s seconds --- Dropped empty rows" % (time.time() - start_time))

        # Cast string to datetime
        gltByCountry['dt'] = pd.to_datetime(gltByCountry['dt'], format='%Y-%m-%d')
        print("--- %s seconds --- Converted dt to datetime" % (time.time() - start_time))

        # Merge all monthly items to one year item
        gltByCountry = gltByCountry.groupby(['Country', pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

        print("--- %s seconds --- Grouped all by one year" % (time.time() - start_time))

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        gltByCountry = gltByCountry[pd.DatetimeIndex(gltByCountry['dt']).year.isin(years)]
        print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))

        # Remove month and day from full date 
        gltByCountry['dt'] = pd.DatetimeIndex(gltByCountry['dt']).year
        print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))

if __name__ == '__main__':
    getData()
