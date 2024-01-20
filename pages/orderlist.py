from dash import dcc 
from dash import html
import dash_bootstrap_components as dbc
import dash 
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import dash_table
from dash import dash_table
from apps import dbconnect as db
from app import app

layout = html.Div(
    [
    dbc.Card(
        dbc.CardBody(
                [
                    dbc.Row(
                        html.H2("Order List"),
                    ),
                    dbc.Row(
                        [
                            dbc.Button("Add Order", href='add_order',className="d-grid gap-2 col-6 mx-auto",
                                       style={'background-color':"#ae7a31"}),
                        ]
                    ),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                width=3
                            ),

                            dbc.Col(
                                dbc.Input(placeholder='Search Customer Name', id='customer_name', size='lg'),
                                width=5
                            ),
                            dbc.Col(
                                [
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Active", "value":1},
                                            {"label":"Fulfilled", "value": 2},
                                        ],
                                        value=[1],
                                        id="search_filter",
                                        inline=False,
                                    )
                                ],
                            )
                        ]
                    ), 
                    html.Br(),
                    dbc.Row(
                        [
                            html.Div("List goes here",
                                     id = 'orders_list')
                        ]
                    )
                ],
            ),
        ),
    ],
)

@app.callback(
    [
        Output('orders_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('customer_name','value'),
        Input('search_filter', 'value')
    ],
)

def orderlist_loadorders(pathname, searchterm, status):
    if pathname == '/orderlist':
        sql = """SELECT order_id, order_date, co_name, status
                FROM customer_order co
                    INNER JOIN status s on co.status_id = s.status_id
            """
        
        values = []
        cols = ['Order No', 'Date', 'Customer Name', 'Order Status']
        
        if searchterm:
            sql += " AND co_name ILIKE %s"
            values += [f"%{searchterm}%"]
        
        elif status:
            if status == [1]:
                sql += "AND co.status_id = 1 "
            elif status == [2]:
                sql += "AND co.status_id = 2"
            

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for order_id in df['Order No']:
                buttons += [
                    html.Div(
                        dbc.Button('View',
                                   href = f'/fulfill_order?mode=edit&id={order_id}',
                                    size = 'sm', color='link',),
                        style={'text-align':'center'}
                    ),
                ]
            df['Action'] = buttons
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No records"]
    
    
    else:
        raise PreventUpdate