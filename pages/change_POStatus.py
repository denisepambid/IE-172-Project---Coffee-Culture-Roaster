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
                dbc.Col(width=1),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label(id='po_number')
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                        "Delivery Received",
                                                        id = 'fulfill_PO', n_clicks=0,
                                                        style={'background-color':"#ae7a31"}
                                                        ),
                                                        dbc.Button(
                                                        "Cancel PO",
                                                        id = 'cancel_PO', n_clicks=0,
                                                        style={'background-color':"#ae7a31"}
                                                        )
                                                    ], 
                                                    class_name= 'd-grid gap-2 d-md-flex justify-content-md-end'
                                                ),
                                            ],
                                            
                                        )
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Supplier:")
                                                ),
                                                dbc.Col(html.Div(id='supplier_name')),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Supplier Address:")
                                                ),
                                                dbc.Col(html.Div(id='supplier_address'))
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Contact No:")
                                                ),
                                                dbc.Col(html.Div(id='contact_no'))
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Email:")
                                                ),
                                                dbc.Col(html.Div(id='supplier_email'))
                                            ]
                                        ),
                                        dbc.Row(
                                            html.Div(id='PO_orders')
                                        )
                                    ]
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(width=1),
                                        dbc.Col(html.Div(id='orders')),
                                        dbc.Col(width=1)
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Col(width=1)
            ]
        ),
        html.Br(),
        dbc. Row(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(width=7 ),
                        dbc.Col(
                            [
                                "Total: PhP "
                            ],
                        width = 1
                        ),
                        dbc.Col(
                            html.Div(id='total_PO')
                        )
                    ]
            )    ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.Div(id='state')),
                dbc.ModalBody(html.Div(id='message')),
                dbc.ModalFooter(
                    dbc.Button('Confirm', id='confirm_PO', n_clicks=0, style={'background-color':"#ae7a31"})
                )
            ],
            id = 'confirmPO_modal',
            is_open = False
        ),
        dbc.Modal(
            [
                dbc.ModalBody(html.Div(id='state2')),
                dbc.ModalFooter(
                    dbc.Button("Close", href='/purchaseorder',style={'background-color':"#ae7a31"})
                )
            ],
            id = 'closePO',
            is_open=False
        )
    ]
)


@app.callback(
    [
        Output('po_number', 'value'),
        Output('supplier_name','children'),
        Output('supplier_address','children'),
        Output('contact_no','children'),
        Output('supplier_email', 'children'),
        Output('PO_orders','children'),
        Output('total_PO','children')
    ],
    Input('url','pathname'),
    [
        State('url','search')
    ]
)

def outputDataPO(pathname, search):
    total = 0
    if pathname == '/fulfill_PO':
        parsed = urlparse(search)
        order_id = parse_qs(parsed.query)['id'][0]

        sql = """
        SELECT supplier_name, supplier_address, supplier_contactno, supplier_email
        from supplier
		inner join purchaseorder on purchaseorder.supplier_id = supplier.supplier_id
        WHERE po_no = %s
        """

        values = [order_id]
        cols = ['name', 'address', 'contact','email']
        df = db.querydatafromdatabase(sql,values,cols)
        supplier_name = df['name'].values.tolist()
        supplier_address = df['address'].values.tolist()
        contact =df['contact'].values.tolist()
        email = df['email'].values.tolist()

        sql2 = """
                SELECT supply_name, po_qty, price
                from po_supply
                inner join supply on po_supply.supply_id = supply.supply_id
                where po_supply.po_no = %s
            """

        values2 = [order_id]
        cols2 = ['Product', 'Qty', 'Unit Price']

        df2=db.querydatafromdatabase(sql2, values2, cols2)
        table = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True, size='sm')

        
        return order_id, supplier_name, supplier_address, contact, email, table, '3200'
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('confirmPO_modal','is_open'),
        Output('closePO','is_open'),
        Output('state', 'children'),
        Output('state2', 'children'),
        Output('message','children')
    ],
    [
        Input('fulfill_PO','n_clicks'),
        Input('cancel_PO','n_clicks'),
        Input('confirm_PO', 'n_clicks'),
        Input('po_number','value')
    ]
)

def confirmPORemoval(fulfill_order, cancel_PO, confirm_PO, po_no):
    if fulfill_order: 
        if confirm_PO:
            sql = """
            update purchaseorder
            set status_id = 2
            where po_no = %s
            """

            values = [po_no]
            db.modifydatabase(sql, values)
            return [False,True, 'Confirmation', 'Confirmation', 'Deliver Accepted']
        return [True, False, 'Confirmation', 'Confirmation','Confirm Delivery']
    elif cancel_PO: 
        if confirm_PO:
            sql = """
            update purchaseorder
            set status_id = 3
            where po_no = %s
            """

            values = [po_no]
            db.modifydatabase(sql, values)
            return [False,True, 'Cancellation', 'Cancellation', 'Order Cancelled']
        return [True, False, 'Cancellation', 'Cancellation','Confirm Cancellation']
    else:
        raise PreventUpdate