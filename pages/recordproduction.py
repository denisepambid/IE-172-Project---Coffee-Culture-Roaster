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
        html.Br(),
        html.H2('Record Production'),
        html. Br(),
        html.Hr(),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(width=2),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Choose Product"),
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(width=2),
                                            dbc.Col(
                                                dcc.Dropdown(placeholder='Choose Product', id='product-options',
                                                            disabled=False),
                                                width=6
                                            ),
                                            dbc.Col(
                                                dbc.Input(placeholder='Qty',id='product-qty'),
                                                width=2
                                            )
                                        ]
                                    )
                                ]
                            ),
                            dbc.CardFooter(
                                dbc.Button('Confirm Product', id='confirm-product',n_clicks=0,
                                        disabled=False, style={'background-color':"#ae7a31"}
                                ), 
                                className="d-grid gap-2 d-md-flex justify-content-md-end"
                            )
                        ]
                    ),
                ),
                dbc.Col(width=2)
            ]
        ),
        
        html.Br(),
        
        dbc.Row(
            [
                dbc.Col(
                    html.Div("Production Number:", style={'text-align':'right'}),
                    width='4'
                ),
                dbc.Col(
                    html.Div('#', id='production-number', 
                             style={'text-align':'left'}),
                    width='auto'
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(width=3),
                dbc.Col(
                    dcc.Dropdown(placeholder='Choose Supply', id='supply-list',
                                 disabled = True)
                ),
                dbc.Col(
                    dbc.Input(placeholder='Qty', id='supply-qty',
                              disabled=True),
                    width=1
                ),
                dbc.Col(
                    dbc.Button(
                        "Record Usage", id='confirm-supply', n_clicks=0, 
                        disabled=True, style={'background-color':"#ae7a31"}
                    )
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Button('Refresh', id = 'refresh-recordproduction',n_clicks=0, color='link')
        ),

        html.Div(id='show-prod-history'),

        html.Br(),
        dbc.Row(
            [
                dbc.Col(width=4),
                dbc.Col(
                    dbc.Button('Finish record', id='finish-record', n_clicks=0, disabled=True, style={'background-color':"#ae7a31"}),
                    className="d-grid gap-2", 
                ),
                dbc.Col(width=4),
            ]
        ),

        dbc.Modal(  
            [
                dbc.ModalHeader('Confirmation'),
                dbc.ModalBody('Confirm product'),
                dbc.ModalFooter(dbc.Button('Confirm',id='add-product', n_clicks=0, style={'background-color':"#ae7a31"}))
            ],
            id = 'add-product-modal', is_open=False
        ),

        dbc.Modal(  
            [
                dbc.ModalHeader('Error'),
                dbc.ModalBody('Check Inputs'),
                dbc.ModalFooter(dbc.Button('Confirm',id='record-error', n_clicks=0, style={'background-color':"#ae7a31"}))
            ],
            id = 'record-error-modal', is_open=False
        ),

        dbc.Modal(
            [
                dbc.ModalHeader('Confirmation'),
                dbc.ModalBody('Confirm supply'),
            ],
            id = 'add-supply-modal', is_open=False
        ),

        dbc.Modal(
            [
                dbc.ModalHeader('Finish Record Production'),
                dbc.ModalBody('Recording Done'),
                dbc.ModalFooter(
                    dbc.Button('Confirm',href='/home', style={'background-color':"#ae7a31"})
                    )
            ],
            id = 'finish-recording-modal', is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('product-options','options'),
        Output('supply-list','options')
    ],
    Input('url','pathname')
)
def loadProductList(pathname):
    if pathname == '/recordproduction':
        sql2 = """SELECT product_name, product_id from product """
        values2 = []
        cols2 = ['label', 'value']
        df2=db.querydatafromdatabase(sql2, values2, cols2)
        products = df2.to_dict('records')

        sql3 = """SELECT supply_name, supply_id from supply """
        values3 = []
        cols3 = ['label', 'value']
        df3=db.querydatafromdatabase(sql3, values3, cols3)
        supplies = df3.to_dict('records')

        return products, supplies
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('add-product-modal','is_open'),
        Output('record-error-modal','is_open'),
        Output('product-options', 'disabled'),
        Output('confirm-product','disabled'),
        Output('supply-list','disabled'),
        Output('supply-qty','disabled'),
        Output('confirm-supply', 'disabled'),
        Output('production-number','children'),
        Output('finish-record','disabled')
    ],
    [
        Input('confirm-product','n_clicks'),
        Input('add-product','n_clicks'),
    ],
    [
        State('add-product-modal','is_open'),
        State('record-error-modal','is_open'),
        State('product-options', 'value'),
        State('product-qty','value')
    ]
)

