import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np
import os.path
import bubblemap as bm

app = dash.Dash()

data = bm.getData();
fig = bm.getFigure(data, 2010)

app.layout  = html.Div([
    dcc.Graph(id='bubblemap'),
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
        },
        # updatemode='drag'
    )
])

@app.callback(
    dash.dependencies.Output('bubblemap', 'figure'),
    [dash.dependencies.Input('bubblemap_slider', 'value')])
def update_output(year): 
    return bm.getFigure(data, year)

if __name__ == '__main__':
    app.run_server(debug=True)

