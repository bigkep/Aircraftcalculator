from dash import html
from dash import dcc


layout = html.Div([
    html.Div([
        html.Div([
            html.P(
                "Aircraft Calculator", style={"color": "#0084d6",
                                              "font-size": "20px",
                                              'margin-left': '15px',
                                              'margin-top': '15px'}
            ),
            html.P([html.P(dcc.Markdown('''Welcome to the **Aircraft Dashboard Calculator**!''',
                                        style={"color": "#ffffff",
                                               "font-size": "15px",
                                               'margin-left': '15px',
                                               'margin-top': '15px'})),
                    html.P(dcc.Markdown(
                        '''
                         I've developed an aircraft calculator utilizing the Python libraries Plotly Dash for interactive data 
                         visualization and Dash for this web framework. This tool allows for the analysis of various aircraft 
                         claculations, providing dynamic dataframe results and allows users to download the table result.
                        ''',
                        style={"color": "#ffffff",
                               "font-size": "15px",
                               'margin-left': '15px',
                               'margin-right': '15px',
                               'margin-bottom': '15px',
                               'line-height': '1.2',
                               'text-align': 'justify'}
                    )),
                    html.P([dcc.Markdown(
                        '''
                        If you have any questions or need assistance, please don't hesitate to reach out.
                        ''',
                        style={"color": "#ffffff",
                               "font-size": "15px",
                               'margin-left': '15px',
                               'margin-right': '15px',
                               'margin-bottom': '15px',
                               'line-height': '1.2',
                               'text-align': 'justify'},
                    ),
                        html.P(
                            html.A('BIGKEP', href='https://www.linkedin.com/in/john-ilesanmi-007487248/',
                                   target="_blank", style={"color": "#0084d6", 'text-decoration': 'none'}),
                            style={"color": "#ffffff",
                                   "font-size": "15px",
                                   'margin-left': '15px',
                                   'margin-right': '15px',
                                   'margin-bottom': '30px',
                                   'line-height': '1.2',
                                   'text-align': 'justify',
                                   'margin-top': '-15px'}),
                    ])
                    ])
        ], className='home_bg eight columns')
    ], className='home_row row')
])

