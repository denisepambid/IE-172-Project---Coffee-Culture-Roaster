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
        html.Br(),
    
        dbc.Row(
            [
                dbc.Col(html.H2('Production Log'),
                        width=8),
                dbc.Col(
                    dbc.Button('Record Production', href='/recordproduction', 
                    style={'background-color':'#ae7a31'}, size='lg',
                    className='d-grid gap-2'
                    ),
                    width=3
                )
            ]
        ),
        html.Br(),

        html.Hr(),
        dbc.Row(
            [
                dbc.Col(width=1),
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Search Date"),
                                dcc.DatePickerSingle(
                                        id = 'date-filter',
                                        placeholder='Search Date',
                                    ),
                            ],
                            size='sm'
                        )
                    ]
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(width=1),
                dbc.Col(
                    html.Div(id='production_log')
                ),
                dbc.Col(width=1)
            ]
        )
   ]
)

@app.callback(
    Output('production_log','children'),
    [
        Input('url','pathname'),
        Input('date-filter','date')
    ]
)

def showProductionLog(pathname, date):
    if pathname == '/productionlog':
        sql = """
        select production.prod_no, prod_date, supply_name, product_name
        from production_supply x
        inner join production on production.prod_no = x.prod_no
        inner join supply on supply.supply_id = x.supply_id
        inner join product on product.product_id = x.product_id
        """
        values = []

        if date:
            sql += "and prod_date = %s"
            values += [date]
        
        cols = ['Prod No', 'Date', 'Supply','Product']
        df = db.querydatafromdatabase(sql, values,cols)
        log = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

        return [log]