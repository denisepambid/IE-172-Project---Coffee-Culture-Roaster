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

order_id = 0
product_order_id = 0
product_order_qty = 0 

order = []

remove_product_id = ""

layout = html.Div(
    [
        html.H2("Add Order"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [   dbc.Collapse(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Customer Name", width="3"),
                                        dbc.Col(
                                            dbc.Input(
                                                type = 'text',
                                                id = 'name_input',
                                                placeholder='Enter Customer Name',
                                            ),
                                            width=7,
                                        ),

                                    ],
                                    class_name="mb-3"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Customer Address", width="auto"),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='customer_address',
                                                placeholder='Customer Address'
                                            ),
                                            width="7"
                                        )
                                    ]
                                ),

                                html.Br(),

                                dbc.Row(
                                    [
                                        dbc.Button("Add Customer",
                                                id='customer-details',
                                                n_clicks=0,
                                                style={'background-color':"#ae7a31"}),
                                    ],
                                ),
                            ], 
                            is_open=True,
                            id='customer_info'
                        ),
                        
                        html.Br(),


                        dbc.Row(
                            [
                                dbc.Collapse(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader("Choose type of coffee:"),
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.RadioItems(
                                                                            id='choice',
                                                                            options=[
                                                                                {"label":"Specialty Coffee", "value":1},
                                                                                {"label":"Premium Blend", "value":2},
                                                                                {"label":"Single Origin", "value":3},
                                                                            ],
                                                                            
                                                                        )
                                                                    ]
                                                                ),
                                                                html.Hr(),
                                                                dbc.Row(html.Div(id='chosen-type')),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            dcc.Dropdown(
                                                                                id='specialty-coffee-products',
                                                                                placeholder = 'Choose product', 
                                                                            ),
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Input(placeholder='Qty', id='qty-specialty'),
                                                                            ],
                                                                            width=3,
                                                                        ),
                                                                    ],
                                                                    
                                                                ),
                                                                dbc.Row(
                                                                    dbc.Button(
                                                                        "Add Order", 
                                                                        color='link',
                                                                        id='add-specialty',
                                                                        n_clicks=0
                                                                    )
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ],
                                            width="auto",
                                        ),    
                                        html.Br(),
                                        dbc.Row(
                                            dbc.Button("Finish Order", id='finish_order', n_clicks=0, 
                                                       style={'background-color':"#ae7a31"})
                                        )
                                    ],
                                    id='order_toggle',
                                    is_open=False
                                ),
                                
                            ]
                        ),
                    ],
                    style={"left-margin": "2em","padding" : "1em 1em"}
                ),

                

                dbc.Col(width=1),
                dbc.Col(
                    dbc.Collapse(
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Order Summary:")),
                                        dbc.Col(html.Div(id='order-number')),
                                        html.Br(),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col('Customer Name:'),
                                        dbc.Col(html.Div(id='name_output')),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col('Customer Address:'),
                                        dbc.Col(html.Div(id='address_output')),
                                    ]
                                ),
                                html.Hr(),
                                dbc.Row(
                                    dbc.Button('Refresh Order List', id='refresh', n_clicks=0, color='link')
                                ),
                                dbc.Row(html.Div(id='order-list'))
                            ],
                            style={"padding": "1em 1em"}
                        ),
                        id='customer-receipt-toggle',
                        is_open=False,
                    ),
                    width=5,
                ),
            ],
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Add Order")),
                dbc.ModalBody(
                    [
                        dbc.Row("Confirm Order"),
                        dbc.Row(id='confirm-order'),
                    ],
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Add Order", id='add-order', n_clicks=0, 
                        ),
                    ]   
                ),
            ],
            id='order_confirmation',
            is_open=False
        ),

        dbc.Modal(
            [
                dbc.ModalHeader("Confirm Orders"),
                dbc.ModalBody(
                    [
                        dbc.Button("Confirm",
                                    id='confirm_orders_button', href='/orderlist',
                                    style={'background-color':"#ae7a31"},
                                    n_clicks=0)
                    ]
                )
            ],
            id='confirm_orders_modal',
            is_open = False
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Error Message"),
                dbc.ModalBody(
                    [
                        dbc.Button("Close",
                                    id='error_button',style={'background-color':"#ae7a31"},
                                    n_clicks=0)
                    ]
                )
            ],
            id = 'error',
            is_open = False
        )
    ]
)

