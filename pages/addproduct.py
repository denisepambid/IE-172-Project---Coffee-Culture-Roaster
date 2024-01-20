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
        html.H2("Product Details"),
        html.Hr(),

        dbc.Alert(id='product_alert', is_open=False, color='danger'),
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Product Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='product_name', placeholder="Enter product name",
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Flavor Notes", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='product_description', placeholder="Describe flavor notes"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Product Type", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id='product_type',
                                options=[
                                    {"label": "Specialty Coffee", "value": 1},
                                    {"label": "Premium Blends", "value": 2},
                                    {"label": "Single Origins", "value": 3}
                                ],
                                placeholder="Product Type"
                            ),
                            width=10
                        )
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Price", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="number", id='product_price', placeholder="Enter product price"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),

                dbc.Button("Submit", id='add_product', n_clicks=None, className='me-2', style={'background-color':"#ae7a31"}),
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody("New product has been added."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/productlist', id='product_modalbutton', className='me-1')
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
        Output('product_alert', 'children'),
        Output('product_alert', 'is_open'),
        Output('product_successmodal', 'is_open'),
    ],
    [
        Input('add_product', 'n_clicks'),
    ],
    [
        State('product_name', 'value'),
        State('product_description', 'value'),
        State('product_type', 'value'),
        State('product_price', 'value'),
        State('product_alert', 'is_open'),
        State('product_successmodal', 'is_open'),
    ]
)

def addproduct(click, name, description, type, price, alertopen, modalopen):
    if click is not None:
        if name is None:
            return ["Kindly input product name", True, False]
        
        elif description is None:
            return ["Kindly input flavor notes", True, False]
        
        elif type is None:
            return ["Kindly select product type", True, False]
        
        elif price is None:
            return ["Kindly input price", True, False]
        
        else:
            if type == 1:
                label = "Specialty Coffee"
            elif type == 2:
                label = "Premium Blends"
            elif type == 3:
                label = "Single Origin"
            else:
                label = ""

            sql = """
                    INSERT INTO product(product_name, product_description, product_type, product_price, is_active)
                    VALUES (%s, %s, %s, %s, %s)
            """
            values = [name, description, label, price, True]
            db.modifydatabase(sql, values)
            return ["", False, True] 
        
    else:
        raise PreventUpdate