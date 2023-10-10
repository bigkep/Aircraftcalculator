import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import urllib.parse
import pandas as pd
import base64
import io

# Function to calculate General Parameters
def GeneralParameters(annual_owner_hrs, annual_charter_hrs, net_effective_hourly_charter_rate):
    total_hrs = annual_owner_hrs + annual_charter_hrs + net_effective_hourly_charter_rate
    return total_hrs

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("General Parameters Dashboard Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Annual Owner Hrs', style={"font-size": "15px"}),
                        dcc.Input(id='annual_owner_hrs', type='number', value=0, style={"width": "50%"}),
                        html.Label('Annual Charter Hrs', style={"font-size": "15px"}),
                        dcc.Input(id='annual_charter_hrs', type='number', value=0, style={"width": "50%"}),
                        html.Label('Net Effective Hourly Charter Rate', style={"font-size": "15px"}),
                        dcc.Input(id='net_effective_hourly_charter_rate', type='number', value=0, style={"width": "50%"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="generalparameters_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center", "height": "100vh"},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('annual_owner_hrs', 'value'),
        Input('annual_charter_hrs', 'value'),
        Input('net_effective_hourly_charter_rate', 'value'),
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, annual_owner_hrs, annual_charter_hrs, net_effective_hourly_charter_rate):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    total_hrs = GeneralParameters(annual_owner_hrs, annual_charter_hrs, net_effective_hourly_charter_rate)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Total hrs', 'value': total_hrs},
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Total hrs', 'value': total_hrs},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='audience_metrics.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
