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
def VariableCosts(Total_hrs, fuel_usage, fuel_cost_per_hour, airframe_maintenance, engine_apu_maintenance, Crew_Misc):
        Annual_Fuel_Gallons = fuel_usage * Total_hrs
        Annual_Fuel_cost = fuel_cost_per_hour * Total_hrs
        Annual_airframe_maintenance = airframe_maintenance * Total_hrs
        Annual_engine_apu_maintenance = engine_apu_maintenance * Total_hrs
        Annual_Crew_Misc = Crew_Misc * Total_hrs
        Total_Variable_cost = Annual_Fuel_cost + Annual_airframe_maintenance + Annual_engine_apu_maintenance + Annual_Crew_Misc
        
        return Annual_Fuel_Gallons, Annual_Fuel_cost, Annual_airframe_maintenance, Annual_engine_apu_maintenance, Annual_Crew_Misc, Total_Variable_cost

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Annual Variable Cost Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Total Hours', style={"font-size": "15px"}),
                        dcc.Input(id='Total_hrs', type='number', value=0, style={"width": "50%"}),
                        html.Label('Fuel Usage(Gallons per Hour)', style={"font-size": "15px"}),
                        dcc.Input(id='fuel_usage', type='number', value=0, style={"width": "50%"}),
                        html.Label('Fuel Cost Per Hour ($', style={"font-size": "15px"}),
                        dcc.Input(id='fuel_cost_per_hour', type='number', value=0, style={"width": "50%"}),
                        html.Label('Airframe Maintenance Cost Per Hour ($)', style={"font-size": "15px"}),
                        dcc.Input(id='airframe_maintenance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Engine & APU Maintenance Cost Per Hour ($)', style={"font-size": "15px"}),
                        dcc.Input(id='engine_apu_maintenance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Misc', style={"font-size": "15px"}),
                        dcc.Input(id='Crew_Misc', type='number', value=0, style={"width": "50%"}),
                        
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output5", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="annualvariable_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center",},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output5', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('Total_hrs', 'value'),
        Input('fuel_usage', 'value'),
        Input('fuel_cost_per_hour', 'value'),
        Input('airframe_maintenance', 'value'),
        Input('engine_apu_maintenance', 'value'),
        Input('Crew_Misc', 'value'),
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, Total_hrs, fuel_usage, fuel_cost_per_hour, airframe_maintenance, engine_apu_maintenance, Crew_Misc):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    Annual_Fuel_Gallons, Annual_Fuel_cost, Annual_airframe_maintenance, Annual_engine_apu_maintenance, Annual_Crew_Misc, Total_Variable_cost = VariableCosts(Total_hrs, fuel_usage, fuel_cost_per_hour, airframe_maintenance, engine_apu_maintenance, Crew_Misc)
    
    # Format the numerical results to two decimal places
    Annual_Fuel_Gallons = Decimal(Annual_Fuel_Gallons).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    Annual_Fuel_cost = Decimal(Annual_Fuel_cost).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    Annual_airframe_maintenance = Decimal(Annual_airframe_maintenance).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    Annual_engine_apu_maintenance = Decimal(Annual_engine_apu_maintenance).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    Annual_Crew_Misc = Decimal(Annual_Crew_Misc).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    Total_Variable_cost = Decimal(Total_Variable_cost).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Fuel Gallons', 'value': Annual_Fuel_Gallons},
                {'metric': 'Fuel Cost ($)', 'value': Annual_Fuel_cost},
                {'metric': 'Airframe Maintenance ($)', 'value': Annual_airframe_maintenance},
                {'metric': 'Engine Apu Maintenance ($)', 'value': Annual_engine_apu_maintenance},
                {'metric': 'Crew Misc ($)', 'value': Annual_Crew_Misc},
                {'metric': 'Total Variable Cost ($)', 'value': Total_Variable_cost},
                
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Fuel Gallons', 'value': Annual_Fuel_Gallons},
        {'metric': 'Fuel Cost ($)', 'value': Annual_Fuel_cost},
        {'metric': 'Airframe Maintenance ($)', 'value': Annual_airframe_maintenance},
        {'metric': 'Engine Apu Maintenance ($)', 'value': Annual_engine_apu_maintenance},
        {'metric': 'Crew Misc ($)', 'value': Annual_Crew_Misc},
        {'metric': 'Total Variable Cost ($)', 'value': Total_Variable_cost},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='Annual-variable-cost.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
