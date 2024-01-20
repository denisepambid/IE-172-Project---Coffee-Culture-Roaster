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
        dbc.Row(
            [
                dbc.Col(width=2),
                dbc.Col
                (
                    dbc.Card(
                        [
                            dbc.CardHeader("Remove Order"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [dbc.Col('PO Number:'),
                                        dbc.Col(html.Div(id='po_number')),]
                                    ),
                                    dbc.Row(
                                        [dbc.Col('Supply:'),
                                        dbc.Col(html.Div(id='supply')),]
                                    ),
                                ]
                            ),
                            dbc.CardFooter(
                                dbc.Button('Remove Order', id='remove_supply', n_clicks=0,
                                           style={'background-color':"#ae7a31"})
                            )
                        ]
                    ),
                    width=8
                ),
                dbc.Col(width=2)
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader('Confirmation'),
                dbc.ModalBody ("Confirm Removal of Item"),
                dbc.ModalFooter(dbc.Button('Confirm', id='confirm_removalS', n_clicks=0,
                                           style={'background-color':"#ae7a31"}),
                                 )
            ],
            id = 'confirmationS',
            is_open=False
        ),
        dbc. Modal(
            [
                dbc.ModalHeader('Removal Successful'),
                dbc.ModalBody('Product has been removed from the database'),
                dbc.ModalFooter('Close tab')
                
            ],
            id = 'final_modalS',
            is_open=False
        )
    ]
)


@app.callback(
    [
        Output('po_number', 'children'),
        Output('supply', 'children')
    ],
    [
        Input('url','pathname'),
    ],
    State('url','search')
)

def outputDetailsSupply(pathname, search):
    if pathname == '/removesupply':
        parsed = urlparse(search)
        order_number = parse_qs(parsed.query)['po_number'][0]
        product_id = parse_qs(parsed.query)['supply_id'][0]
   
        sql = """
        SELECT supply_name from supply
        WHERE supply_id = %s
        """
        values = [product_id]
        cols = ['name']
        df = db.querydatafromdatabase(sql, values,cols)
        product = df["name"]
        return [order_number, product]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('confirmationS','is_open'),
        Output('final_modalS','is_open')

    ],
    [Input('remove_supply','n_clicks'),
    Input('confirm_removalS','n_clicks')],
    State('url','search')
)

def OpenModalS(n_clicks, confirm, search):
    if n_clicks:
        if confirm:
            parsed = urlparse(search)
            order_number = parse_qs(parsed.query)['po_number'][0]
            product_id = parse_qs(parsed.query)['supply_id'][0]

            sql = """ DELETE FROM po_supply
            WHERE po_no = %s and supply_id=%s"""

            values = [order_number, product_id]
            df = db.modifydatabase(sql, values)

            return [False, True]
        return[True, False]
        
    else:
        raise PreventUpdate