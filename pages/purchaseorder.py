from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import date
from app import app

from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H2("Purchase Order"),
                ),
                dbc.Col(
                    width = 6
                ),
                dbc.Col(
                    dbc.Button('Create New Purchase Order', href='create_po', n_clicks=0,
                               style={'background-color':"#ae7a31"})
                )
            ]
        ),
        html.Hr(),

        html.Br(),
        dbc.Card(
            [   
                dbc.CardHeader(html.H5('Supplier Information')),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(width=1),
                                dbc.Col(
                                    dbc.Label('Supplier Name:'),
                                    width='auto'
                                ),
                                dbc.Col(
                                    dcc.Dropdown(id = 'supplier_names', placeholder='Choose Supplier'),
                                    width=8
                                ),
                                dbc.Col(width=1),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(width=3),
                                dbc.Col('Supplier Address: ', width=2),
                                dbc.Col(html.Div(id = 'address'), width='auto')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(width=3),
                                dbc.Col('Supplier Co. Number: ', width=2),
                                dbc.Col(html.Div(id = 'contact'), width='auto')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(width=3),
                                dbc.Col('Supplier Email: ', width=2),
                                dbc.Col(html.Div(id = 'email'), width='auto')
                            ]
                        ),
                        html.Br(),
                        
                    ]
                )
            ],
        ),

        html.Br(),

        dbc.Checklist(
            options=[
                {"label": "Active", "value":1},
                {"label":"Fulfilled", "value": 2},
                {"label": "Cancelled",  "value":3}
            ],
            value=[1],
            id="po_filter",
            inline=True,
        ),

        dbc.Card(
            [
                html.Div(id= 'po_list')
            ]
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader('Error Message'),
                dbc.ModalBody(
                    [
                        dbc.Row('Input Error'),
                    ]
                ),
            ],
            centered = True,
            id = 'error_modal',
            is_open=False
        ),
    ]
)

@app.callback(
    Output('supplier_names','options'),
    Input('url', 'pathname')
)

def showsuppliers(pathname):
    if pathname == '/purchaseorder':
        sql = """ 
        SELECT supplier_name, supplier_id from supplier
        """
        values = []
        cols = ['label', 'value']
        df=db.querydatafromdatabase(sql, values, cols)
        suppliers = df.to_dict('records')
        return suppliers
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('address', 'children'),
        Output('contact', 'children'),
        Output('email', 'children'),
    ],
    Input('supplier_names','value')
)

def supplierchosen(supplier):
    if supplier:
        sql = """SELECT supplier_address, supplier_contactno, supplier_email from supplier
            WHERE supplier_id = %s"""
        values = [supplier]
        cols = ['address', 'contact', 'email']
        df=db.querydatafromdatabase(sql,values,cols)
        
        address =df['address'].values.tolist()
        contact =df['contact'].values.tolist()
        email = df['email'].values.tolist()
        return address, contact, email
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('po_list','children'),
    ],
    [
        Input('supplier_names','value'),
        Input('po_filter', 'value')
    ]
)

def po_list(supplier_name, filter):
    sql = """
        select po_no,supplier_name, po_date, status
        from purchaseorder po
        inner join status s on po.status_id = s.status_id
        inner join supplier on po.supplier_id = supplier.supplier_id 
        """
    
    values = []

    if supplier_name:
        sql += "and supplier.supplier_id = %s"
        values += [supplier_name]
    
    if filter == [1]:
        sql += " and s.status_id = 1"
    elif filter == [2]:
        sql += " and s.status_id = 2"
    elif filter == [3]:
        sql += " and s.status_id = 3"
    elif filter == [1,2]:
        sql += " and s.status_id < 3"
    elif filter == [2,3]:
        sql += " and s.status_id > 1"
    


    cols = ['PO No', 'Supplier', 'Date', 'Status']
    df = db.querydatafromdatabase(sql, values, cols)

    if df.shape:
        buttons = []
        for po_no in df['PO No']:
            buttons += [
                html.Div(
                    dbc.Button('Open',
                               href=f'fulfill_PO?id={po_no}',
                               size='sm', color='link')
                )
            ]
    df['Action'] = buttons
    df = df[['PO No', 'Supplier', 'Date', 'Status','Action']]

    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
    return [table]


