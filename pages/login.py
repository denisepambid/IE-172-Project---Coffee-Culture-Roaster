from dash import dcc 
from dash import html
import dash_bootstrap_components as dbc
import dash 
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import dash_table
from dash import dash_table
from apps import dbconnect as db
from app import app

layout = html.Div(
    [
        html.H2('Login'),
        html.Hr(),
        dbc.Alert('Username or password is incorrect.', color="danger", id='login-alert', is_open=False),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src = 'assets/coffee culture.png',
                                top = True
                            ),
                        ],
                    )
                ),
                dbc.Col(
                    [
                        ###
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Label("Username", width=3),
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="login-username", placeholder="Enter username"
                                    ),
                                    width=8,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Password", width=3),
                                dbc.Col(
                                    dbc.Input(
                                        type="password", id="login-password", placeholder="Enter password"
                                    ),
                                    width=8,
                                ),
                            ],
                            className="mb-3",
                        ),
                        
                        dbc.Row(html.Div(
                            dbc.Button('Login', style={'background-color':"#ae7a31"}, id='login-button', n_clicks=0),
                            className='d-grid gap-2 d-md-flex justify-content-md-end'
                            ))
                        ###
                    ],
                    width='auto'
                ),
                dbc.Col(
                    width = 2
                )
            ]
        ),
        
        html.Hr(),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Login Success')
                ),
                dbc.ModalBody("You are successfully logged in."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/home', id='login-modalbutton', className='me-1', n_clicks=0,
                               style={'background-color':"#ae7a31"})
                )
            ],
            centered=True,
            id='login-modal',
            backdrop='static',
            is_open=False,
        )
    ]
)


@app.callback(
    [
        Output('login-alert', 'is_open'),
        Output('login-modal', 'is_open'),
    ],
    [
        Input('login-button', 'n_clicks'), 
    ],
    [
        State('login-username', 'value'),
        State('login-password', 'value'),
    ]
)
def loginprocess(click, username, password):
    if click:
        if username == "user" and password == "admin":
            return [False, True]
        
        else:
            return [True, False]
    
    else:
        raise PreventUpdate
    