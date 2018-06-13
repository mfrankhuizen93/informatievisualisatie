import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

gltByCity = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
gltByCountry = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
gltByMajorCity = pd.read_csv('data/GlobalLandTemperaturesByMajorCity.csv')
gltByState = pd.read_csv('data/GlobalLandTemperaturesByState.csv')
gt = pd.read_csv('data/GlobalTemperatures.csv')

def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
cities = []

for i in range(len(limits)):
    lim = limits[i]
    gltByCity = gltByCity[lim[0]:lim[1]]
    city = dict(
        type = 'scattergeo',
        locationmode = 'world',
        lon = gltByCity['Longitude'],
        lat = gltByCity['Latitude'],
        text = gltByCity['City'],
        marker = dict(
            size = gltByCity['AverageTemperature'],
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)

layout = dict(
        title = '2014 US city populations<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='world',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
py.iplot( fig, validate=False, filename='d3-bubble-map-populations' )


data = [fig]
url_1 = py.plot(data, filename='scatter-for-dashboard', auto_open=False)
py.iplot(data, filename='scatter-for-dashboard')

if __name__ == '__main__':
    app.run_server()

# app.layout = html.Div(children=[
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(gltByState),
#     html.H1(gltByState['State'].unique())
# ])



