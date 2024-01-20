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
                    html.H2('Product List'),
                    width="auto"
                ),

                dbc.Col(
                    html.Div(
                        [
                            dbc.RadioItems(
                                id="productbuttons",
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": "All", "value": 1},
                                    {"label": "Specialty Coffee", "value": 2},
                                    {"label": "Premium Blends", "value": 3},
                                    {"label": "Single Origin", "value": 4},
                                ],
                                value=1,
                            ),
                        ],
                        className="radio-group",
                    )
                ),
                   
                dbc.Col(
                    dbc.Button(
                        "Add Product",
                        href="/addproduct", style={'background-color':"#ae7a31"}
                    ),
                    width='auto',
                ),
            ]
        ),
        
        dbc.Card(
            [
                dbc.Row(
                    html.Div(
                        id='product_list',
                    ),
                )
            ]
        ),
    ]
)

@app.callback(
    [
        Output('product_list', 'children')
    ],
    [
        Input('productbuttons','value')
    ]
)

def productinventory_specificproducts(value):
    if value == 1:
        sql = """  SELECT product_name, sum(product_qty-co_product.order_qty) as inventory, product_type, product.product_id
            from product 
            FULL OUTER JOIN production_supply on product.product_id = production_supply.product_id
            FULL OUTER JOIN co_product on co_product.product_id = production_supply.product_id
            and is_active is True
            group by product_name, product_type,product.product_id
        """
        values = []

        cols = ['Product Name', 'Current Inventory', 'Product Type', 'Product ID']

        df = db.querydatafromdatabase(sql, values, cols)

        buttons = []
        for product_id in df['Product ID']:
            buttons += [
                html.Div(
                    dbc.Button('Edit', href=f'editproducts?id={product_id}', size='sm', color='link'),
                    style={'text-align': 'center'}
                )
            ]
        df['Action'] = buttons

        df = df[['Product Name', 'Current Inventory', 'Product Type', 'Action']] 

        sorted_df = df.sort_values(by=['Product Name'], ascending=True)   

        products=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
        return[products]

    elif value == 2:
        sql = """ SELECT product_name, sum(product_qty-co_product.order_qty) as inventory, product.product_id
            from product 
            FULL OUTER JOIN production_supply on product.product_id = production_supply.product_id
            FULL OUTER JOIN co_product on co_product.product_id = product.product_id
            where is_active is True
            and product_type = 'Specialty Coffee'
            group by product_name, product_type,product.product_id
        """
    
        values = []

        cols = ['Product Name', 'Current Inventory', 'Product ID']

        df = db.querydatafromdatabase(sql, values, cols)

        buttons = []
        for product_id in df['Product ID']:
            buttons += [
                html.Div(
                    dbc.Button('Edit', href=f'editproducts?id={product_id}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            ]
        df['Action'] = buttons

        df = df[['Product Name', 'Current Inventory', 'Action']] 
        sorted_df = df.sort_values(by=['Product Name'], ascending=True)

        specialty_coffee=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
        return[specialty_coffee]
    
    elif value == 3:
        sql = """ SELECT product_name, sum(product_qty-co_product.order_qty) as inventory, product.product_id
            from product 
            FULL OUTER JOIN production_supply on product.product_id = production_supply.product_id
            FULL OUTER JOIN co_product on co_product.product_id = product.product_id
            where is_active is True
            and product_type = 'Premium Blends'
            group by product_name, product_type,product.product_id
        """
    
        values = []

        cols = ['Product Name', 'Current Inventory', 'Product ID']

        df = db.querydatafromdatabase(sql, values, cols)

        buttons = []
        for product_id in df['Product ID']:
            buttons += [
                html.Div(
                    dbc.Button('Edit', href=f'editproducts?id={product_id}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            ]
        df['Action'] = buttons

        df = df[['Product Name', 'Current Inventory', 'Action']] 
        sorted_df = df.sort_values(by=['Product Name'], ascending=True)

        premium_blends=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
        return[premium_blends]
    
    elif value == 4:
        sql = """ SELECT product_name, sum(product_qty-co_product.order_qty) as inventory, product.product_id
            from product 
            FULL OUTER JOIN production_supply on product.product_id = production_supply.product_id
            FULL OUTER JOIN co_product on co_product.product_id = product.product_id
            where is_active is True
            and product_type = 'Single Origin'
            group by product_name, product_type,product.product_id
        """
    
        values = []

        cols = ['Product Name', 'Current Inventory', 'Product ID']

        df = db.querydatafromdatabase(sql, values, cols)

        buttons = []
        for product_id in df['Product ID']:
            buttons += [
                html.Div(
                    dbc.Button('Edit', href=f'editproducts?id={product_id}', size='sm', color='warning'),
                    style={'text-align': 'center'}
                )
            ]
        df['Action'] = buttons

        df = df[['Product Name', 'Current Inventory', 'Action']] 
        sorted_df = df.sort_values(by=['Product Name'], ascending=True)

        single_origin=dbc.Table.from_dataframe(sorted_df, striped=True, bordered=True, hover=True, size='sm') 
        return[single_origin]

    else:
        raise PreventUpdate
    