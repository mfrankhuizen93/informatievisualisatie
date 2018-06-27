from plotly.offline import init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os.path
import time

start_time = time.time()

def getDataPerYear(df, year = 1750):
    limits = [(-50, -15)] + [(temp, temp + 1) for temp in (range(-14, 30, 2))] + [(30, 50)]
    colors = ['#add8e6','#bbd3d6','#c6cfc6','#cfcab7','#d7c5a8','#dec09a','#e4bb8d','#e9b580','#edaf74','#f1a968','#f4a35d','#f79c53','#f99648','#fb8e3f','#fc8736','#fe7f2d','#ff7624','#ff6d1c','#ff6314','#ff580c','#ff4c05','#ff3d01','#ff2a00','#ff0000']
    data = []

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[(df['AverageTemperature'] > lim[0]) & (df['AverageTemperature'] < lim[1])]

        trace = dict(
            type = 'scattergeo',
            locationmode = 'world',
            lon = df_sub[ (df_sub['dt'] == year)]['Longitude'],
            lat = df_sub[ (df_sub['dt'] == year)]['Latitude'],
            text = 'Average temperature of ' + df_sub[ (df_sub['dt'] == year)]['City'] + ': <br> ' + (df_sub[ (df_sub['dt'] == year)]['AverageTemperature']).astype(str)+'°C',
            hoverinfo = 'text',
            marker = dict(
                size = 15,
                color = colors[i],
                line = dict(width=0.0, color='rgb(40,40,40)'),
                sizemode = 'area'
            ), 

            name = '{0} - {1}°C'.format(lim[1], lim[0])
        )

        data.append(trace)

    return data

def getFigure(df, year = 1750):
    data = getDataPerYear(df, year)
    layout = dict(
        title = 'Earth Surface Temperature in ' + str(year),
        showlegend = True,
        height = 500,
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

def createBubblemap(df, data, year = 1750):
    print("--- %s seconds --- Started creating bubbleMap " % (time.time() - start_time))

    layout = dict(
            title = 'Climate Change: Earth Surface Temperature Bubblemap',
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
    plot(fig, filename='climate_change_bubblemap.html' )

def getData():
    if os.path.isfile('data/df_city.csv'):
        df = pd.read_csv('data/df_city.csv')
        print("--- %s seconds --- Getting optimized dataset " % (time.time() - start_time))
    else:
        # Reading the dataset and storing it
        df = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
        print("--- %s seconds --- Read dataset" % (time.time() - start_time))

        # Remove all empty elements
        df = df.dropna()
        print("--- %s seconds --- Dropped empty rows" % (time.time() - start_time))

        # Cast string to datetime
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d')
        print("--- %s seconds --- Converted dt to datetime" % (time.time() - start_time))

        # Merge all monthly items to one year item
        df = df.groupby(['City', 'Country', 'Longitude', 'Latitude', pd.Grouper(key='dt', freq='1Y')]).mean().reset_index()

        print("--- %s seconds --- Grouped all by one year" % (time.time() - start_time))

        # Remove all dates not in scope
        years = list(range(1750, 2014))
        df = df[pd.DatetimeIndex(df['dt']).year.isin(years)]
        print("--- %s seconds --- Removed all dates not in scope" % (time.time() - start_time))

        # Remove month and day from full date 
        df['dt'] = pd.DatetimeIndex(df['dt']).year
        print("--- %s seconds --- Removed month and day from full date" % (time.time() - start_time))

        df['Latitude'] = np.where(df['Latitude'].str[-1:] =='S', '-' + df['Latitude'].str[:-1], df['Latitude'].str[:-1])
        df['Longitude'] = np.where(df['Longitude'].str[-1:] =='W', '-' + df['Longitude'].str[:-1], df['Longitude'].str[:-1])

        df.to_csv('data/df_city.csv')

    return df

if __name__ == '__main__':
    df = getData()
    data = getDataPerYear(df, 2010)
    createBubblemap(df, data, 2010)

