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
        dbc.Row(
            [
                dbc.Col(
                    html.H2('Warehouse Inventory'),
                ),
                dbc.Col(
                    dbc.Button(
                        "Add Item",
                        href="/additem",
                    ),
                    width='auto',
                ),
                html.Hr(),
             ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    html.H5("CURRENT INVENTORY"),
                                ),
                            ]
                        ),
                        dbc.Col(
                            dbc.Input(placeholder='Search Supply Name', id='search-supply', size='md'),
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='current-inventory',
                            ),
                        )
                    ],
                    width = 4,
                ),
                dbc.Col(width = 1),
                dbc.Col(
                    [
                        dbc.Row(
                            html.H5("TO RECEIVE"),
                        ),
                        dbc.Row(
                            html.Div(
                                id='inbound-orders',
                            ),
                        )
                    ],
                    width = 7,
                    align='left',
                ),
            ],
        ),
    ]
)

@app.callback(
    [
        Output('current-inventory', 'children'),
        Output('inbound-orders', 'children'),
    ],
    [
        Input('url','pathname'),
        Input('search-supply', 'value')
    ]
)

def loadsuppliers(pathname, searchterm):
    if pathname == "/warehouseinventory":
        sqlorder = """
            SELECT s.supply_name, sum(ps.po_qty) as total_qty
            FROM purchaseorder po
            FULL OUTER JOIN PO_supply ps on ps.po_no = po.po_no
            FULL OUTER JOIN supply s on s.supply_id = ps.supply_id
            WHERE po.status_id = 1
            GROUP BY po.po_no, s.supply_name
        """
        values1 = []
        cols1 = ['Supply Item', 'Total Quantity (kg)']
        df1 = db.querydatafromdatabase(sqlorder, values1, cols1)
        orders = dbc.Table.from_dataframe(df1, striped=True, bordered=True, hover=True, size='sm')  

        sql = """ SELECT supply_name, sum(po_supply.po_qty-production_supply.supply_qty) as inventory
            from supply
            FULL OUTER JOIN po_supply on po_supply.supply_id = supply.supply_id
			FULL OUTER JOIN production_supply on production_supply.supply_id = supply.supply_id
            group by supply.supply_name, supply.supply_id
        """
        values = []

        cols = ['Supply Item', 'Quantity (kg)']

        if searchterm:
            sql += "WHERE supply_name ILIKE %s"
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols) 

        if df.shape:
            sorted_df = df.sort_values(by=['Supply Item'], ascending=True)    
            inventory=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
            return [inventory, orders]
        else: 
            return ["No records", orders]
    
    else:
        raise PreventUpdate
