import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,datetime,timedelta
import dash_table
from dash_table.Format import Format, Group, Scheme


from utils.server_function import *
from pages.dash_pages.model import *





cellsoh_control_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("SOH(Cell)")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dcc.Store(id='ds_cellsoh_df'             ,storage_type='memory'),
                dbc.Col(children=[dbc.Label("Period")], width=3),
                dbc.Col(children=[    
                    dcc.DatePickerRange(
                        id='date_range_cellsoh',
                        min_date_allowed=date(2019, 12, 13),
                        max_date_allowed=date.today()-timedelta(days=1),
                        initial_visible_month=date.today()-timedelta(days=30),
                        start_date=datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
                        end_date  =datetime.strptime('2021-12-31', '%Y-%m-%d').date(),
                        display_format='YYYY-MM-DD',
                        style = {'width':'100%','font-size': '10px','display': 'inline','border-spacing' : '0'} 
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_cellsoh_bank",
                       options=[
                            {"label": col, "value": col} for col in df_bank().code
                        ],
                        value="2",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Rack")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_cellsoh_rack",
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
                   dcc.Dropdown(id="cbo_cellsoh_module",
                       options=[
                            {"label": col, "value": col} for col in df_module().code
                        ],
                        value="",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Cell")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_cellsoh_cell",
                       options=[
                            {"label": col, "value": col} for col in df_cell().code
                        ],
                        value="",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Loading(id="loading_cellsoh_1", type="circle", children=html.Div(id="cellsoh_loading_output1")),
                    html.Br(),
                    dbc.Button(html.Span(["Load Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_dataload", color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={'height': '500px','padding-left': '10px', 'padding-right': '10px'},
    body=True,
)



cellsoh_control_2 = dbc.Card([
    dbc.Row([
        dbc.Label("SOH"),
        dcc.Loading(id="cellsoh_plot_2_loading", type="dot",
                    children=dcc.Graph(
                        id="cellsoh_plot_1",
                        figure={'data': [{'y': [0, 0] }],'layout': {'height': 550}}
                    )
                )
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height":"620px"},
    body=True,
)






cellsoh_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Second Page"),
            html.Div(id='div_cellsoh_model_info', style={'height':'440px', 'whiteSpace':'pre-line','border':'1px #AEAFAF solid','overflow':'auto'})
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)







content = dac.TabItem(id='content_cellsoh_pages',
                        children=html.Div([
                            dbc.Tabs([
                                #------First Tab Start --------------------------------------------------------------------------
                                dbc.Tab(label="SOH[Cell]", active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                    children=html.Div([
                                            dbc.Row([
                                                dbc.Col([ cellsoh_control_1 ],md=3,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                dbc.Col([ cellsoh_control_2 ],md=9,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                            ],),
                                        ],
                                    ),  
                                ),
                                #------First Tab End    --------------------------------------------------------------------------
                                #------Second Tab Start --------------------------------------------------------------------------
                                dbc.Tab(label='Second Page', active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                children=[
                                    dbc.Row([
                                        dbc.Col([
                                              cellsoh_control_3
                                        ],md=12, style={"height": "100%"},),
                                    ],),
                                ]),
                                #------Second Tab End   --------------------------------------------------------------------------
                            ])
                               
						] ,style={'width': '100%'} )
                            # className='flex-container'
         )                        