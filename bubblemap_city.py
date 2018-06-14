from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()
gltCities = ""

def getDataPerYear(df, year):
    limits = [(41, 51), (31, 40), (21, 30), (11, 20), (1, 10), (-10, 0), (-20, -11), (-30, -21), (-40, -31), (-50, -41)]
    colors = ['rgb(165,0,38)','rgb(215,48,39)','rgb(244,109,67)','rgb(253,174,97)','rgb(254,224,144)','rgb(224,243,248)','rgb(171,217,233)','rgb(116,173,209)','rgb(69,117,180)','rgb(49,54,149)']
    data = []

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[(df['AverageTemperature'] > lim[0]) & (df['AverageTemperature'] < lim[1])]

        trace = dict(
            type = 'scattergeo',
            locationmode = 'world',
            lon = df_sub[ (df_sub['dt'] == year)]['Longitude'],
            lat = df_sub[ (df_sub['dt'] == year)]['Latitude'],
            text = df_sub[ (df_sub['dt'] == year)]['City'] + '<br>Average temperature ' + (df_sub[ (df_sub['dt'] == year)]['AverageTemperature']).astype(str)+' degrees',
            hoverinfo = 'text',
            marker = dict(
                size = 15,
                color = colors[i],
                line = dict(width=0.0, color='rgb(40,40,40)'),
                sizemode = 'area'
            ), 

            name = '{0} - {1}'.format(lim[1], lim[0])
        )

        data.append(trace)

    return data

def createBubblemap(df):
    print("--- %s seconds --- Started creating bubbleMap " % (time.time() - start_time))

    year = 2000

    data = getDataPerYear(df, year) 

    layout = dict(
            title = 'Titel hier',
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

    fig = dict(data=data, layout=layout)
    plot(fig, filename='bubbleMap.html' )

def getData():
    if os.path.isfile('data/df.csv'):
        gltByCity = pd.read_csv('data/df.csv')
        print("--- %s seconds --- Getting optimized dataset " % (time.time() - start_time))
    else:
        # Reading the dataset and storing it
        gltByCity = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
        print("--- %s seconds --- Read dataset" % (time.time() - start_time))

        # Remove all empty elements
        gltByCity = gltByCity.dropna()
        print("--- %s seconds --- Dropped empty rows" % (time.time() - start_time))

        # Cast string to datetime
        gltByCity['dt'] = pd.to_datetime(gltByCity['dt'], format='%Y-%m-%d')
        print("--- %s seconds --- Converted dt to datetime" % (time.time() - start_time))

        # Merge all monthly items to one year item
        gltByCity = gltByCity.groupby(['City', 'Country', 'Longitude', 'Latitude', pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

        print("--- %s seconds --- Grouped all by one year" % (time.time() - start_time))

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        gltByCity = gltByCity[pd.DatetimeIndex(gltByCity['dt']).year.isin(years)]
        print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))

        # Remove month and day from full date 
        gltByCity['dt'] = pd.DatetimeIndex(gltByCity['dt']).year
        print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))

        gltByCity['Latitude'] = np.where(gltByCity['Latitude'].str[-1:] =='S', '-' + gltByCity['Latitude'].str[:-1], gltByCity['Latitude'].str[:-1])
        gltByCity['Longitude'] = np.where(gltByCity['Longitude'].str[-1:] =='W', '-' + gltByCity['Longitude'].str[:-1], gltByCity['Longitude'].str[:-1])

        gltByCity.to_csv('data/df.csv')

    createBubblemap(gltByCity)

if __name__ == '__main__':
    getData()
