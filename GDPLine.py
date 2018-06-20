from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
from numpy import arange,array,ones
import os.path
import time
from scipy import stats

start_time = time.time()
continent_data = {}
pd.options.mode.chained_assignment = None

def getDataByDateRange(df, df_gdp, start = 1867, end = 2013):
    # Create a trace
    data = []

    y_as = df[(df['Country'] == 'Netherlands') & (df['dt'] > start) & (df['dt'] <= end)]['AverageTemperature']
    x_as = df[(df['Country'] == 'Netherlands') & (df['dt'] > start) & (df['dt'] <= end)]['dt']
    xi = arange(0,len(df[(df['Country'] == 'Netherlands') & (df['dt'] > start) & (df['dt'] <= end)]['dt']))
        
    # Generated linear fit
    slope, intercept, r_value, _, _ = stats.linregress(xi,y_as)

    temp = []
    for i in xi:
        line = slope*i+intercept
        temp.append(line)

    trace1 = go.Scatter(
                      x=x_as,
                      y=y_as,
                      mode='markers',
                      marker=go.Marker(color='rgb(255, 127, 14)'),
                      name='Data'
                      )

    trace2 = go.Scatter(
                      x=x_as,
                      y=temp,
                      mode='lines',
                      marker=go.Marker(color='rgb(31, 119, 180)'),
                      name='Fit'
                      )

    data.append(trace1)
    data.append(trace2)

    return data

def getContinent(df):
    c = pd.read_csv('data/CountriesInContinent.csv')

    continents = c['Continent'].unique();

    for continent in continents:
        continent_data[continent] = df[df['Country'].isin(list(c[c['Continent']=='Europe']['Country']))]

def removeUnlistedCountries(df):
    gdp = pd.read_csv('data/GDPPerCountry.csv')
    countries = gdp['country'].unique()
    return df[df['Country'].isin(countries)] 

def getAnnualGDPGrowth():
    df_gdp = pd.read_csv('data/GDPPerCountry.csv')
    df_gdp['date'] = pd.to_datetime(df_gdp['date'], format='%Y-%m-%d')
    df_gdp['date'] = pd.DatetimeIndex(df_gdp['date']).year
    return df_gdp

def getFigure(df, year = 1750):
    # data = getDataPerYear(df, year)
    # Edit the layout
    layout = dict(title = 'Average High and Low Temperatures in New York',
                  xaxis = dict(title = 'Month'),
                  yaxis = dict(title = 'Temperature (degrees F)'),
                )
    return dict( data=data, layout=layout )    

def createScatter(data, country = 'Netherlands'):
    print("--- %s seconds --- Started creating GDP- and Temperaturegrowth by year " % (time.time() - start_time))

    layout = dict(title = 'Average High and Low Temperatures in New York',
                  xaxis = dict(title = 'Month'),
                  yaxis = dict(title = 'Temperature (degrees F)'),
                )

    fig = dict(data=data, layout=layout)
    plot(fig, filename='climate_change_line.html' )

def getData():
    if os.path.isfile('data/df_r.csv'):
        df = pd.read_csv('data/df_gdp.csv')
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
        df = df.groupby([pd.Grouper(key='dt', freq='1Y'), 'Country']).mean().reset_index()
        print("--- %s seconds --- Grouped all by five years" % (time.time() - start_time))

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]
        print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))
        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))
        df.to_csv('data/df_gdp.csv')

    df = removeUnlistedCountries(df)
    return df

if __name__ == '__main__':
    df = getData()
    df_gdp = getAnnualGDPGrowth()
    # df = calculateTemperatureGrowth(df)

    # print(df.head(100))
    # getContinent(df)
    data = getDataByDateRange(df, df_gdp)
    createScatter(data)

