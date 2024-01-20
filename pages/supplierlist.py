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
                    html.H2('Supplier List'),
                ),

                dbc.Col(
                    dbc.Button(
                        "Add Supplier",
                        href="/addsupplier",
                        style={'background-color':"#ae7a31"}
                    ),
                    width='auto',
                ),
            ]
        ),
        
        dbc.Card(
            [
                dbc.Row(
                    html.Div(
                        id='supplierlist',
                    ),
                )
            ]
        ),

        
    ]
)


@app.callback(
    [
        Output('supplierlist', 'children')
    ],
    [
        Input('url','pathname')
    ]
)

def loadsuppliers(pathname):
    if pathname == "/suppliers":
        sql = """ SELECT supplier_name, supplier_address, supplier_contactno, supplier_email, supplier_id
            FROM supplier
            WHERE is_active is True
        """
        values = []

        cols = ['Supplier Name', 'Address', 'Contact Number', 'Email', 'Supplier ID']

        df = db.querydatafromdatabase(sql, values, cols)

        buttons = []
        for supplier_id in df['Supplier ID']:
            buttons += [
                html.Div(
                    dbc.Button('Edit', href=f'editsuppliers?id={supplier_id}', size='sm', color='link'),
                    style={'text-align': 'center'}
                )
            ]
        df['Action'] = buttons

        df = df[['Supplier Name', 'Address', 'Contact Number', 'Email', 'Action']]

        sorted_df = df.sort_values(by=['Supplier Name'], ascending=True)     

        suppliers=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
        return[suppliers]
    
    else:
        raise PreventUpdate
    