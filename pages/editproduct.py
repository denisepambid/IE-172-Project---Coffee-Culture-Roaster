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
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Product Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='edit-name', placeholder="Product Name",
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
                                type="text", id='edit-desc', placeholder="Describe flavor notes"
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
                                id='edit-type',
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
                                type="number", id='edit-price', placeholder="Enter product price"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Update", id='edit-product', n_clicks=None, style={'background-color':"#ae7a31"}, className='me-2'),
                            class_name='d-grid gap-2 col-6 mx-auto'
                        ),
                        dbc.Col(
                            dbc.Button("Delete", id='delete-product', n_clicks=None, style={'background-color':"#ae7a31"}, className='me-3'),
                            class_name='d-grid gap-2 col-6 mx-auto'
                        )
                    ]
                )
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Edit Success')
                ),
                dbc.ModalBody("Product details has been updated."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/productlist', id='edit-modalbutton', className='me-1')
                )
            ],
            centered=True,
            id='edit-modal',
            backdrop='static',
            is_open=False,
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Product Deleted')
                ),
                dbc.ModalBody("Product has been successfully deleted."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/productlist', id='delete-modalbutton', className='me-1')
                )
            ],
            centered=True,
            id='delete-modal',
            backdrop='static',
            is_open=False,
        )

    ]
)

#---- load current details ----#
@app.callback(
    [
        Output('edit-name', 'value'),
        Output('edit-desc', 'value'),
        Output('edit-type', 'value'),
        Output('edit-price', 'value'),
    ],
    Input('url', 'pathname'),
    State('url', 'search')
)

def loaddetails(pathname, search):
    if pathname == '/editproducts':
        parsed = urlparse(search)
        productid = parse_qs(parsed.query)['id'][0]

        loadsql = """
            SELECT product_name, product_description, product_type, product_price
            FROM product
            WHERE product_id = %s
        """
        loadvalues = [productid]
        col = ['loadname', 'loaddesc', 'loadtype', 'loadprice']

        df = db.querydatafromdatabase(loadsql, loadvalues, col)

        productlabel = df['loadtype'][0]
        if productlabel == "Specialty Coffee":
            producttype = 1
        elif productlabel == "Premium Blends":
            producttype = 2
        elif productlabel == "Single Origin":
            producttype = 3
        productname = df['loadname'][0]
        productdesc = df['loaddesc'][0]
        productprice = df['loadprice'][0]

        return [productname, productdesc, producttype, productprice]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('edit-modal', 'is_open'),
    ],
    [
        Input('edit-product', 'n_clicks'),
    ],
    [
        State('edit-name', 'value'),
        State('edit-desc', 'value'),
        State('edit-type', 'value'),
        State('edit-price', 'value'),
        State('url', 'search'),
        State('edit-modal', 'is_open'),
    ]
)

def updateproduct(click, name, description, type, price, search, modalopen):
    if click is not None:
            if type == 1:
                label = "Specialty Coffee"
            elif type == 2:
                label = "Premium Blends"
            elif type == 3:
                label = "Single Origin"
            else:
                label = ""

            parsed = urlparse(search)
            productid = parse_qs(parsed.query)['id'][0]

            updatesql = """
                UPDATE product
                SET
                    product_name = %s,
                    product_description = %s,
                    product_type = %s,
                    product_price = %s
                WHERE product_id = %s
            """

            updatevalues = [name, description, label, price, productid]

            db.modifydatabase(updatesql, updatevalues)                

            return [True] 
        
    else:
        raise PreventUpdate
    


@app.callback(
    [
        Output('delete-modal', 'is_open'),
    ],
    [
        Input('delete-product', 'n_clicks'),
    ],
    [
        State('url', 'search'),
        State('delete-modal', 'is_open'),
    ]
)

def deleteproduct(delclick, search, modalopen):
    if delclick is not None:
        parsed = urlparse(search)
        productid = int(parse_qs(parsed.query)['id'][0])

        delsql = """
            UPDATE product
            SET is_active = %s
            WHERE product_id = %s
        """

        delvalues = [False, productid]

        db.modifydatabase(delsql, delvalues)                

        return [True] 
        
    else:
        raise PreventUpdate