from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

import calendar
from datetime import date
from apps import dbconnect as db
from app import app

layout = html.Div(
    [
        dbc.Row(
            html.H2('Overview')
        ),
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.Row(
                            html.B(
                                    html.H4("Monthly Summary")
                                )
                                ),
                        dbc.Row(
                            [
                                dbc.Col(width=3),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.H4(
                                                html.Div(id='fulfilled-orders', style={'text-align':'center'})
                                            )
                                        ),
                                        dbc.Row(
                                            html.Div("Fulfilled Orders", style={'text-align':'center'})
                                        )
                                    ]
                                ),
                                
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            html.H4(
                                                html.Div(id='gross-revenue'),
                                                style={'text-align':'center'}
                                            )
                                        ),
                                        dbc.Row(html.Div('Gross Revenue (Php)'), style={'text-align':'center'}),
                                    ]
                                ),
                            ]
                        )
                    ], style={'padding':'1em 1em'}
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        dbc.Row(html.B("Best Selling Products")),
                                        dbc.Row(html.I("Top 5 Products"))
                                    ]
                                ),
                                dbc.CardBody(
                                    html.Div(id = 'top-sellers', 
                                             style={'padding': '1em 1em'})
                                )
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(html.B("Top Suppliers")),
                                dbc.CardBody(
                                    html.Div("top suppliers", id='top-suppliers')
                                )
                            ]
                        )
                    ],
                    width=5
                ),

                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        dbc.Row(html.B("Low Inventory Summary")),
                                        dbc.Row(html.I("Product Inventory below 30, Supply Inventory below 50"))
                                    ]
                                ),
                                dbc.CardBody(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div('products',id='low-inventory-products',
                                                style={'padding':'1em 1em'})
                                            ),
                                            dbc.Col(
                                                html.Div('supply',id='low-inventory-supply',
                                                         style={'padding':'1em 1em'})
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.B("Customer Orders")),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    html.B(
                                                        html.Div('3', id = 'active-customer-orders')
                                                    )
                                                ),
                                                dbc.Row("Active")
                                            ]
                                        )
                                    ]
                                )
                            ],
                            style={'padding':'1em 1em'}
                        ),
                        html.Br(),
                        dbc.Card(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.B("Purchase Orders")),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    html.B(html.Div('5', id = 'active-purchase-orders'))
                                                ),
                                                dbc.Row("Active")
                                            ]
                                        )
                                    ]
                                ),
                            ], 
                            style={'padding':'1em 1em'}
                        )
                    ]
                )
            ]
        )
        
    ]
)

@app.callback(
    [
        Output('fulfilled-orders', 'children'),
        Output('gross-revenue', 'children'),
        Output('top-sellers', 'children'),
        Output('top-suppliers', 'children'),
        Output('low-inventory-products', 'children'),
        Output('low-inventory-supply', 'children'),
        Output('active-customer-orders', 'children'),
        Output('active-purchase-orders', 'children')
    ],
    [
        Input('url','pathname')
    ]
)

def showOutputs(pathname):
    #compute date
    today = date.today()
    lastday = calendar.monthrange(today.year, today.month)
    lastday = lastday[1]

    startdate = date(today.year, today.month, 1)
    enddate = date(today.year, today.month, lastday)

    #show fulfilled orders
    sql = """
        select count(*) 
        from customer_order
        where order_date <= %s
        and order_date >= %s
        and status_id = 2
        """
    
    values = [enddate, startdate]
    cols = ['count']
    df = db.querydatafromdatabase(sql, values, cols)
    fulfilled_orders = df['count']

    #show gross revenue
    sql1 = """
        SELECT sum(pr.product_price*cp.order_qty) as total_revenue
        FROM customer_order co
        LEFT JOIN co_product cp on co.order_id = cp.order_id
        INNER JOIN product pr on pr.product_id = cp.product_id
        WHERE co.status_id = 2
        AND co.order_date <= %s
        AND co.order_date >= %s
    """
    values1 = [enddate, startdate]
    cols1 = ['total']
    df1 = db.querydatafromdatabase(sql1, values1, cols1)
    revenue = df1['total']

    #select low inventory
    sql2 =  """
        select supply_name
        from supply
        where current_inventory < 50
    """
    values2 = []
    cols2 = ['Supply Name']
    df2 = db.querydatafromdatabase(sql2, values2, cols2)
    lowsupply = dbc.Table.from_dataframe(df2.head(), striped=True, bordered=True, hover=True, size='sm')

    sql3 =  """
        select product_name
        from product
        where inventory_level < 30
    """
    values2 = []
    cols2 = ['Product Name']
    df2 = db.querydatafromdatabase(sql2, values2, cols2)
    lowprod = dbc.Table.from_dataframe(df2.head(), striped=True, bordered=True, hover=True, size='sm')

    #top sellers
    sql3 = """
        select product_name, sum(order_qty) as summ
        from co_product
        inner join product on product.product_id = co_product.product_id
        inner join customer_order on customer_order.order_id = co_product.order_id
        and order_date <= %s
        and order_date >= %s
        group by product_name
        order by summ desc
        """
    values3 = [enddate, startdate]
    cols3 = ['Product Name','Qty']
    df3 = db.querydatafromdatabase(sql3, values3, cols3)
    top_sellers = dbc.Table.from_dataframe(df3.head(), striped=True, bordered=True, hover=True, size='sm')

    #top suppliers
    sql3 = """
        select supplier_name, count(*) as total
        from purchaseorder
        inner join supplier_supply on supplier_supply.supplier_id = purchaseorder.supplier_id
        inner join supplier on supplier.supplier_id = supplier_supply.supplier_id
        and po_date <= %s
        and po_date >= %s
        group by supplier_name
        order by total desc
        """
    values3 = [enddate, startdate]
    cols3 = ['Supplier Name','Total Fulfilled Orders']
    df3 = db.querydatafromdatabase(sql3, values3, cols3)
    top_suppliers = dbc.Table.from_dataframe(df3.head(), striped=True, bordered=True, hover=True, size='sm')

    #customer order
    sql4 = """
        select count(*)
        from customer_order co
        where co.status_id = 1
        and order_date <= %s
        and order_date >= %s
    """
    values4 = [enddate, startdate]
    cols4 = ['count']
    df4 = db.querydatafromdatabase(sql4, values4, cols4)
    active_co = df4['count'].head()

    #purchase order
    sql5 = """
        select count(*)
        from purchaseorder po
        where po.status_id = 1
        and po_date <= %s
        and po_date >= %s
    """
    values5 = [enddate, startdate]
    cols5 = ['count']
    df5 = db.querydatafromdatabase(sql5, values5, cols5)
    active_po = df5['count']

    return [fulfilled_orders, revenue, top_sellers, top_suppliers, lowsupply, lowprod, active_co, active_po]