def addProductionProduct(n_clicks, add_product, confirm, error, product, qty):
    disabled = False
    prod_no = ""
    if n_clicks:
        if product and qty:
            confirm = not confirm
            if add_product:
                disabled = True

                #add production no
                sql = """INSERT INTO production(prod_date)
                values (%s)"""

                values = [date.today()]
                db.modifydatabase(sql, values)

                #get prod_no
                sql2 = """
                SELECT max(prod_no) from production
                """
                values2 = []
                cols2 = ['prod_no']
                df2 = db.querydatafromdatabase(sql2, values2, cols2)
                prod_no = df2.iat[0,0]

                sql3 = """
                SELECT inventory_level from product
                WHERE product_id = %s
                """

                #values3 = [product]
                #cols3 = ['value']
                #df3 = db.querydatafromdatabase(sql3, values3, cols3)
                #old_inv = df3['value']
                #print(old_inv[0])

                #new_inv = old_inv + int(qty)
                #sql4 = """
                #update product
                #set inventory_level = %s
                #where product_id = %s"""

                #values4 = [new_inv]
                #db.modifydatabase(sql4,values4)
                



        else: 
            error = not error
        return [confirm, error, disabled, disabled, not disabled, not disabled, not disabled, prod_no, not disabled]
    
    else: 
        raise PreventUpdate
    
    
@app.callback(
    Output('finish-recording-modal','is_open'),
    Input('finish-record','n_clicks')
)

def finishRecording(n_clicks):
    if n_clicks:
        return True
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('add-supply-modal','is_open'),
        Output('show-prod-history','children'),
        Output('supply-list','value'),
        Output('supply-qty','value')
    ],
    [
        Input('confirm-supply','n_clicks'),
        Input('product-options', 'value'),
        Input('product-qty','value'),
        Input('refresh-recordproduction','n_clicks')
    ],
    [
        State('supply-list','value'),
        State('supply-qty','value'),
        State('add-supply-modal','is_open'),
    ]
)

def openModalProduction(confirm, product, Pqty, refresh, supply, Sqty, modal):
    if product and Pqty:
        sql = """
            SELECT max(prod_no) from production
            """
        values = []
        cols = ['prod_no']
        df = db.querydatafromdatabase(sql, values, cols)
        prod_no = int(df.iat[0,0])

        sql2 = """select supply_name, supply_qty
                from supply 
                inner join production_supply x 
                on supply.supply_id = x.supply_id
                and x.prod_no = %s"""
        values2 = [prod_no]
        cols2 = ['Supply','Amount']
        df2 = db.querydatafromdatabase(sql2, values2, cols2)
        
    if confirm:
        if supply and Sqty:
            modal = not modal
            
            sql3 = """
            INSERT INTO production_supply(prod_no, supply_id, supply_qty,product_id,product_qty)
            VALUES (%s, %s, %s, %s, %s)
            """
            values3 = [prod_no, supply, int(Sqty), product, Pqty]
            db.modifydatabase(sql3, values3)

            sql2 = """select supply_name, supply_qty
                    from supply 
                    inner join production_supply x 
                    on supply.supply_id = x.supply_id
                    and x.prod_no = %s"""
            values2 = [prod_no]
            cols2 = ['Supply','Amount']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)
        
            if df.shape:
                buttons = []
                for supply_name in df2['Supply']:
                    buttons += [
                        html.Div(
                            dbc.Button(
                                html.Div(
                                html.A("Remove", href=f'/removerecordsupply?prod_no={prod_no}&supply_id={supply}', target="_blank"),
                                style={'text-align':'center'}
                                ),
                                color='link'
                            ),
                        )
                    ]
                
                df2['Action'] = buttons
                df2 = df2[['Supply','Amount','Action']]
                table = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True, size='sm')
            
        elif refresh:
            sql2 = """select supply_name, supply_qty
                    from supply 
                    inner join production_supply x 
                    on supply.supply_id = x.supply_id
                    and x.prod_no = %s"""
            values2 = [prod_no]
            cols2 = ['Supply','Amount']
            df2 = db.querydatafromdatabase(sql2, values2, cols2)
        
            if df.shape:
                buttons = []
                for supply_name in df2['Supply']:
                    buttons += [
                        html.Div(
                            dbc.Button(
                                html.Div(
                                html.A("Remove", href=f'/removerecordsupply?prod_no={prod_no}&supply_id={supply}', target="_blank"),
                                style={'text-align':'center'}
                                ),
                                color='link'
                            ),
                        )
                    ]
                
                df2['Action'] = buttons
                df2 = df2[['Supply','Amount','Action']]
                table = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True, size='sm')
        supply = ''
        Sqty = ''
    return [modal, table, supply, Sqty]
        
