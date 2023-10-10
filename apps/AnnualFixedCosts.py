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
def AnnualFixedCost(crew_expense, crew_training, hangar, insurance, aircraft_misc, mmg_fee, payment_capital_cost,avg_residual_depreciation_per_year):
    avg_residual_depreciation_per_year == avg_residual_depreciation_per_year
    total_fixed_cost_with_charter = crew_expense + crew_training + hangar + insurance + aircraft_misc + mmg_fee + payment_capital_cost + avg_residual_depreciation_per_year
    net_charter_profit_contribution = 0.00
    total_fixed_cost_without_charter = crew_expense + crew_training + hangar + insurance + aircraft_misc + mmg_fee + payment_capital_cost + avg_residual_depreciation_per_year
    
    return avg_residual_depreciation_per_year, total_fixed_cost_with_charter, net_charter_profit_contribution, total_fixed_cost_without_charter

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Annual Fixed Costs Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Crew Expense ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_expense', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Training ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_training', type='number', value=0, style={"width": "50%"}),
                        html.Label('Hangar ($)', style={"font-size": "15px"}),
                        dcc.Input(id='hangar', type='number', value=0, style={"width": "50%"}),
                        html.Label('Insurance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='insurance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Aircraft Misc ($)', style={"font-size": "15px"}),
                        dcc.Input(id='aircraft_misc', type='number', value=0, style={"width": "50%"}),
                        html.Label('MMG Fee ($)', style={"font-size": "15px"}),
                        dcc.Input(id='mmg_fee', type='number', value=0, style={"width": "50%"}),
                        html.Label('Payment/Capital cost ($)', style={"font-size": "15px"}),
                        dcc.Input(id='payment_capital_cost', type='number', value=0, style={"width": "50%"}),
                        #html.Label('Original Aircraft Cost ($)', style={"font-size": "15px"}),
                        #dcc.Input(id='original_aircraft_cost', type='number', value=0, style={"width": "50%"}),
                        #html.Label('Annual Residual Depreciation (%)', style={"font-size": "15px"}),
                        #dcc.Input(id='annual_residual_depreciation_percent', type='number', value=0, style={"width": "50%"}),
                        #html.Label('Term of Ownership (Years)', style={"font-size": "15px"}),
                        #dcc.Input(id='term_of_ownership', type='number', value=0, style={"width": "50%"}),
                        html.Label('avg residual depreciation/Year (Years)', style={"font-size": "15px"}),
                        dcc.Input(id='avg_residual_depreciation_per_year', type='number', value=0, style={"width": "50%"}),
                          
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output6", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="annualfixed_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output6', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('crew_expense', 'value'),
        Input('crew_training', 'value'),
        Input('hangar', 'value'),
        Input('insurance', 'value'),
        Input('aircraft_misc', 'value'),
        Input('mmg_fee', 'value'),
        Input('payment_capital_cost', 'value'),
        #Input('original_aircraft_cost', 'value'),
        #Input('annual_residual_depreciation_percent', 'value'),
        #Input('term_of_ownership', 'value'),
        Input('avg_residual_depreciation_per_year', 'value'),
    
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, crew_expense, crew_training, hangar, insurance, aircraft_misc, mmg_fee, payment_capital_cost,avg_residual_depreciation_per_year):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    avg_residual_depreciation_per_year, total_fixed_cost_with_charter, net_charter_profit_contribution, total_fixed_cost_without_charter = AnnualFixedCost(crew_expense, crew_training, hangar, insurance, aircraft_misc, mmg_fee, payment_capital_cost,avg_residual_depreciation_per_year)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Avg Residual Depreciation/Year', 'value': avg_residual_depreciation_per_year},
                {'metric': 'Total Fixed Cost With Charter', 'value': total_fixed_cost_with_charter},
                {'metric': 'Net Charter Profit Contribution', 'value': net_charter_profit_contribution},
                {'metric': 'Total Fixed Cost W/O Charter', 'value': total_fixed_cost_without_charter},
               
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Avg Residual Depreciation/Year', 'value': avg_residual_depreciation_per_year},
        {'metric': 'Total Fixed Cost With Charter', 'value': total_fixed_cost_with_charter},
        {'metric': 'Net Charter Profit Contribution', 'value': net_charter_profit_contribution},
        {'metric': 'Total Fixed Cost W/O Charter', 'value': total_fixed_cost_without_charter},
        
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='annual-fixed-cost.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
