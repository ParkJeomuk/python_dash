import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,timedelta
from dash import dash_table
from dash_table.Format import Format, Group, Scheme

from utils.server_function import *
 

automl_control_1 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dcc.Store(id='ds_automl_train_data' ,storage_type='memory'),
            dcc.Store(id='ds_automl_test_data'  ,storage_type='memory'),
            dbc.Button(html.Span(["Data Load", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_automl_dataload", color="dark"),
        ], width=2),
        dbc.Col(children=[
            dbc.Label("Model"),
            dcc.Dropdown(id="cbo_automl_model",options=[{"label": 'LM', "value": 'LM'}],value="LM",)
        ], width=1),
        dbc.Col(children=[
            dbc.Label("Y Var"),
            dcc.Dropdown(id="cbo_automl_y",options=[{"label": 'Y', "value": 'Y'}],value="1",)
        ], width=2),
        dbc.Col(children=[
            dbc.Label("X Var"),
            dcc.Dropdown(id="cbo_automl_x",options=[{"label": 'X', "value": 'X'}],value="1",multi=True)
        ], width=6),
        dbc.Col(children=[
            html.Br(), 
            dbc.Button(html.Span(["Calc", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_automl_model_apply", color="dark") 
        ], width=1,style={'padding-top': '7px'},),
    ],style={'height': '100%'},),
    ],style={"height": "120px"},
    body=True,
)



automl_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.Label("AutoML Model"),
            html.Div(id='div_automl_data_info', style={'height':'760px', 
                                                       'whiteSpace':'pre-line',
                                                       'border':'1px #AEAFAF solid',
                                                       'overflow':'auto', 
                                                       'padding-left':'10px',
                                                       'padding-right':'10px',
                                                       'padding-top':'10px',
                                                       'padding-bottom':'10px'})

        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height":"815px"},
)






automl_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dbc.Label("Variable Importance"),
                    dcc.Loading(id="automl_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="automl_plot_1",
                        figure={'layout': {'height': 450}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)


automl_control_4 = dbc.Card([
        dbc.Row([ 
                dbc.Col(children=[
                     dbc.Label("Variable Importance Table"),
                     html.H1(id='automl_DT_1'),                  
                ], width=12, style={'padding-top': '5px', 'padding-bottom': '5px'}, ),
        ],style={"height": "330px",'padding-left': '10px', 'padding-right': '10px'}, ),
    ],
    style={"height": "300px"},
)
 






content = dac.TabItem(id='content_automl_pages',
                        children=html.Div([
                            dbc.Row([
                                dbc.Col([
                                    automl_control_1
                                ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),
                            dbc.Row([
                                dbc.Col([
                                    automl_control_2
                                ],md=6, style={"padding-left": "10px","padding-right": "10px", },),    
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            automl_control_3
                                        ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ],),
                                    dbc.Row([    
                                        dbc.Col([
                                            automl_control_4
                                        ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ],),    
                                ],md=6, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),    
                            
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        