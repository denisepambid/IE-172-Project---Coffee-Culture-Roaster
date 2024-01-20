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
                                                    dbc.Label(id='order_number')
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                        "Fulfill Order",
                                                        id = 'fulfill_order', n_clicks=0,
                                                        style={'background-color':"#ae7a31"}
                                                        ),

                                                        dbc.Button(
                                                        "Cancel Order",
                                                        id = 'cancel_order', n_clicks=0,
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
                                                    dbc.Label("Customer Name:")
                                                ),
                                                dbc.Col(html.Div(id='customer_name')),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Label("Customer Address:")
                                                ),
                                                dbc.Col(id='customer_address')
                                            ]
                                        ),
                                        dbc.Row(
                                            html.Div(id='customer_orders')
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
                            html.Div(id='total')
                        )
                    ]
            )    ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.Div(id='modal1')),
                dbc.ModalBody(html.Div(id='modal_message')),
                dbc.ModalFooter(
                    dbc.Button('Confirm', id='confirm', n_clicks=0,
                               style={'background-color':"#ae7a31"})
                )
            ],
            id = 'confirm_modal',
            is_open = False
        ),
        dbc.Modal(
            [
                dbc.ModalBody(html.Div(id='modal2')),
                dbc.ModalFooter(
                    dbc.Button("Close", href='/orderlist', style={'background-color':"#ae7a31"})
                )
            ],
            id = 'close',
            is_open=False
        )
    ]
)

@app.callback(
    [
        Output('order_number', 'value'),
        Output('customer_name','children'),
        Output('customer_address','children'),
        Output('orders','children'),
        Output('total','children')
    ],
    Input('url','pathname'),
    [
        State('url','search')
    ]
)

def outputData(pathname, search):
    if pathname == '/fulfill_order':
        parsed = urlparse(search)
        order_id = parse_qs(parsed.query)['id'][0]

        sql = """
        SELECT co_name, co_address from customer_order
        WHERE order_id = %s
        """

        values = [order_id]
        cols = ['name', 'address']
        df = db.querydatafromdatabase(sql,values,cols)
        customer_name = df['name'].values.tolist()
        customer_address = df['address'].values.tolist()

        sql2 = """
                SELECT product_name, order_qty , product.product_price
                from co_product
                inner join product on product.product_id = co_product.product_id
                where co_product.order_id = %s
            """

        values2 = [order_id]
        cols2 = ['Product', 'Qty', 'Unit Price']

        df2=db.querydatafromdatabase(sql2, values2, cols2)
        table = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True, size='sm')

        #computing total bill
        sql3 = """
        SELECT sum(co_product.order_qty* product.product_price)
        from co_product inner join product on product.product_id = co_product.product_id
        where co_product.order_id = %s       
        """
        
        values3 = [order_id]
        cols3 = ['Total']

        df3=db.querydatafromdatabase(sql3, values3, cols3)

        total_bill = df3['Total'].values.tolist()
        return order_id, customer_name, customer_address, table, total_bill
    
@app.callback(
    [
        Output('confirm_modal','is_open'),
        Output('close','is_open'),

        Output('modal1','children'),
        Output('modal2','children'),
        Output('modal_message','children')
    ],
    [
        Input('fulfill_order','n_clicks'),
        Input('cancel_order', 'n_clicks'),
        Input('confirm','n_clicks'),
        Input('order_number','value')
    ],
    State('confirm_modal','is_open')
)
def openModalCO(fulfill_order, cancel_order, confirm, order_number, modal):
    close = False
    modal1 = ''
    modal2 = ''
    message = ''
    if fulfill_order:
        modal = not modal
        modal1 = 'Confirmation'
        message = 'Confirm Release of Product'
        if confirm:
            modal2 = modal1
            sql = """
            update customer_order
            set status_id = 2
            where order_id = %s
            """

            values = [order_number]
            db.modifydatabase(sql, values)
            close = True
    elif cancel_order:
        modal = not modal
        modal1 = 'Cancellation'
        message = 'Confirm Cancellation of Order'
        if confirm:
            modal2 = modal1
            sql = """
            update customer_order
            set status_id = 3
            where order_id = %s
            """

            values = [order_number]
            db.modifydatabase(sql, values)
            close = True

    return [modal, close, modal1, modal2, message]