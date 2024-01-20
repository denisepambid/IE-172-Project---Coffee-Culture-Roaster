from dash import dcc, html
import dash_bootstrap_components as dbc 
import dash 
from dash.exceptions import PreventUpdate

navlink_style = {
    'color': '#fff', #change color of navbar
}

navbar = dbc.NavbarSimple(
    children = [
        dbc.NavItem(
            [
                dbc.NavLink("Suppliers", href='/suppliers'),
            ]
        ),     
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Production Log', href='/productionlog'),
                dbc.DropdownMenuItem("Record Production", href='/recordproduction')
            ],
            nav=True,
            in_navbar=True,
            label='Production'
        ),     
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Warehouse", href="/warehouseinventory"),
                dbc.DropdownMenuItem("Products", href="/productlist"),
            ],
            nav=True,
            in_navbar=True,
            label = "Inventory"
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Customer Order", href="/orderlist"),
                dbc.DropdownMenuItem("Purchase Order", href="/purchaseorder"),
            ],
            nav=True,
            in_navbar=True,
            label = "Orders"
        ),
        dbc.NavItem(
            [
                dbc.NavLink("Logout", href='/login'),
            ]
        ),  
    ],
    brand="COFFEE CULTURE ROASTERY",
    brand_href="/home",
    color="#7d2c01",
    dark=True,
)