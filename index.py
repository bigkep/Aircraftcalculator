from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq as pd1
import csv

# Connect to main app.py file
from app import app
from app import server

# Connect to your pages
from apps import Home, GeneralParameters, OwnerHourlyCost, AnnualBudget, BudgetPerMonth, AnnualVariableCost, AnnualFixedCosts, PaymentSchedule

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content', children=[]),

    html.Div(
        [
            html.Div([
                html.Div([
                    html.Img(src="/assets/aircraft.png", style={"width": "20.9rem"}),
                    #html.H5("AIRCRAFT CALCULATOR", style={'color': 'white', 'margin-top': '20px', 'font-size' : '0.9em'}),
                ], className='image_title')
            ], className="sidebar-header"),
            html.Div([
                html.Div([
                    html.H5("AIRCRAFT CALCULATOR", style={'color': 'white', 'margin-top': '20px', 'font-size' : '1.2em'}),
                ], className='image_title')
            ], className="sidebar-header"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-house"),
                        html.Span("Home", style={'margin-top': '3px'})], className='icon_title')],
                        href="/",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("GeneralParameters", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/GeneralParameters",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("OwnerHourlyCost", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/OwnerHourlyCost",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("AnnualBudget", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/AnnualBudget",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("BudgetPerMonth", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/BudgetPerMonth",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("AnnualVariableCost", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/AnnualVariableCost",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("AnnualFixedCosts", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/AnnualFixedCosts",
                        active="exact",
                        className="pe-3"
                    ),
                    dbc.NavLink([html.Div([
                        html.I(className="fa-solid fa-database"),
                        html.Span("PaymentSchedule", style={'margin-top': '3px'})], className='icon_title')],
                        href="/apps/PaymentSchedule",
                        active="exact",
                        className="pe-3"
                    ),
                    #dbc.NavLink([html.Div([
                    #    html.I(className="fa-solid fa-circle-info"),
                    #    html.Span("About", style={'margin-top': '3px'})], className='icon_title')],
                    #    href="/apps/about",
                    #    active="exact",
                    #    className="pe-3"
                    #),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        id="bg_id",
        className="sidebar",
    )

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return Home.layout
    elif pathname == '/apps/GeneralParameters':
        return GeneralParameters.layout
    elif pathname == '/apps/OwnerHourlyCost':
        return OwnerHourlyCost.layout
    elif pathname == '/apps/AnnualBudget':
        return AnnualBudget.layout
    elif pathname == '/apps/BudgetPerMonth':
        return BudgetPerMonth.layout
    elif pathname == '/apps/AnnualVariableCost':
        return AnnualVariableCost.layout
    elif pathname == '/apps/AnnualFixedCosts':
        return AnnualFixedCosts.layout
    elif pathname == '/apps/PaymentSchedule':
        return PaymentSchedule.layout
    #elif pathname == '/apps/about':
        #return about.layout


if __name__ == '__main__':
    app.run_server(debug=True)