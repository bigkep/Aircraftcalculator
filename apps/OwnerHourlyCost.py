import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from decimal import Decimal, ROUND_HALF_UP
import urllib.parse
import pandas as pd
import base64
import io

# Function to calculate General Parameters
def Ownerhourlycost(fuel_usage, fuel_cost_per_gallon, airframe_maintenance, engine_apu_maintenance, crew_cost, total_fixed_cost_without_charter ):
    fuel_cost_per_hour = fuel_usage * fuel_cost_per_gallon
    total_maintenance_cost = airframe_maintenance + engine_apu_maintenance
    total_variable_cost_per_hour = fuel_cost_per_hour + total_maintenance_cost + crew_cost
    total_hourly_cost_without_charter = total_variable_cost_per_hour + total_fixed_cost_without_charter
    total_fixed_cost_with_charter = total_fixed_cost_without_charter
    total_hourly_cost_with_charter = total_variable_cost_per_hour + total_fixed_cost_with_charter
    
    return fuel_cost_per_hour, total_maintenance_cost, total_variable_cost_per_hour, total_hourly_cost_without_charter,total_fixed_cost_with_charter, total_hourly_cost_with_charter

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Owner Hourly Cost Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Fuel Usage (Gallon Per Hour)', style={"font-size": "15px"}),
                        dcc.Input(id='fuel_usage', type='number', value=0, style={"width": "50%"}),
                        html.Label('Fuel Cost Per Gallon ($)', style={"font-size": "15px"}),
                        dcc.Input(id='fuel_cost_per_gallon', type='number', value=0, style={"width": "50%"}),
                        html.Label('Airframe Maintenance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='airframe_maintenance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Engine Apu Maintenance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='engine_apu_maintenance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Cost ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_cost', type='number', value=0, style={"width": "50%"}),
                        html.Label('Total Fixed Cost W/O Charter ($)', style={"font-size": "15px"}),
                        dcc.Input(id='total_fixed_cost_without_charter', type='number', value=0, style={"width": "50%"}),
                        
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output2", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="ownerhourlycost_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center",},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output2', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('fuel_usage', 'value'),
        Input('fuel_cost_per_gallon', 'value'),
        Input('airframe_maintenance', 'value'),
        Input('engine_apu_maintenance', 'value'),
        Input('crew_cost', 'value'),
        Input('total_fixed_cost_without_charter', 'value'),
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, fuel_usage, fuel_cost_per_gallon, airframe_maintenance, engine_apu_maintenance, crew_cost, total_fixed_cost_without_charter):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    fuel_cost_per_hour, total_maintenance_cost, total_variable_cost_per_hour, total_hourly_cost_without_charter, total_fixed_cost_with_charter, total_hourly_cost_with_charter = Ownerhourlycost(fuel_usage, fuel_cost_per_gallon, airframe_maintenance, engine_apu_maintenance, crew_cost, total_fixed_cost_without_charter)
    
    # Format the numerical results to two decimal places
    fuel_cost_per_hour = Decimal(fuel_cost_per_hour).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_maintenance_cost = Decimal(total_maintenance_cost).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_variable_cost_per_hour = Decimal(total_variable_cost_per_hour).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_hourly_cost_without_charter = Decimal(total_hourly_cost_without_charter).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_fixed_cost_with_charter = Decimal(total_fixed_cost_with_charter).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_hourly_cost_with_charter = Decimal(total_hourly_cost_with_charter).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Fuel Cost Per Hour ($)', 'value': fuel_cost_per_hour},
                {'metric': 'Total Maintenance Cost ($)', 'value': total_maintenance_cost},
                {'metric': 'Total Variable Cost Per Hour ($)', 'value': total_variable_cost_per_hour},
                {'metric': 'Total Fixed Cost W/O Charter ($)', 'value': total_fixed_cost_without_charter},
                {'metric': 'Total Hourly Cost W/O Charter ($)', 'value': total_hourly_cost_without_charter},
                {'metric': 'Total Fixed Cost With Charter ($)', 'value': total_fixed_cost_with_charter},
                {'metric': 'Total Hourly Cost With Charter ($)', 'value': total_hourly_cost_with_charter},
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Fuel Cost Per Hour ($)', 'value': fuel_cost_per_hour},
        {'metric': 'Total Maintenance Cost ($)', 'value': total_maintenance_cost},
        {'metric': 'Total Variable Cost Per Hour ($)', 'value': total_variable_cost_per_hour},
        {'metric': 'Total Fixed Cost W/O Charter ($)', 'value': total_fixed_cost_without_charter},
        {'metric': 'Total Hourly Cost W/O Charter ($)', 'value': total_hourly_cost_without_charter},
        {'metric': 'Total Fixed Cost With Charter ($)', 'value': total_fixed_cost_with_charter},
        {'metric': 'Total Hourly Cost With Charter ($)', 'value': total_hourly_cost_with_charter},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='owner_hourly_cost.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
