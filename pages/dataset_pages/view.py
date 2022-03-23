import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,timedelta
import dash_table
from dash_table.Format import Format, Group, Scheme

from utils.server_function import *
from pages.dash_pages.model import *


dataset_modal_popup = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("No Data")),
            dbc.ModalBody(
                children=[
                    dbc.Label("No Data"),
                ]),
        ],
        id="dataset_alert",
        size="xl",
        fullscreen=False,
    )



dataset_DataTable_1_columns = [
    dict(id='column'   , name='column'    , type='text'), 
]


dataset_DataTable_1 = dash_table.DataTable(
                id='dataset_DT',
                columns = dataset_DataTable_1_columns,
                editable=True,
                style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                column_selectable="single",
                row_selectable="multi",
                selected_rows=[],
                style_cell_conditional=[
                    { 'if': {'column_id': 'column'  }, 'textAlign': 'left',   'width': '100%' },
                ],
                style_data_conditional=[{
                        'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
                    },
                ],
                style_header={
                    'backgroundColor': '#929494',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'height':'40px'
                },
                export_headers='display',
            )








condi_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("Data Load")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dcc.Store(id='ds_dataset_original_df'    ,storage_type='memory'),
                dcc.Store(id='ds_dataset_df'             ,storage_type='memory'),
                dcc.Store(id='ds_train_test_file'        ,storage_type='session'),
                dbc.Col(children=[dbc.Label("Period")], width={"size":3, "offset":0 }),
                dbc.Col(children=[
                    dcc.DatePickerRange(
                        id='date_range_dataset',
                        min_date_allowed=date(2019, 12, 13),
                        max_date_allowed=date.today()-timedelta(days=1),
                        initial_visible_month=date.today()-timedelta(days=30),
                        start_date=date.today()-timedelta(days=750),
                        end_date=date.today()-timedelta(days=1),
                        display_format='YYYY-MM-DD'
                    )
                ], width={"size":9, "offset":0 }),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data Type")], width=3),
                dbc.Col(children=[
                   dcc.RadioItems(
                       id='rdo_dataset_datatype',
                       options=[ 
                                dict(label='Cell'  ,value='C'),
                                dict(label='Module',value='M'),
                                dict(label='Rack'  ,value='R')
                                ], 
                       value='C' ,
                       labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'20px'}
                       )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dataset_bank",
                       options=[
                            {"label": col, "value": col} for col in df_bank().code
                        ],
                        value="1",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Rack")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dataset_rack",
                       options=[
                            {"label": col, "value": col} for col in df_rack().code
                        ],
                        value="1",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Module")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dataset_module",
                       options=[
                            {"label": col, "value": col} for col in df_module().code
                        ],
                        value="1",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Cell")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dataset_cell",
                       options=[
                            {"label": col, "value": col} for col in df_cell().code
                        ],
                        value="1",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Loading(id="loading_datset_1", type="circle", children=html.Div(id="dataset_loading_output1")),
                    html.Br(),
                    dbc.Button(html.Span(["Data Load", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_dataset_dataload",
                               color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={'height': '450px','padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)

condi_2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Extra Condition")], width=12),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Charging Dept")], width=5),
                dbc.Col(children=[
                    dbc.Label("Condition..") ,
                    html.Div(id="dataset_select_test")
                ], width=7),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "520px",'padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)



dataset_control_1 = dbc.Card(
    [
        dbc.Row(
            [
                html.Div(
                    className="w-80 center",
                    children=[
                        dcc.Loading(id='dataset_loading_1', color='gold')
                    ],
                ),
                dbc.Col(children=[dbc.Label("Data Structure")], width=7 , align="center"),
                dbc.Col(children=[
                   dbc.Button(html.Span(["Get Data Info", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_dataset_datainfo",
                               color="dark")
                    ], style={'text-align':'right',   'whiteSpace':'pre-line' })
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.Div(id='div_dataset_datainfo', style={'height':'300px', 'whiteSpace':'pre-line','border':'1px #AEAFAF solid','overflow':'scroll'})
                ], width=12)
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data Summary")], width=12),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.Div(id='div_dataset_datasummary', style={'height':'175px', 'whiteSpace':'pre-line','border':'1px #AEAFAF solid','overflow':'scroll'})
                ], width=12)            
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "600px",'padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)

dataset_control_2 = dbc.Card(
    [
        dbc.Row([
                dbc.Col(children=[dbc.Label("Data Column Choice")
                ], width=8,style={'text-align':'left','padding-top': '12px', 'padding-bottom': '5px','padding-left': '20px'}),
                dbc.Col(children=[
                   dbc.Button(html.Span(["Set Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_dataset_set_data",
                               color="dark")
                ], width=4 ,style={'text-align':'right','padding-top': '5px', 'padding-bottom': '5px'}),
        ]),
        dbc.Row([
                dbc.Col(children=[
                    dataset_DataTable_1
                ], width=12,style={'padding-top': '5px', 'padding-bottom': '5px'},),
                
        ]),
    ],
    style={"height": "370px",'padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)

dataset_control_3 = dbc.Card(
    [  
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data View")], width=4),
                dbc.Col(children=[
                   html.Div([
                    dcc.RadioItems(
                        id='rdo_dataset_dataview',
                        options=[ 
                                    dict(label='Head'   ,value='H'),
                                    dict(label='Tail'   ,value='T'),
                                    dict(label='Custom' ,value='C')
                                    ], 
                        value='H' ,
                        labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'20px'}
                        )
                ],style={'height':'37px','width':'250px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})         
                ], width=8 , style={'text-align':'right' }),
            ],style={'padding-left': '20px', 'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.H1(id='dataset_DT_2')
                ], width=12, style={'padding-left': '20px', 'padding-right': '20px'}),
                
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "600px",'padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)

dataset_control_4 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Train/Test Data Set")], width=6),
                dbc.Col(children=[
                   dbc.Button(html.Span(["Data Split", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_dataset_split_data",
                               color="dark")
                ], width=3, style={'text-align':'right'}),
                dbc.Col(children=[
                   dbc.Button(html.Span(["Data View", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_dataset_data_view",
                               color="dark")
                ], width=3, style={'text-align':'right'}),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    dbc.Label("Train Data"),
                    html.H1(id='dataset_DT_Train')
                ], width=6),
                dbc.Col(children=[
                    dbc.Label("Test Data"),
                    html.H1(id='dataset_DT_Test')
                ], width=6),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "370px",'padding-left': '10px', 'padding-right': '10px'},
    # body=True,
)

dataset_dataview = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Train/Test Data")),
        dbc.ModalBody(
            children=[
                dbc.Label("Train Data"),
                 html.H1(id='dataset_DT_3') ,
                 html.Br(),
                 dbc.Label("Test Data"),
                 html.H1(id='dataset_DT_4')
            ]),
    ],
    id="dataset_modal_data",
    # size="xl",
    fullscreen=True,
)


content = dac.TabItem(id='content_dataset_pages',
                        children=html.Div([
 
                                            dbc.Row(
                                                    [
                                                        dataset_modal_popup,
                                                        dataset_dataview, 
                                                        dbc.Col([ 
                                                            dbc.Row([
                                                                 dbc.Col([ condi_1 ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ]),
                                                            dbc.Row([
                                                               dbc.Col([ condi_2 ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ]) ],
                                                            md=3, 
                                                        ),
                                                        dbc.Col([
                                                            dbc.Row([
                                                               dbc.Col([ dataset_control_1 ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ]),
                                                            dbc.Row([
                                                               dbc.Col([ dataset_control_2 ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ]) ],
                                                            md=4, 
                                                        ),
                                                        dbc.Col([
                                                            
                                                            dbc.Row([
                                                               dbc.Col([
                                                                   dataset_control_3 
                                                               ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ]),
                                                            dbc.Row([
                                                               dbc.Col([ dataset_control_4 ], md=12, style={"padding-left": "10px","padding-right": "10px"},),
                                                            ])  ],
                                                            md=5, 
                                                        ),
                                                    ],
                                            ),
                                        ], 
                                        className='row'
                                    )
                    )
                        