from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()

def getDataByRange(df, start = 2000, end = 2010):
    limits = [(-5, -0.6), (-0.5, 0.5), (0.6, 1), (2, 5)]
    colors = ['blue', 'transparent', 'orange', 'red']
    data = []

    new = df[df['dt'] == end].set_index(['City', 'Country'])
    old = df[df['dt'] == start].set_index(['City', 'Country'])

    new.reset_index(inplace=True)
    old.reset_index(inplace=True)

    newdf = pd.merge(old, new, on= ["Country", "City", "Longitude", "Latitude"])
    newdf['New'] = newdf['AverageTemperature_y'] - newdf['AverageTemperature_x']

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = newdf[(newdf['New'] > lim[0]) & (newdf['New'] < lim[1])]

        trace = dict(
            type = 'scattergeo',
            locationmode = 'world',
            lon = list(df_sub['Longitude']),
            lat = list(df_sub['Latitude']),
            text = 'Temperature growth in ' + (df_sub['New']).astype(str)+'°C',
            hoverinfo = 'text',
            marker = dict(
                size = 15,
                color = colors[i],
                line = dict(width=0.1, color='white'),
                sizemode = 'area'
            ), 

            name = 'Temperature growth between {0} - {1}°C'.format(lim[0], lim[1])
        )

        data.append(trace)

    return data

def getFigure(df, start = 2000, end = 2010):
    data = getDataByRange(df, start, end)
    layout = dict(
        title = 'Earth Surface Temperature in ' + str(start) + ' - ' + str(end),
        showlegend = True,
        geo = dict(
            projection=dict( type='natural earth' ),
            resolution='50',
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

def getData():
    print("--- %s seconds --- Getting bubblemap data " % (time.time() - start_time))
    if os.path.isfile('data/df_city.csv'):
        df = pd.read_csv('data/df_city.csv')
    else:
        # Reading the dataset and storing it
        df = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')

        # Remove all empty elements
        df = df.dropna()

        # Cast string to datetime
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')

        # Merge all monthly items to one year item
        df = df.groupby(['City', 'Country', 'Longitude', 'Latitude', pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]

        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year

        df['Latitude'] = np.where(df['Latitude'].str[-1:] =='S', '-' + df['Latitude'].str[:-1], df['Latitude'].str[:-1])
        df['Longitude'] = np.where(df['Longitude'].str[-1:] =='W', '-' + df['Longitude'].str[:-1], df['Longitude'].str[:-1])

        df.to_csv('data/df_city.csv')

    print("--- %s seconds --- Finished getting bubblemap data " % (time.time() - start_time))    
    return df

if __name__ == '__main__':
    start = 1850
    end = 2010
    df = getData()
    plot(getFigure(df, start, end), filename='climate_change_bubblemap.html' )
