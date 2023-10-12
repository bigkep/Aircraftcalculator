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
def BudgetPercentage(fuel_cost, airframe_maintainance, engine_apu_maintenance, crew_cost, crew_expenses, crew_training, hanger, insurance, aircraft_misc, mgmt_fee, payment_capital_cost, avg_depreciation_per_year, total_hourly_cost_with_charter, annual_total_fixed_cost_with_charter, total_variable_cost):
    annual_total_hourly_cost_with_charter = annual_total_fixed_cost_with_charter + total_variable_cost
    fuel_cost_percentage = (fuel_cost / total_hourly_cost_with_charter) * 100
    airframe_maintainance_percentage = (airframe_maintainance / total_hourly_cost_with_charter) * 100
    engine_apu_maintenance_percentage = (engine_apu_maintenance/ total_hourly_cost_with_charter ) * 100
    crew_cost_percentage = (crew_cost / total_hourly_cost_with_charter) * 100
    crew_expenses_percentage = (crew_expenses / total_hourly_cost_with_charter ) * 100
    crew_training_percentage = (crew_training / annual_total_hourly_cost_with_charter) * 100
    hanger_percentage = (hanger/ annual_total_hourly_cost_with_charter) * 100
    insurance_percentage = (insurance / annual_total_hourly_cost_with_charter) * 100
    aircraft_misc_percentage = (aircraft_misc/ annual_total_hourly_cost_with_charter) * 100
    mgmt_fee_percentage = (mgmt_fee / annual_total_hourly_cost_with_charter) * 100 
    payment_capital_cost_percentage = (payment_capital_cost / annual_total_hourly_cost_with_charter) * 100
    avg_depreciation_per_year_percentage = (avg_depreciation_per_year / annual_total_hourly_cost_with_charter) * 100
    total_percentage = avg_depreciation_per_year_percentage + payment_capital_cost_percentage + mgmt_fee_percentage + aircraft_misc_percentage + insurance_percentage + hanger_percentage + crew_training_percentage + crew_expenses_percentage + crew_cost_percentage + fuel_cost_percentage + engine_apu_maintenance_percentage + airframe_maintainance_percentage
    
    return fuel_cost_percentage, airframe_maintainance_percentage, engine_apu_maintenance_percentage, crew_cost_percentage, crew_expenses_percentage, crew_training_percentage, hanger_percentage, insurance_percentage, aircraft_misc_percentage, mgmt_fee_percentage, payment_capital_cost_percentage, avg_depreciation_per_year_percentage , total_percentage

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Budget By Percentage Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Fuel Cost ($)', style={"font-size": "15px"}),
                        dcc.Input(id='fuel_cost', type='number', value=0, style={"width": "50%"}),
                        html.Label('Airframe Maintainance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='airframe_maintainance', type='number', value=0, style={"width": "50%"}),
                        html.Label('engine APU Maintenance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='engine_apu_maintenance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Misc ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_cost', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Expenses ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_expenses', type='number', value=0, style={"width": "50%"}),
                        html.Label('Crew Training ($)', style={"font-size": "15px"}),
                        dcc.Input(id='crew_training', type='number', value=0, style={"width": "50%"}),
                        html.Label('Hanger ($)', style={"font-size": "15px"}),
                        dcc.Input(id='hanger', type='number', value=0, style={"width": "50%"}),
                        html.Label('Insurance ($)', style={"font-size": "15px"}),
                        dcc.Input(id='insurance', type='number', value=0, style={"width": "50%"}),
                        html.Label('Aircraft Misc ($)', style={"font-size": "15px"}),
                        dcc.Input(id='aircraft_misc', type='number', value=0, style={"width": "50%"}),
                        html.Label('Mgmt Fee ($)', style={"font-size": "15px"}),
                        dcc.Input(id='mgmt_fee', type='number', value=0, style={"width": "50%"}),
                        html.Label('Payment Capital Cost ($)', style={"font-size": "15px"}),
                        dcc.Input(id='payment_capital_cost', type='number', value=0, style={"width": "50%"}),
                        html.Label('Avg Depreciation Per Year ($)', style={"font-size": "15px"}),
                        dcc.Input(id='avg_depreciation_per_year', type='number', value=0, style={"width": "50%"}),
                        html.Label('Total Hourly Cost With Charter ($)', style={"font-size": "15px"}),
                        dcc.Input(id='total_hourly_cost_with_charter', type='number', value=0, style={"width": "50%"}),
                        html.Label('Annual Total Fixed Cost With Charter ($)', style={"font-size": "15px"}),
                        dcc.Input(id='annual_total_fixed_cost_with_charter', type='number', value=0, style={"width": "50%"}),
                        html.Label('Total Variable Cost ($)', style={"font-size": "15px"}),
                        dcc.Input(id='total_variable_cost', type='number', value=0, style={"width": "50%"}),
                        
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output8", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="monthlynudget_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output8', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('fuel_cost', 'value'),
        Input('airframe_maintainance', 'value'),
        Input('engine_apu_maintenance', 'value'),
        Input('crew_cost', 'value'),
        Input('crew_expenses', 'value'),
        Input('crew_training', 'value'),
        Input('hanger', 'value'),
        Input('insurance', 'value'),
        Input('aircraft_misc', 'value'),
        Input('mgmt_fee', 'value'),
        Input('payment_capital_cost', 'value'),
        Input('avg_depreciation_per_year', 'value'),
        Input('total_hourly_cost_with_charter', 'value'),
        Input('annual_total_fixed_cost_with_charter', 'value'),
        Input('total_variable_cost', 'value'),
    
    ]
)

