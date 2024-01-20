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
        html.H2("Purchase Order"),
        html.Hr(),

        dbc.Collapse(
            [
                dbc.Row(
                    [
                        dbc.Col(width=2),
                        dbc.Col('Choose Supplier:', width = 'auto'),
                        dbc.Col(
                            dcc.Dropdown(placeholder='Supplier', id='supplier'),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Button('Create Purchase Order', id='create_newpo', n_clicks=0,
                                       style={'background-color':"#ae7a31"}),
                            width = 3
                        )
                    ]
                ),
            ],
            id = 'choose_supplier',
            is_open=True
        ),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col('Supplier:', width = 2),
                dbc.Col(html.Div(id='supp_name'), width='auto')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col('Supplier Address: ', width=2),
                dbc.Col(html.Div(id = 'Saddress'), width='auto')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col('Supplier Co. Number: ', width=2),
                dbc.Col(html.Div(id = 'Scontact'), width='auto')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col('Supplier Email: ', width=2),
                dbc.Col(html.Div(id = 'Semail'), width='auto')
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Hr(),
                )
            ]
        ),

        dbc.Collapse(
            [
                dbc.Row(
                    [
                        dbc.Col(width=2),
                        dbc.Col(
                            dbc.Label('Product:'),
                            width=1
                        ),
                        dbc.Col(
                            dcc.Dropdown(placeholder='Choose Product', id = 'product'),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Input(placeholder='Qty', id='qty'),
                            width=1
                        ),
                        dbc.Col(
                            dbc.Input(placeholder='Price', id='price', type='float'),
                            width = 1
                        ),
                         dbc.Col(
                            dbc.Button('Add Order', id='add_order', n_clicks=0, color='link')
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Button('Refresh List', id='refresh', n_clicks=0, color='link')),
                    ],
                    style={
                        'text-align':'center'
                    }
                ),
                dbc.Row(
                    html.Div(id='show_orders')
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(width=2),
                        dbc.Col(
                            dbc.Button('Finish Order', id='finish_order', n_clicks=0,
                                style={'background-color':"#ae7a31"}),
                                className='d-grid gap-2'
                           ),
                           dbc.Col(width=2)
                    ], 
                    )
            ],
            id = 'show_product', is_open = False
        ),

        dbc.Modal(
            [
                dbc.ModalHeader("Alert"),
                dbc.ModalBody("Finishing Purchase Order"),
                dbc.ModalFooter(
                    dbc.Button("Confirm", href='purchaseorder',
                               style={'background-color':"#ae7a31"})
                )
            ],
            id='finish',
            is_open = False
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Alert"),
                dbc.ModalBody("Check Input")
            ],
            id = 'error_modal',
            is_open = False
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Alert"),
                dbc.ModalBody("Check Input")
            ],
            id = 'error_modal2',
            is_open = False
        )

    ],
)

@app.callback(
    Output('supplier','options'),
    Input('url', 'pathname')
)

def showsuppliers(pathname):
    if pathname == '/create_po':
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
        Output('supp_name','children'),
        Output('Saddress', 'children'),
        Output('Scontact', 'children'),
        Output('Semail', 'children'),
        Output('product','options'),
    ],
    Input('supplier','value')
)

def supplierchosen(supplier):
    if supplier:
        #show details of the supplier
        sql = """SELECT supplier_name, supplier_address, supplier_contactno, supplier_email from supplier
            WHERE supplier_id = %s"""
        values = [supplier]
        cols = ['name','address', 'contact', 'email']
        df=db.querydatafromdatabase(sql,values,cols)
        
        name = df['name'].values.tolist()
        address =df['address'].values.tolist()
        contact =df['contact'].values.tolist()
        email = df['email'].values.tolist()
        
    
        #show products of supplier
        sql2 = """ 
        select supply_name, ss.supply_id 
        from supplier_supply ss 
        inner join supply on ss.supply_id= supply.supply_id
        where supplier_id = %s
        """
        values2 = [supplier]
        cols2 = ['label', 'value']
        df2=db.querydatafromdatabase(sql2, values2, cols2)
        products = df2.to_dict('records')

        #show orders
        ##get PO number
        sql3 = """
            SELECT max(order_id)
            from customer_order
        """
        values3 = []
        cols3 = ['value']

        df3=db.querydatafromdatabase(sql3, values3, cols3)
        order_number = df3.iat[0,0]
        
        return name,address, contact, email, products
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('choose_supplier','is_open'),
        Output('show_product','is_open'),
        Output('error_modal2', 'is_open')
    ],
    Input('create_newpo','n_clicks'),
    [
        State('choose_supplier','is_open'),
        State('supplier','value'),
        State('error_modal2', 'is_open')
    ]
)

def addPOtoDatabase (n_clicks, is_open, supplier, error_modal):
    if n_clicks:
        if supplier:
            is_open = not is_open

            sql = """
            INSERT INTO purchaseorder(supplier_id,status_id,po_date)
            VALUES (%s,1,%s)
            """
            values = [supplier,date.today()]
            db.modifydatabase(sql, values)
        else:
            error_modal = not error_modal

    return is_open, not is_open, error_modal

@app.callback(
    [
        Output('show_orders','children'),
        Output('product', 'value'),
        Output('qty','value'),
        Output('price','value'),
        Output('error_modal', 'is_open')
    ],
    [
        Input('add_order','n_clicks'),
        Input('refresh','n_clicks')
    ],
    [
        State('product','value'),
        State('qty','value'),
        State('price','value'),
        State('error_modal', 'is_open')
    ]
)

def addPOItemtoDatabase(addorder, refresh,product, qty, price, error_modal):
    if addorder:
        sql = """
            SELECT max(po_no)
            from purchaseorder
            """
        values = []
        cols = ['value']

        df=db.querydatafromdatabase(sql, values, cols)
        order_number = df.iat[0,0]
        if product and qty:
            sql2 = """
                INSERT INTO po_supply
                VALUES (%s, %s, %s, %s)
            """
            values2 = [int(order_number), int(product), float(qty), price]
            db.modifydatabase(sql2, values2)

            #show list of orders
            sql3 = """
                select supply_name, po_qty, supply.supply_id
                from po_supply
                inner join supply on supply.supply_id = po_supply.supply_id
                where po_no = %s
            """
            values3 = [int(order_number)]
            cols3 = ['Supply', 'Qty', 'ID']
            df3 = db.querydatafromdatabase(sql3, values3, cols3)
            
        elif refresh:
            sql3 = """
            select supply_name, po_qty, supply.supply_id
            from po_supply
            inner join supply on supply.supply_id = po_supply.supply_id
            where po_no = %s
            """
            values3 = [int(order_number)]
            cols3 = ['Supply', 'Qty', 'ID']
            df3 = db.querydatafromdatabase(sql3, values3, cols3)
            ##
                
        if df3.shape:
            buttons = []
            for supply_id in df3["ID"]:
                buttons += [
                    html.Div(
                        html.A("Remove", href=f'/removesupply?supply_id={supply_id}&po_number={order_number}', target="_blank"),
                        style={'text-align':'center'}
                    ),
                ]
            df3['Action'] = buttons
            df3 = df3[['Supply', 'Qty', 'Action']]

            table = dbc.Table.from_dataframe(df3, striped=True, bordered=True, hover=True, size='sm')
            return table, "","", '',error_modal
        else:
            return "", "","",'', not error_modal
    else:
        raise PreventUpdate

@app.callback(
    Output('finish','is_open'),
    Input('finish_order', 'n_clicks'),
)

def finishModal(finish_order):
    if finish_order:
        return True
    else:
        raise PreventUpdate
    

