import base64

import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

COMPANY_NAME = 'MARTLET SOFTWARE'
VEHICLES = ['SUV1', 'SUV2', 'Truck1']
SUBASSIES_SENSORS = {
    'BRAKING SYSTEM': ['Vibration FL', 'Vibration FR', 'Vibration RL', 'Vibration RR'],
    'ELECTRIC SYSTEM': ['Battery Voltage']
}
SUBASSIES = list(SUBASSIES_SENSORS.keys())

app = dash.Dash('vehicle-data', static_folder='assets')
app.title = COMPANY_NAME

image_filename = 'assets/logo.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Div([html.H1(COMPANY_NAME),
              html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                       style={'width': '200px'}),
              ], className='row', style={'textAlign': 'center'}),

    html.Div([html.H2(id='title'),
              ], className='row', style={'textAlign': 'center'}),

    html.Div([
        html.Label('Vehicles'),
        dcc.Dropdown(
            id='vehicles-dropdown',
            options=[{'label': s, 'value': s} for s in VEHICLES],
            value=VEHICLES[0]
        ),
        html.Hr(),
        html.Label('Subassies'),
        dcc.RadioItems(
            id='subassies-radioitems',
            options=[{'label': s, 'value': s} for s in SUBASSIES],
            value=SUBASSIES[0]
        ),
        html.Hr(),
        html.Label('Sensors'),
        dcc.Dropdown(id='sensors-dropdown',
                     options=[{'label': s, 'value': s} for s in SUBASSIES_SENSORS[SUBASSIES[0]]],
                     value=[],
                     multi=True
                     ),
    ], className='row'),
    html.Hr(),
    html.Div(children=html.Div(id='graphs'),
             className='row',
             # style={'columnCount': 2}
             ),
    dcc.Interval(id='graph-update', interval=5000),
], className="container",
    # style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000}
)


@app.callback(Output('title', component_property='children'), [Input('vehicles-dropdown', 'value')])
def update_vehicle(selected_dropdown_value):
    return selected_dropdown_value


@app.callback(Output('sensors-dropdown', 'options'), [Input('subassies-radioitems', 'value')])
def update_subassy(selected_value):
    options = [{'label': s, 'value': s} for s in SUBASSIES_SENSORS[selected_value]]
    return options


@app.callback(Output('sensors-dropdown', 'value'), [Input('subassies-radioitems', 'value')])
def update_subassy(selected_value):
    return SUBASSIES_SENSORS[selected_value]


def get_sensor_data(sensor_name):
    data = {"2018-01-01 01:01": 2.2,
            "2018-01-01 01:02": 2.1,
            "2018-01-01 01:03": 3.1
            }
    return data


@app.callback(Output('graphs', 'children'), [Input('sensors-dropdown', 'value')],
              events=[Event('graph-update', 'interval')])
def update_graph(sensors):
    graphs = []
    class_choice = 'col s6 m6 l6'
    for sensor in sensors:
        sensor_data = get_sensor_data(sensor)
        times = sensor_data.keys()
        data = go.Scatter(
            x=list(times),
            y=list(sensor_data.values()),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
        )

        graphs.append(html.Div(dcc.Graph(
            id=sensor,
            animate=False,
            figure={'data': [data],
                    'layout': go.Layout(xaxis=dict(range=[min(times), max(times)]),
                                        yaxis=dict(range=[0.0, 4.5]),
                                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                                        title='{}'.format(sensor),
                                        images=[dict(
                                            source='/assets/logo.png',
                                            xref="x",
                                            yref="y",
                                            x=0,
                                            y=3,
                                            sizex=2,
                                            sizey=2,
                                            sizing="fill",
                                            opacity=0.5,
                                            layer="above"
                                        )]), }
        ), className=class_choice))

    return graphs


external_css = [
    # "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "/assets/my.css"
]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)