# Define the callback function to perform the calculation
def calculate_percentage(n_clicks, fuel_cost, airframe_maintainance, engine_apu_maintenance, crew_cost, crew_expenses, crew_training, hanger, insurance, aircraft_misc, mgmt_fee, payment_capital_cost, avg_depreciation_per_year, total_hourly_cost_with_charter, annual_total_fixed_cost_with_charter, total_variable_cost):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    fuel_cost_percentage, airframe_maintainance_percentage, engine_apu_maintenance_percentage, crew_cost_percentage , crew_expenses_percentage ,crew_training_percentage, hanger_percentage, insurance_percentage, aircraft_misc_percentage, mgmt_fee_percentage, payment_capital_cost_percentage, avg_depreciation_per_year_percentage, total_percentage= BudgetPercentage(fuel_cost, airframe_maintainance, engine_apu_maintenance, crew_cost, crew_expenses, crew_training, hanger, insurance, aircraft_misc, mgmt_fee, payment_capital_cost, avg_depreciation_per_year, total_hourly_cost_with_charter, annual_total_fixed_cost_with_charter, total_variable_cost)
    
    # Format the numerical results to two decimal places
    fuel_cost_percentage = Decimal(fuel_cost_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    airframe_maintainance_percentage = Decimal(airframe_maintainance_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    engine_apu_maintenance_percentage = Decimal(engine_apu_maintenance_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    crew_cost_percentage = Decimal(crew_cost_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    crew_expenses_percentage = Decimal(crew_expenses_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    crew_training_percentage = Decimal(crew_training_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    hanger_percentage = Decimal(hanger_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    insurance_percentage = Decimal(insurance_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    aircraft_misc_percentage = Decimal(aircraft_misc_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    mgmt_fee_percentage = Decimal(mgmt_fee_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    payment_capital_cost_percentage = Decimal(payment_capital_cost_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    avg_depreciation_per_year_percentage = Decimal(avg_depreciation_per_year_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    total_percentage = Decimal(total_percentage).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Fuel Cost %', 'value': fuel_cost_percentage},
                {'metric': 'Airframe Maintainance %', 'value': airframe_maintainance_percentage},
                {'metric': 'Engine APU Maintenance %', 'value': engine_apu_maintenance_percentage},
                {'metric': 'Crew Cost %', 'value': crew_cost_percentage},
                {'metric': 'Crew Expenses %', 'value': crew_expenses_percentage},
                {'metric': 'Crew Training %', 'value': crew_training_percentage},
                {'metric': 'Hanger %', 'value': hanger_percentage},
                {'metric': 'Insurance %', 'value': insurance_percentage},
                {'metric': 'Aircraft Misc %', 'value': aircraft_misc_percentage},
                {'metric': 'Mgmt Fee %', 'value': mgmt_fee_percentage},
                {'metric': 'Payment Capital Cost %', 'value': payment_capital_cost_percentage},
                {'metric': 'Avg Depreciation Per Year %', 'value': avg_depreciation_per_year_percentage},
                {'metric': 'Total %', 'value': total_percentage},
                
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Fuel Cost %', 'value': fuel_cost_percentage},
        {'metric': 'Airframe Maintainance %', 'value': airframe_maintainance_percentage},
        {'metric': 'Engine APU Maintenance %', 'value': engine_apu_maintenance_percentage},
        {'metric': 'Crew Cost %', 'value': crew_cost_percentage},
        {'metric': 'Crew Expenses %', 'value': crew_expenses_percentage},
        {'metric': 'Crew Training %', 'value': crew_training_percentage},
        {'metric': 'Hanger %', 'value': hanger_percentage},
        {'metric': 'Insurance %', 'value': insurance_percentage},
        {'metric': 'Aircraft Misc %', 'value': aircraft_misc_percentage},
        {'metric': 'Mgmt Fee %', 'value': mgmt_fee_percentage},
        {'metric': 'Payment Capital Cost %', 'value': payment_capital_cost_percentage},
        {'metric': 'Avg Depreciation Per Year %', 'value': avg_depreciation_per_year_percentage},
        {'metric': 'Total %', 'value': total_percentage},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='Budget-by-percentage.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)

    

    