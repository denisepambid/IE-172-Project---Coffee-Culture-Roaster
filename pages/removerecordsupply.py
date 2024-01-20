from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from urllib.parse import urlparse,parse_qs

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Remove Supply in Record Production"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [dbc.Col('Production Number:'),
                            dbc.Col(html.Div(id='remove_prod_no')),]
                        ),
                        dbc.Row(
                            [dbc.Col('Supply Name:'),
                            dbc.Col(html.Div(id='remove_supply_id')),]
                        ),
                    ]
                ),
                dbc.CardFooter(
                    dbc.Button('Remove Supply', id='remove-supply', n_clicks=0)
                )
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader('Confirmation'),
                dbc.ModalBody ("Confirm Removal of Item"),
                dbc.ModalFooter(dbc.Button('Confirm', id='confirm_removal-record', n_clicks=0))
            ],
            id = 'confirmation-removeproduction',
            is_open=False
        ),
        dbc. Modal(
            [
                dbc.ModalHeader('Removal Successful'),
                dbc.ModalBody('Product has been removed from the database'),
                dbc.ModalFooter('Close tab')
                
            ],
            id = 'final_modal-record',
            is_open=False
        )
    ]
)

@app.callback(
    [
        Output('remove_prod_no', 'children'),
        Output('remove_supply_id','children')
    ],

    [
        Input('url','pathname'),
        #Input('remove-supply','n_clicks')
    ],
    State('url','search')
)

def removeSupplyRecord(pathname, search):
    if pathname == '/removerecordsupply':
        parsed = urlparse(search)
        prod_no = parse_qs(parsed.query)['prod_no'][0]
        supply_id = parse_qs(parsed.query)['supply_id'][0]

        sql = """SELECT supply_name from supply where supply_id = %s"""
        values = [supply_id]
        cols = ['supply']

        df = db.querydatafromdatabase(sql, values, cols)
        supply = df['supply']

        return [prod_no, supply]
        

@app.callback(
    [
        Output('confirmation-removeproduction','is_open'),
        Output('final_modal-record','is_open')
    ],
    [
        Input('remove-supply','n_clicks'),
        Input('confirm_removal-record', 'n_clicks')
    ],
    State('url','search')

)

def removeSupplyRecordinDatabase(n_clicks, n_clicks2, search):
    if n_clicks:
        if n_clicks2:
            parsed = urlparse(search)
            prod_no = parse_qs(parsed.query)['prod_no'][0]
            supply_id = parse_qs(parsed.query)['supply_id'][0]

            sql = """
            DELETE FROM production_supply
            where prod_no = %s and supply_id = %s
            """

            values = [prod_no, supply_id]
            db.modifydatabase(sql, values)

            return [False, True]
        return [True, False]


