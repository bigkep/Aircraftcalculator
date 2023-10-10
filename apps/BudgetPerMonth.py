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
def MonthlyBudgets(Annual_Owner_Hr, Annual_budget):
    Monthly_Hr = Annual_Owner_Hr / 12
    Monthly_budget = Annual_budget / 12
    
    return Monthly_Hr, Monthly_budget

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Budget Per Month Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Annual Owner Hours', style={"font-size": "15px"}),
                        dcc.Input(id='Annual_Owner_Hr', type='number', value=0, style={"width": "50%"}),
                        html.Label('Annual Budget ($)', style={"font-size": "15px"}),
                        dcc.Input(id='Annual_budget', type='number', value=0, style={"width": "50%"}),
                        
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output4", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="monthlynudget_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center","height": "100vh"},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output4', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('Annual_Owner_Hr', 'value'),
        Input('Annual_budget', 'value'),
    
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, Annual_Owner_Hr, Annual_budget):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    Monthly_Hr, MonthlyBudget = MonthlyBudgets(Annual_Owner_Hr, Annual_budget)
    
    # Format the numerical results to two decimal places
    #annual_owner_hrs = Decimal(annual_owner_hrs).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    #annual_budget_without_charter = Decimal(annual_budget_without_charter).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    #annual_budget_with_charter = Decimal(annual_budget_with_charter).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Monthly Hours', 'value': Monthly_Hr},
                {'metric': 'MonthlybBudget ($)', 'value': MonthlyBudget},
                
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Monthly Hours', 'value': Monthly_Hr},
        {'metric': 'MonthlybBudget ($)', 'value': MonthlyBudget},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='Budget-per-month.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
