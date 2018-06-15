import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np
import os.path
import time

app = dash.Dash()
start_time = time.time()

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

    return gltByCity

def getDataPerYear(year = 1750):
    print(year)
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

df = getData()
data = getDataPerYear()

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

fig = dict( data=data, layout=layout )    


app.layout  = html.Div([
    dcc.Graph(id='climate_change_bubblemap', style={"height" : "75vh", "width" : "100%"}),
    dcc.Slider(
        id='my-slider',
        min=1750,
        max=2010,
        step=5,
        value=1750,
        marks={
            1750: {'label': '1750'},
            1802: {'label': '1802'},
            1854: {'label': '1854'},
            1906: {'label': '1906'},
            1958: {'label': '1958'},
            2010: {'label': '2010'}
        },
        updatemode='drag'
    ),
    html.Div(id='slider-output-container')
])

@app.callback(
    dash.dependencies.Output('climate_change_bubblemap', 'figure'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value): 
    layout = dict(
        title = 'Earth Surface Temperature in ' + str(value),
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
    data = getDataPerYear(value)
    fig = dict( data=data, layout=layout )    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

