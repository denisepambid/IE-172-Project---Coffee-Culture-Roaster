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



CONTENT_STYLE={
    "margin-top": "em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(width=2),
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardHeader("Remove Order"),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [dbc.Col('Order Number:'),
                                    dbc.Col(html.Div(id='order_number')),]
                                ),
                                dbc.Row(
                                    [dbc.Col('Product Name:'),
                                    dbc.Col(html.Div(id='product')),]
                                ),
                            ]
                        ),
                        dbc.CardFooter(
                            dbc.Button('Remove Order', id='remove', n_clicks=0,
                                    style={'background-color':"#ae7a31"}
                                    )
                        )
                    ]
                ),),
                dbc.Col(width=2)
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader('Confirmation'),
                dbc.ModalBody ("Confirm Removal of Item"),
                dbc.ModalFooter(dbc.Button('Confirm', id='confirm_removal', n_clicks=0,
                                            style={'background-color':"#ae7a31"}))
            ],
            id = 'confirmation',
            is_open=False
        ),
        dbc. Modal(
            [
                dbc.ModalHeader('Removal Successful'),
                dbc.ModalBody('Product has been removed from the database'),
                dbc.ModalFooter('Close tab')
                
            ],
            id = 'final_modal',
            is_open=False
        )
    ]
)

@app.callback(
    [
        Output('order_number', 'children'),
        Output('product', 'children')
    ],
    [
        Input('url','pathname'),
    ],
    State('url','search')
)

def outputDetails(pathname, search):
    if pathname == '/removeorder':
        parsed = urlparse(search)
        order_number = parse_qs(parsed.query)['ordernumber'][0]
        product_id = parse_qs(parsed.query)['id'][0]

        sql = """
        SELECT product_name from product
        WHERE product_id = %s
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
        Output('confirmation','is_open'),
        Output('final_modal','is_open')

    ],
    [Input('remove','n_clicks'),
    Input('confirm_removal','n_clicks')],
    State('url','search')
)

def OpenModal(n_clicks, confirm, search):
    if n_clicks:
        if confirm:
            parsed = urlparse(search)
            order_number = parse_qs(parsed.query)['ordernumber'][0]
            product_id = parse_qs(parsed.query)['id'][0]

            sql = """ DELETE FROM co_product
            WHERE order_id = %s and product_id=%s"""

            values = [order_number, product_id]
            df = db.modifydatabase(sql, values)

            return [False, True]
        return[True, False]
        
    else:
        raise PreventUpdate