@app.callback(
    [
        Output('name_output', 'children'),
        Output('address_output','children'), 
        Output('order_toggle','is_open'),
        Output('customer_info', 'is_open'),
        Output('customer-receipt-toggle','is_open'),
    ],
    Input('customer-details', 'n_clicks'),
    [
    State('name_input', 'value'),
    State('customer_address', 'value'),
    State('order_toggle','is_open')
    ],
)

#save customer details to database
def output_customer_details(n_clicks,name_input, customer_address, is_open):
    if not name_input:
        order_tog = is_open
    elif not customer_address:
        order_tog = is_open
    else:
        sql = '''INSERT INTO customer_order (co_name,co_address, status_id, order_date)
                VALUES (%s, %s, %s, %s)'''
        values = [name_input, customer_address, 1, date.today()]
        db.modifydatabase(sql, values)

        if n_clicks:
            order_tog = not is_open
        else:
            order_tog = is_open

    c_info = not order_tog
    receipt = order_tog

    return [name_input, customer_address, order_tog, c_info, receipt]

#--------------------Dropdown Selection---------------------------------#
@app.callback(
    [
        Output('specialty-coffee-products', 'options'),
        Output('chosen-type','children')
    ],
    [
        Input("choice", "value"),
    ],
)

def specialty_coffee_products(value):
    
    if value == 1:
        c_type = 'Specialty Coffee'
        sql = """
            SELECT product_name as label, product_id as value
            FROM product
            WHERE product_type = 'Specialty Coffee'
        """
    
    elif value == 2:
        c_type = 'Premium Blends'
        sql = """
            SELECT product_name as label, product_id as value
            FROM product
            WHERE product_type = 'Premium Blends'
        """

    elif value == 3:
        c_type = 'Single Origin'
        sql = """
            SELECT product_name as label, product_id as value
            FROM product
            WHERE product_type = 'Single Origin'
        """
    
    else:
        c_type="All Products"
        sql = """
            SELECT product_name as label, product_id as value
            FROM product
        """
    values = []
    cols = ['label', 'value']

    df=db.querydatafromdatabase(sql, values, cols)
    specialty_coffee_products_option = df.to_dict('records')
    return [specialty_coffee_products_option, c_type]
   
    
@app.callback(
    [
        Output('premium-coffee-products', 'options'),
    ],
    [
        Input("url", "pathname"),
    ],
)   
#----------------------- Show order ID ------------------------#
@app.callback(
    Output('order-number','children'),
    [
        Input('customer-details', 'n_clicks'),
    ]
)

def output_order_number(click):
    if click:
        sql = """
            SELECT max(order_id)
            from customer_order
        """
        values = []
        cols = ['value']

        df=db.querydatafromdatabase(sql, values, cols)
        order_number = df.iat[0,0]

        return f'{order_number}'
    else:
        raise PreventUpdate

#--------------- add specialty product to database ---------------#
@app.callback(
    [
        Output('order_confirmation','is_open'),
        Output('confirm-order','children'),
        Output('specialty-coffee-products','value'),
        Output('qty-specialty', 'value'),
        Output('order-list','children'),
        Output('error', 'is_open')
    ],
    
    [   
        Input('add-specialty','n_clicks'),
        Input('add-order', 'n_clicks'),
        Input('error_button', 'n_clicks'),
        Input('refresh','n_clicks')
    ],
    
    [
        State('specialty-coffee-products','value'),
        State('qty-specialty','value'),
        State('order_confirmation','is_open'),
    ]
)

