#!/usr/bin/env python
# encoding: utf-8
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as dhc
import plotly.graph_objs as go
from dash.dependencies import Input, Output


filename = 'daily-house-deal.csv'
df = pd.read_csv(filename)
df = df[df.number > 0]
districts = df.district.unique()
house_types = df.house_type.unique()


app = dash.Dash(
    'Chengdu House',
    sharing=True,
    url_base_pathname='/'
)
server = app.server

app.layout = dhc.Div([
    dhc.H1('成都各区每天房子销售情况'),
    dhc.Label('请选择地区及房子类型：'),
    dcc.Dropdown(
        id='select-district-house-type',
        options=[
            {
                'label': f'{district}-{house_type}',
                'value': f'{district}-{house_type}',
            }
            for district in districts
            for house_type in house_types
        ],
        # value=[],
        multi=True
    ),
    dcc.Graph(
        id='house-sales-count',
        # figure={
        #    'data': data,
        # }
    ),
])


@app.callback(
    Output('house-sales-count', 'figure'),
    [Input('select-district-house-type', 'value')]
)
def update_house_sales_count(district_house_type):
    if not district_house_type:
        district_house_type = []

    data = []

    for district, house_type in [s.split('-') for s in district_house_type]:
        data.append(
            go.Scatter(
                x=df.loc[(df.district == district) & (df.house_type == house_type)]['date'].apply(lambda x: pd.to_datetime(x).date().strftime('%Y-%m-%d')).unique(),
                y=df.loc[(df.district == district) & (df.house_type == house_type)]['number'],
                mode='lines',
                text=f'{district}-{house_type}',
                name=f'{district}-{house_type}',
            )
        )

    return {'data': data}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
