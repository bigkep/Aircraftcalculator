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
def Paymentschedule(interest_rate, loan_term_months, loan_amount, Monthly_lesae, period_number):
    
    monthly_interest_rate = interest_rate / 12 /100
    
    # Calculate monthly payment
    payment_per_period = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
    monthly_interest_payment = loan_amount * monthly_interest_rate
    principal_amount = payment_per_period - monthly_interest_payment
    #principal_amount = (payment_per_period * ((1 + monthly_interest_rate) ** loan_term_months - 1)) / monthly_interest_rate
    
    
    intrest_amount = payment_per_period - principal_amount
    
    
    
    return monthly_interest_rate, payment_per_period, principal_amount, intrest_amount

# Initialize the Dash App
app = dash.Dash(__name__)

# Define the layout of the app
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("Payment Schedule Calculator", style={"color": "white", "font-size": "20px"}),
                    ],
                    style={"text-align": "center", "margin-top": "20px"}
                ),
                html.Div(
                    children=[
                        html.Label('Interest Rate (%)', style={"font-size": "15px"}),
                        dcc.Input(id='interest_rate', type='number', value=0, style={"width": "50%"}),
                        html.Label('Term of Loan (Months)', style={"font-size": "15px"}),
                        dcc.Input(id='loan_term_months', type='number', value=0, style={"width": "50%"}),
                        html.Label('Loan ($)', style={"font-size": "15px"}),
                        dcc.Input(id='loan_amount', type='number', value=0, style={"width": "50%"}),
                        html.Label('Monthly Lease ($)', style={"font-size": "15px"}),
                        dcc.Input(id='Monthly_lesae', type='number', value=0, style={"width": "50%"}),
                        html.Label('Period Number', style={"font-size": "15px"}),
                        dcc.Input(id='period_number', type='number', value=0, style={"width": "50%"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(
                    children=[
                        html.Button('Calculate', id='calculate_button', style={"margin-top": "15px", "width": "50%", "color": "Blue"}),
                    ],
                    style={"text-align": "center", "margin": "20px"}
                ),
                html.Div(id="output7", style={"margin-top": "20px"})
            ],
            style={"width": "50%", "margin": "0 auto"},
            className="Paymentschedule_one",
        )
    ],
    style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center", "height": "100vh"},
)

# Define the callback to calculate and display the metrics
@callback(
    Output('output7', 'children'),
    [Input('calculate_button', 'n_clicks')],
    [   
        Input('interest_rate', 'value'),
        Input('loan_term_months', 'value'),
        Input('loan_amount', 'value'),
        Input('Monthly_lesae', 'value'),
        Input('period_number', 'value'),
    ]
)
# Define the callback function to perform the calculation
def calculate_total_hours(n_clicks, interest_rate, loan_term_months, loan_amount, Monthly_lesae, period_number):
    if n_clicks is None:
        raise PreventUpdate
    
    # Call the GeneralParameters function with user inputs
    monthly_interest_rate, payment_per_period, principal_amount, intrest_amount = Paymentschedule(interest_rate, loan_term_months, loan_amount, Monthly_lesae, period_number)
    
    # Format the numerical results to two decimal places
    payment_per_period = Decimal(payment_per_period).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    principal_amount = Decimal(principal_amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    intrest_amount = Decimal(intrest_amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    
    # Create a table to display the results
    result = html.Div([
        html.H2("Metrics", style={"color": "#0084d6", "font-size": "20px", 'width': '50%', 'margin':'auto'}),
        dash_table.DataTable(
            columns=[{'name': 'Metric', 'id': 'metric'}, {'name': 'Value', 'id': 'value'}],
            data=[
                {'metric': 'Payment Per Period ($)', 'value': payment_per_period},
                {'metric': 'Principal Amount ($)', 'value': principal_amount},
                {'metric': 'Interest Amount ($)', 'value': intrest_amount},
            ],
            style_table={"color": "#0084d6", 'width': '50%','margin':'auto' },
            style_cell={'textAlign': 'center'},
        ),
    ])
    
    # Create a CSV file to be downloaded
    csv_string = pd.DataFrame([
        {'metric': 'Payment Per Period ($)', 'value': payment_per_period},
        {'metric': 'Principal Amount ($)', 'value': principal_amount},
        {'metric': 'Intrest Amount ($)', 'value': intrest_amount},
    ]).to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    # Include the download button under the table
    result_with_download = html.Div([
        result,
        html.A('Download Table', href=csv_string, download='payment-schedule.csv'),
        
    ], style={"text-align": "center"})

    return result_with_download

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
