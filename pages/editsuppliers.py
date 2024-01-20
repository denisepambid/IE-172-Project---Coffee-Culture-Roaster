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
        
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Supplier Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", id='edit-suppname', placeholder="Enter supplier name",
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
                                type="text", id='edit-address', placeholder="Enter supplier address"
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
                                type="tel", id='edit-number', placeholder="Enter contact number"
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
                                type="email", id='edit-email', placeholder="Enter supplier email"
                            ),
                            width=10,
                        ),
                    ],
                    className="mb-3",
                ),
                
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Update", id='update-supplier', n_clicks=None, style={'background-color':"#ae7a31"}),
                            class_name='d-grid gap-2 col-6 mx-auto'
                            ),
                        dbc.Col(
                            dbc.Button("Delete", id='delete-supplier', n_clicks=None, style={'background-color':"#ae7a31"}),
                            class_name='d-grid gap-2 col-6 mx-auto')
                    ]
                )
            ]
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Edit Success')
                ),
                dbc.ModalBody("Supplier details has been updated."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/suppliers', id='edit-suppmodalbtn', className='me-1')
                )
            ],
            centered=True,
            id='edit-suppliermodal',
            backdrop='static',
            is_open=False,
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Supplier Deleted')
                ),
                dbc.ModalBody("Supplier records has been successfully deleted."),
                dbc.ModalFooter(
                    dbc.Button( "Continue", href='/suppliers', id='delete-suppmodalbtn', className='me-1')
                )
            ],
            centered=True,
            id='delete-suppliermodal',
            backdrop='static',
            is_open=False,
        )

    ]
)

#---- load current details ----#
@app.callback(
    [
        Output('edit-suppname', 'value'),
        Output('edit-address', 'value'),
        Output('edit-number', 'value'),
        Output('edit-email', 'value'),
    ],
    Input('url', 'pathname'),
    State('url', 'search')
)
def loadsupp(pathname, search):
    if pathname == '/editsuppliers':
        parsed = urlparse(search)
        supplierid = int(parse_qs(parsed.query)['id'][0])

        loadsql = """
            SELECT supplier_name, supplier_address, supplier_contactno, supplier_email
            FROM supplier
            WHERE supplier_id = %s
        """
        loadvalues = [supplierid]
        col = ['suppname', 'address', 'contactno', 'email']

        df = db.querydatafromdatabase(loadsql, loadvalues, col)

        suppname = df['suppname'][0]
        suppaddress = df['address'][0]
        suppcontactno = df['contactno'][0]
        suppemail = df['email'][0]

        return [suppname, suppaddress, suppcontactno, suppemail]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('edit-suppliermodal', 'is_open'),
    ],
    [
        Input('update-supplier', 'n_clicks'),
    ],
    [
        State('edit-suppname', 'value'),
        State('edit-address', 'value'),
        State('edit-number', 'value'),
        State('edit-email', 'value'),
        State('url', 'search'),
        State('edit-suppliermodal', 'is_open'),
    ]
)

def updatesupplier(click, suppname, suppaddress, suppnumber, suppemail, search, modalopen):
    if click is not None:
        parsed = urlparse(search)
        supplierid = parse_qs(parsed.query)['id'][0]

        updatesql = """
            UPDATE supplier
            SET
                supplier_name = %s,
                supplier_address = %s,
                supplier_contactno = %s,
                supplier_email = %s
            WHERE supplier_id = %s
        """

        updatevalues = [suppname, suppaddress, suppnumber, suppemail, supplierid]

        db.modifydatabase(updatesql, updatevalues)                

        return [True] 
        
    else:
        raise PreventUpdate
    


@app.callback(
    [
        Output('delete-suppliermodal', 'is_open'),
    ],
    [
        Input('delete-supplier', 'n_clicks'),
    ],
    [
        State('url', 'search'),
        State('delete-suppliermodal', 'is_open'),
    ]
)

def deletesupplier(delclick, search, modalopen):
    if delclick is not None:
        parsed = urlparse(search)
        supplierid = parse_qs(parsed.query)['id'][0]

        delsql = """
            UPDATE supplier
            SET is_active = %s
            WHERE supplier_id = %s
        """

        delvalues = [False, supplierid]

        db.modifydatabase(delsql, delvalues)                

        return [True] 
        
    else:
        raise PreventUpdate