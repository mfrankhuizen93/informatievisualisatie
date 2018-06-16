from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()
continent_data = {}

def getDataPerYear(df):
    # Create a trace
    data = []
    for country in continent_data['Europe']['Country'].unique():
        trace = go.Scatter(
            x = df[(df['Country'] == country)]['dt'],
            y = df[(df['Country'] == country)]['AverageTemperature'],
            mode = 'line',
            name = country
        )

        data.append(trace)


    return data

def getContinent(df):
    c = pd.read_csv('data/CountriesInContinent.csv')

    continents = c['Continent'].unique();

    for continent in continents:
        continent_data[continent] = df[df['Country'].isin(list(c[c['Continent']=='Europe']['Country']))]



def getFigure(df, year = 1750):
    data = getDataPerYear(df, year)
    layout = dict(
        title = 'Earth Surface Temperature in ' + str(year),
        showlegend = True,
        geo = dict(
            projection=dict( type='natural earth' ),
            showland = True,
            landcolor = 'rgb(65, 174, 118)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showocean= True,
            oceancolor = 'rgb(116, 169, 207)'
        ),
    )
    return dict( data=data, layout=layout )    

def createScatter(data, country = 'Netherlands'):
    print("--- %s seconds --- Started creating bubbleMap " % (time.time() - start_time))

    layout = dict(
            title = 'Climate Change: Earth Surface Temperature Scatter ' + country,
            showlegend = True,
        )

    fig = dict(data=data, layout=layout)
    plot(fig, filename='climate_change_scatter.html' )

def getData():
    if os.path.isfile('data/df_ry.csv'):
        df = pd.read_csv('data/df_country.csv')
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
        df.to_csv('data/df_country.csv')

    return df

if __name__ == '__main__':
    df = getData()
    getContinent(df)
    data = getDataPerYear(df)
    createScatter(data)

