from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser
import numpy
import home
from apps import commonmodules as cm
from app import app
import orderlist
import add_orders
import change_order_status
import productlist
import purchaseorder
import create_po
import removeorder
import removesupply
import change_POStatus
import addproduct
import editproduct
import supplierlist
import addsupplier
import recordproduction
import productionlog
import removerecordsupply
import warehouse
import editsuppliers
import addsupply
import login

CONTENT_STYLE={
    "margin-top": "em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [   
        dcc.Location(id='url', refresh=True),
        cm.navbar, 
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)



@app.callback(
    [
        Output('page-content', 'children'),
    ],
    [
        Input('url', 'pathname'),
    ],
)

def displaypage(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if pathname == '/'  or pathname == '/login':
                returnlayout = login.layout
            elif pathname == '/home':
                returnlayout = home.layout
            elif pathname == '/orderlist':
                returnlayout = orderlist.layout
            elif pathname == '/add_order':
                returnlayout = add_orders.layout
            elif pathname == '/purchaseorder':
                returnlayout = purchaseorder.layout
            elif pathname == '/create_po':
                returnlayout = create_po.layout
            elif pathname == '/fulfill_order':
                returnlayout = change_order_status.layout
            elif pathname == '/fulfill_PO':
                returnlayout = change_POStatus.layout
            elif pathname == '/removeorder':
                returnlayout = removeorder.layout
            elif pathname == '/removesupply':
                returnlayout = removesupply.layout
            elif pathname == '/recordproduction':
                returnlayout = recordproduction.layout
            elif pathname == '/productionlog':
                returnlayout = productionlog.layout
            elif pathname == '/removerecordsupply':
                returnlayout = removerecordsupply.layout
            elif pathname == '/productlist':
                returnlayout = productlist.layout
            elif pathname == '/addproduct':
                returnlayout = addproduct.layout
            elif pathname == '/editproducts':
                returnlayout = editproduct.layout
            elif pathname == '/warehouseinventory':
                returnlayout = warehouse.layout
            elif pathname == '/additem':
                returnlayout = addsupply.layout
            elif pathname == '/suppliers':
                returnlayout = supplierlist.layout
            elif pathname == '/addsupplier':
                returnlayout = addsupplier.layout
            elif pathname == '/editsuppliers':
                returnlayout = editsuppliers.layout
        
            else:
                returnlayout = 'error404'
            return [returnlayout]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050', autoraise=True)
    app.run_server(debug=False)

