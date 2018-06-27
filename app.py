import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np
import os.path
import bubblemap as bm
import line as ln

app = dash.Dash()

bubblemap_data = bm.getData()
line_global_data = ln.getGlobalData()
line_country_data = ln.getData()

app.layout  = html.Div([

    html.Div([
        dcc.Graph(id='bubblemap'),

        html.Div([
            dcc.Slider(
                id='bubblemap_slider',
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
                }
            )
            ], style={'margin-left': '300px', 'margin-right': '300px'}),
    ], style={'width': '100%', 'height': '600px', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='line'),

        html.Div([
            dcc.Dropdown(
                id='line_dropdown',
                options=ln.getOptions(),
                value='Global'
            )
        ], style={'margin-left': '120px', 'margin-right': '120px'}),

        html.Div([
            dcc.RangeSlider(
                id='line_daterange',
                marks={i: '{}'.format(i) for i in range(1850, 2014, 10)},
                min=1850,
                max=2013,
                step=1,
                value=[1850, 2013]
            )
        ], style={'margin-left': '120px', 'margin-right': '120px'}),

    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
])

@app.callback(
    dash.dependencies.Output('bubblemap', 'figure'),
    [dash.dependencies.Input('bubblemap_slider', 'value')])
def update_bubblemap(year): 
    return bm.getFigure(bubblemap_data, year)

@app.callback(dash.dependencies.Output('line', 'figure'),
              [dash.dependencies.Input('line_daterange', 'value'),
               dash.dependencies.Input('line_dropdown', 'value')])
def update_line(date, country): 
    if country == 'Global':
        return ln.getFigure(line_global_data, country, date[0], date[1])
    else:
        return ln.getFigure(line_country_data, country, date[0], date[1])

if __name__ == '__main__':
    app.run_server(debug=True)

