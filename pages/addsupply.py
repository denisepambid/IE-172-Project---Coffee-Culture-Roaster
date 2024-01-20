from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from urllib.parse import urlparse, parse_qs
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Item Details"),
        html.Hr(),

        dbc.Alert(id='item_alert', is_open=False, color='danger'),
        
        
        dbc.Row(
            [
                dbc.Col(width=2),
                dbc.Col(
                    [
                    dbc.Row(
                        [
                            dbc.Label("Supply Name", width=3),
                            dbc.Col(
                                dbc.Input(
                                type="text", id='new-supply', placeholder="Enter supply name",
                                ),
                                width=8,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Label("Supply Description", width=3),
                            dbc.Col(
                                dbc.Input(
                                type="text", id='new-supplydesc', placeholder="Enter supply description",
                                ),
                                width=8,
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Button("Submit", id='add-item', n_clicks=None, className='me-2',
                                style={'background-color':"#ae7a31"}),
                    )
                    ]
                ),
                dbc.Col(width=2)
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody("New product has been added."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/productlist', id='item-modalbutton', className='me-1')
                )
            ],
            centered=True,
            id='product_successmodal',
            backdrop='static',
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('item_alert', 'children'),
        Output('item_alert', 'is_open'),
        Output('item-modalbutton', 'is_open'),
    ],
    [
        Input('add-item', 'n_clicks'),
    ],
    [
        State('new-supply', 'value'),
        State('new-supplydesc', 'value'),
        State('item_alert', 'is_open'),
        State('item-modalbutton', 'is_open'),
    ]
)

def addsupplier(click, addntsupply, addntsupplydesc, alertopen, modalopen):
    if click is not None:
        if addntsupply is None:
            return ["Kindly input item name", True, False]
        
        elif addntsupplydesc is None:
            return ["Kindly input item description", True, False]
        
        else:
            sql = """
            INSERT INTO supply(supply_name, supply_description)
            VALUES (%s, %s)
            """
            values = [addntsupply, addntsupplydesc]
            db.modifydatabase(sql, values)
                
            return ["", False, True]
        
    else:
        raise PreventUpdate