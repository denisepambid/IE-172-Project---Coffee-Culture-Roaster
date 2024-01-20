from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from urllib.parse import urlparse, parse_qs
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Supplier Details"),
        html.Hr(),

        dbc.Alert(id='supplier-alert', is_open=False, color='danger'),
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Supplier Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='supplier-name', placeholder="Enter supplier name",
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Address", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='supplier-address', placeholder="Enter supplier address"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Contact Number", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="tel", id='supplier-number', placeholder="Enter contact number"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Email", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="email", id='supplier-email', placeholder="Enter supplier email"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Choose supply/ies:"),
                        dbc.Col(
                            id="supply-column"
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Switch(
                    id="new-suppliersupply",
                    label="New additional supply?",
                    value=False,
                ),
                dbc.Collapse(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Supply Name", width=2),
                                dbc.Col(
                                    dbc.Input(
                                    type="text", id='new-supply', placeholder="Enter supply name",
                                    ),
                                    width=10,
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Supply Description", width=2),
                                dbc.Col(
                                    dbc.Input(
                                    type="text", id='new-supplydesc', placeholder="Enter supply description",
                                    ),
                                    width=10,
                                ),
                            ]
                        ),
                    ],
                    id='additional-supplylist',
                    is_open=False,
                ),

                dbc.Button("Submit", id='add-supplier', n_clicks=None, className='me-2', style={'background-color':"#ae7a31"}),
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody("New supplier has been added."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/suppliers', id='supplier-modalbutton', className='me-1')
                )
            ],
            centered=True,
            id='supplier-successmodal',
            backdrop='static',
            is_open=False,
        )
    ]
)


@app.callback(
    Output('supply-column', 'children'),
    Input('url', 'pathname'),
)

def loadsupp(pathname):
    if pathname == '/addsupplier':
        loadsql = """
            SELECT supply_name as label, supply_id as value
            FROM supply
        """
        values = []
        col = ['label', 'value']

        df = db.querydatafromdatabase(loadsql, values, col)
        supplyoptions = df.to_dict('records')
        
        supply=dbc.Checklist(options=supplyoptions, value=[], id='supply-checklist')
        return [supply]

    else:
        raise PreventUpdate



@app.callback(
    Output('additional-supplylist', 'is_open'),
    Input('new-suppliersupply', 'value'),
    State('additional-supplylist', 'is_open')
)

def opentoggle(switch, collapse):
    if switch is not collapse:
        return not collapse
    else:
        PreventUpdate
    


@app.callback(
    [
        Output('supplier-alert', 'children'),
        Output('supplier-alert', 'is_open'),
        Output('supplier-successmodal', 'is_open'),
    ],
    [
        Input('add-supplier', 'n_clicks'),
    ],
    [
        State('supplier-name', 'value'),
        State('supplier-address', 'value'),
        State('supplier-number', 'value'),
        State('supplier-email', 'value'),
        State('supply-checklist', 'value'),
        State('new-supply', 'value'),
        State('new-supplydesc', 'value'),
        State('supplier-alert', 'is_open'),
        State('supplier-successmodal', 'is_open'),
    ]
)

def addsupplier(click, name, address, number, email, supplylist, addntsupply, addntsupplydesc, alertopen, modalopen):
    if click is not None:
        if name is None:
            return ["Kindly input supplier name", True, False]
        
        elif address is None:
            return ["Kindly input address", True, False]
        
        elif number is None:
            return ["Kindly input contact number", True, False]
        
        elif email is None:
            return ["Kindly input supplier email", True, False]
        
        elif supplylist == [] and addntsupply is None:
            return ["Kindly select supplies or input new supply", True, False]
        
        else:
            if addntsupply is not None:
                sql1 = """
                INSERT INTO supply(supply_name, supply_description)
                VALUES (%s, %s)
                """
                values1 = [addntsupply, addntsupplydesc]
                db.modifydatabase(sql1, values1)
            else:
                pass

            sql2 = """
                INSERT INTO supplier(supplier_name, supplier_address, supplier_contactno, supplier_email, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """
            values2 = [name, address, number, email, True]
            db.modifydatabase(sql2, values2)
            
            sql3 = """
                SELECT supplier_id
                FROM supplier
                WHERE supplier_name = %s
            """
            getsupplierid = [name]
            col = ['suppid']

            df = db.querydatafromdatabase(sql3, getsupplierid, col)

            supplierid = int(df['suppid'][0])
            
            for supplyid in supplylist:
                sql4 = """
                    INSERT INTO supplier_supply(supplier_id, supply_id)
                    VALUES (%s, %s)
                """

                values3 = [supplierid, supplyid]
                db.modifydatabase(sql4, values3)
            
            if addntsupply is not None:
                sql5 = """
                    SELECT supply_id
                    FROM supply
                    WHERE supply_name = %s
                """
                getsupplyid = [addntsupply]
                col2 = ['supplyid']

                df = db.querydatafromdatabase(sql5, getsupplyid, col2)

                newsupplyid = int(df['supplyid'][0])

                sql6 = """
                    INSERT INTO supplier_supply(supplier_id, supply_id)
                    VALUES (%s, %s)
                """

                values4 = [supplierid, newsupplyid]
                db.modifydatabase(sql6, values4)
                
            return ["", False, True]
        
    else:
        raise PreventUpdate