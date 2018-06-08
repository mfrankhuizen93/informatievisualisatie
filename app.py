# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

# pandas om de CSV data te laden en te visualiseren
import pandas as pd 

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
#     html.H1(
#         children='Hey guys, welkom bij Informatievisualisatie',
#         style={
#             'textAlign': 'center',
#             'color': colors['text']
#         }
#     ),

#     html.Div(children='Dash: A web application framework for Python.', style={
#         'textAlign': 'center',
#         'color': colors['text']
#     }),

#     dcc.Graph(
#         id='example-graph-2',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
#             ],
#             'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 }
#             }
#         }
#     )

# ])
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


app = dash.Dash()

app.layout = html.Div(children=[
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(gltByCity),
    html.H1(len(gltByCity['City'].unique()))
])

if __name__ == '__main__':
    app.run_server(debug=True)
