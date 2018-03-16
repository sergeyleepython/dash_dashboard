import base64

import dash
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random

DATAFLOW = {
    'Vibration FL': [0.5],
    'Vibration FR': [0.5],
    'Vibration RL': [0.5],
    'Vibration RR': [0.5],
}

app = dash.Dash('vehicle-data')

max_length = 30
times = deque(maxlen=max_length)
vibration_FL = deque(maxlen=max_length)
vibration_FR = deque(maxlen=max_length)
vibration_RL = deque(maxlen=max_length)
vibration_RR = deque(maxlen=max_length)

data_dict = {
    "Vibration FL": vibration_FL,
    "Vibration FR": vibration_FR,
    "Vibration RL": vibration_RL,
    "Vibration RR": vibration_RR,
}

image_filename = 'images/logo.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Div([
        html.H2('Vehicle Data',
                style={'float': 'left',
                       }),
    ]),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '200px', 'float': 'right'}),
    dcc.Dropdown(id='vehicle-data-name',
                 options=[{'label': s, 'value': s} for s in data_dict.keys()],
                 value=['Vibration FL', 'Vibration FR', 'Vibration RL', 'Vibration RR'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(id='graph-update', interval=5000),
], className="container", style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000})


def update_obd_values(times, vibration_FL, vibration_FR, vibration_RL, vibration_RR):
    times.append(time.time())
    if len(times) == 1:
        # starting relevant values
        vibration_FL.append(0.5)
        vibration_FR.append(0.5)
        vibration_RL.append(0.5)
        vibration_RR.append(0.5)
    else:
        for label, data_deque in data_dict.items():
            l = DATAFLOW[label]
            DATAFLOW[label] = [0.5]
            data_deque.append(sum(l) / float(len(l)))

    return times, vibration_FL, vibration_FR, vibration_RL, vibration_RR


times, vibration_FL, vibration_FR, vibration_RL, vibration_RR = update_obd_values(times,
                                                                                  vibration_FL,
                                                                                  vibration_FR,
                                                                                  vibration_RL,
                                                                                  vibration_RR,
                                                                                  )


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('vehicle-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
)
def update_graph(data_names):
    graphs = []
    update_obd_values(times, vibration_FL, vibration_FR, vibration_RL, vibration_RR)

    class_choice = 'col s6 m6 l6'

    for data_name in data_names:
        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
        )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=False,
            figure={'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(times), max(times)]),
                                                        yaxis=dict(range=[0.0, 4.5]),
                                                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                                                        title='{}'.format(data_name),
                                                        images=[dict(
                                                            source='images/logo.png',
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


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css",
                "my.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)