def open_modal(click, add_order, error_close, refresh, product, qty, is_open):
    product_name = ""
    
    sql = """
        SELECT max(order_id)
        from customer_order
        """
    values = []
    cols = ['value']

    df=db.querydatafromdatabase(sql, values, cols)
    order_number = df.iat[0,0]
    
    if click: 
        if product and qty:
            modal = True

            sql = """
                SELECT product_name as label, product_id as value
                FROM product
            """

            values = []
            cols = ['label', 'value']

            df=db.querydatafromdatabase(sql, values, cols)
            row = df.to_numpy()
            row = df.loc[df.value == product]
            row=row.to_numpy()

            if len(row) > 0:
                product_name = row[0][0]
                print(order)
            else: 
                product_name = ""

            if add_order and is_open == True:
                #get order number
                
                
                sql2 = """
                        INSERT INTO co_product(order_id, product_id, order_qty)
                        VALUES (%s, %s, %s)
                    """
                values2 = [int(order_number),int(product), qty]
                db.modifydatabase(sql2, values2)

                print("Add Order")
                print(int(order_number))
                modal = False
                product = 0
                qty = ""

                order.append(product_name)
                print(order)
                
            sql3 = """
                    SELECT max(order_id)
                    from customer_order
                    """
            values3 = []
            cols3 = ['value']

            df2=db.querydatafromdatabase(sql3, values3, cols3)
            order_number = df2.iat[0,0]
            
            sql4 = """
                select product.product_name, co_product.order_qty, co_product.product_id
                from co_product
                inner join product
                on product.product_id = co_product.product_id
                where co_product.order_id = %s
                """
            values4 = [int(order_number)]
            cols4 = ["Product Name", "Qty", "ID"]

            df3=db.querydatafromdatabase(sql4, values4, cols4)

            if df3.shape:
                buttons = []
                for product_id in df3["ID"]:
                    buttons += [
                        html.Div(
                            html.A("Remove", href=f'/removeorder?id={product_id}&ordernumber={order_number}', target="_blank"),
                            style={'text-align':'center'}
                        ),
                    ]
                df3['Action'] = buttons
                df3 = df3[['Product Name', 'Qty', 'Action']]


            table = dbc.Table.from_dataframe(df3, striped=True, bordered=True, hover=True, size='sm')
            error = False
        
        elif refresh:
            modal = False
            
            sql4 = """
                select product.product_name, co_product.order_qty, co_product.product_id, product_price
                from co_product
                inner join product
                on product.product_id = co_product.product_id
                where co_product.order_id = %s
                """
            values4 = [int(order_number)]
            cols4 = ["Product Name", "Qty", "Price", "ID"]

            df3=db.querydatafromdatabase(sql4, values4, cols4)

            if df3.shape:
                buttons = []
                for product_id in df3["ID"]:
                    buttons += [
                        html.Div(
                            html.A("Remove", href=f'/removeorder?id={product_id}&ordernumber={order_number}', target="_blank"),
                            style={'text-align':'center'}
                        ),
                    ]
                df3['Action'] = buttons
                df3 = df3[['Product Name', 'Qty', 'Price', 'Action']]


            table = dbc.Table.from_dataframe(df3, striped=True, bordered=True, hover=True, size='sm')
            error = False
        else:
            modal = False
            error = True
            table = None

            if error_close:
                error = False
    else:
        raise PreventUpdate

    return [modal, f'{product_name}: {qty}', product, qty, table, error]

@app.callback(
    [
        Output('confirm_orders_modal','is_open'),
    ],
    [
        Input('finish_order', 'n_clicks'),
    ],
    [
        State('confirm_orders_modal', 'is_open'),
    ]
)

def ending_modal(finish_order,  modal_open):

    if finish_order:
        modal = not modal_open
    
    else:
        modal = modal_open
    
    return [modal]
