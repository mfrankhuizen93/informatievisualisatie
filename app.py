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
import co2 as co

app = dash.Dash()

bubblemap_data = bm.getData()
line_global_data = ln.getGlobalData()
line_country_data = ln.getData()
co2_global_data = co.getData()

app.layout  = html.Div([

    html.H1('Temperature change by Laura, Ossip and Michelle',
            style={
                'textAlign': 'center'
            }),

    html.Div([
        dcc.RangeSlider(
            id='daterange',
            marks={i: '{}'.format(i) for i in range(1850, 2014, 10)},
            min=1850,
            max=2013,
            step=1,
            value=[1850, 2013]
        )
    ], style={'margin-left': '300px', 'margin-right': '300px', 'height': '50px'}),

    html.Div([
        dcc.Graph(id='bubblemap'),
    ], style={'width': '80%', 'display': 'inline-block'}),

    html.Div([
            html.Div([
                dcc.Graph(id='line'),

                html.Div([
                    dcc.Dropdown(
                        id='line_dropdown',
                        options=ln.getOptions(),
                        value='Global'
                    )
                ], style={'margin-left': '120px', 'margin-right': '120px'}),
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

            html.Div([
                dcc.Graph(id='co2'),
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ], style={'width': '100%', 'display': 'inline-block'})
])

@app.callback(dash.dependencies.Output('bubblemap', 'figure'),
                [dash.dependencies.Input('daterange', 'value')])
def update_bubblemap(date): 
    return bm.getFigure(bubblemap_data, date[0], date[1])

@app.callback(dash.dependencies.Output('line', 'figure'),
                [dash.dependencies.Input('daterange', 'value'),
                dash.dependencies.Input('line_dropdown', 'value')])
def update_line(date, country): 
    if country == 'Global':
        return ln.getFigure(line_global_data, country, date[0], date[1])
    else:
        return ln.getFigure(line_country_data, country, date[0], date[1])

@app.callback(dash.dependencies.Output('co2', 'figure'),
              [dash.dependencies.Input('daterange', 'value')])
def update_co2(date): 
        return co.getFigure(co2_global_data, date[0], date[1])

if __name__ == '__main__':
    app.run_server(debug=True)

