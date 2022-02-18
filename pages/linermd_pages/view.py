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





linerdm_condi_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("Data Load")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Store(id='ds_linerdm_train_data' ,storage_type='memory'),
                    dcc.Store(id='ds_linerdm_test_data'  ,storage_type='memory'),
                    dcc.Loading(id="loading_linerdm_1", type="circle", children=html.Div(id="linerdm_loading_output1")),
                    dbc.Button(html.Span(["Data Load", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_linerdm_dataload",
                               color="dark"),
                    html.Br()           
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ), 
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("X Var")], width=4),
                dbc.Col(children=[dcc.Dropdown(id="cbo_linerdm_x",options=[{"label": 'X', "value": 'X'}],value="1",multi=True)], width=8),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Y Var")], width=4),
                dbc.Col(children=[dcc.Dropdown(id="cbo_linerdm_y",options=[{"label": 'Y', "value": 'Y'}],value="1",)], width=8),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Loading(id="loading_linerdm_2", type="circle", children=html.Div(id="linerdm_loading_output2")),
                    html.Br(),
                    dbc.Button(html.Span(["Data Apply", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="btn_linerdm_apply",
                               color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height": "350px"},
    body=True,
)

linerdm_condi_2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data Information")], width=12),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.Div(id='div_linerdm_datainfo', style={'height':'440px', 'whiteSpace':'pre-line','border':'0px black solid','overflow':'auto'})
                ], width=12)
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "520px"},
    body=True,
)



linerdm_control_1 = dbc.Card([
    dbc.Row([
        dcc.Loading(id="linerdm_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="linerdm_plot_1",
                        figure={'data': [{'y': [0, 0] }],'layout': {'height': 580}}
                    )
                )
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height":"600px"},
)




linerdm_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[dbc.Label("Data View / Remove")], width=6),
        dbc.Col(children=[ dbc.Button(html.Span(["Data View", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_dataview",color="dark") ], width=2),
        dbc.Col(children=[ dbc.Button(html.Span(["Remove"   , html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_remove"  ,color="dark") ], width=2),
        dbc.Col(children=[ dbc.Button(html.Span(["Reset"    , html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_reset"   ,color="dark") ], width=2),
    ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
    ],style={"height": "90px"},
    body=True,
)

linerdm_control_3 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[dbc.Label("Model Choice")], width=12),
    ]),
    dbc.Row([
        dbc.Col(children=[dbc.Label("Model")], width=4),
        dbc.Col(children=[dcc.Dropdown(id="cbo_linerdm_model",options=[{"label": 'LM', "value": 'LM'}],value="1",)], width=5),
        dbc.Col(children=[dbc.Button(html.Span(["Apply", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_model_apply",color="dark") ], width=3),
    ],style={'padding-left': '20px', 'padding-top': '5px', 'padding-bottom': '5px'},),
    ],style={"height": "120px"},
    body=True,
)


linerdm_control_4 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[dbc.Label("Model Tuning/Save")], width=12),
    ]),
    dbc.Row([
        dbc.Col(children=[dbc.Label("Parameter")], width=3),
        dbc.Col(children=[dcc.Dropdown(id="cbo_linerdm_model_para",options=[{"label": 'x', "value": 'x'}],value="1",)], width=3),
        dbc.Col(children=[dbc.Button(html.Span(["Apply", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_model_tune",color="dark") ], width=3),
        dbc.Col(children=[dbc.Button(html.Span(["Save" , html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_model_save",color="dark") ], width=3),
    ],style={'padding-left': '20px', 'padding-top': '5px', 'padding-bottom': '5px'},),
    ],style={"height": "120px"},
    body=True,
)






content = dac.TabItem(id='content_linermd_pages',
                        children=html.Div([
						    dbc.Row([
                                #-----------dbc.Col1 Start ---------------------------------------------
                                dbc.Col([ 
                                    dbc.Row([
                                        linerdm_condi_1
                                    ]),
                                    dbc.Row([
                                        linerdm_condi_2
                                    ])  
                                ],md=3, style={"height": "100%"},),
                                #-----------dbc.Col1 End -----------------------------------------------

                                #-----------dbc.Col2 Start ---------------------------------------------
                                dbc.Col([
                                    dbc.Tabs([
                                        #------First Tab Start --------------------------------------------------------------------------
                                        dbc.Tab(label="Modeling", active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                            children=html.Div([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dbc.Row([
                                                                dbc.Col([ linerdm_control_1 ],md=12, style={"padding-left": "10px","padding-right": "10px", },),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col([ linerdm_control_2 ],md=12, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                            ]),
                                                            dbc.Row([
                                                                dbc.Col([ linerdm_control_3 , ],md=6, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                                dbc.Col([ linerdm_control_4 , ],md=6, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                            ]) 
                                                        ],md=12, style={"height": "100%"},),
                                                    ],),
                                                ],
                                            ),  
                                        ),
                                        #------First Tab End    --------------------------------------------------------------------------
                                        #------Second Tab Start --------------------------------------------------------------------------
                                        dbc.Tab(label='Prediction', active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                        children=[
                                            html.Br() 
                                            ]),
                                        #------Second Tab End   --------------------------------------------------------------------------
                                    ])
                                ], md=9, style={"height": "100%", "padding-left":"10px"},),
                                #-----------dbc.Col2 End ---------------------------------------------
                            ]) ,
						] ,style={'width': '100%'}
                            # className='flex-container'
                        )
         )                        