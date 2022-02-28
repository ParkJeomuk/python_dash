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
        # dbc.Col(children=[
        #     dbc.Label("Model"),
        #     dcc.Dropdown(id="cbo_automl_model",options=[{"label": 'LM', "value": 'LM'}],value="LM",)
        # ], width=1),
        # dbc.Col(children=[
        #     dbc.Label("Y Var"),
        #     dcc.Dropdown(id="cbo_automl_y",options=[{"label": 'Y', "value": 'Y'}],value="1",)
        # ], width=2),
        # dbc.Col(children=[
        #     dbc.Label("X Var"),
        #     dcc.Dropdown(id="cbo_automl_x",options=[{"label": 'X', "value": 'X'}],value="1",multi=True)
        # ], width=6),
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
        dbc.Label("AutoML Model"),
        dcc.Loading(id="automl_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="automl_plot_1",
                        figure={'data': [{'y': [0, 0] }],'layout': {'height': 450}}
                    )
                )
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height":"500px"},
)






# automl_control_3 = dbc.Card([
#     dbc.Row([
#         dbc.Col(children=[
#             dbc.Label("Model Summary"),
#             html.Div(id='div_automl_model_info', style={'height':'440px', 'whiteSpace':'pre-line','border':'1px #E8EBEB solid','overflow':'auto'})
#         ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
#     ]),
#     ],style={"height": "500px"},
# )




# automl_control_4 = dbc.Card([  
#     dbc.Row([
#         dbc.Col(children=[dbc.Label("Model Tuning/Save")], width=12),
#     ]),
#     dbc.Row([
#         dbc.Col(children=[dbc.Label("Parameter")], width=2),
#         dbc.Col(children=[dcc.Dropdown(id="cbo_automl_model_para",options=[{"label": 'x', "value": 'x'}],value="1",)], width=1),
#         dbc.Col(children=[dbc.Button(html.Span(["Apply", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_automl_model_tune",color="dark") ], width=2),
#         dbc.Col(children=[dbc.Label("Model Name")], width=2),
#         dbc.Col(children=[html.Div(id="automl_div_save_model_name"), ], width=3),
#         dbc.Col(children=[dbc.Button(html.Span(["Save" , html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_automl_model_save",color="dark") ], width=2),
#     ],style={'padding-left': '20px', 'padding-top': '5px', 'padding-bottom': '5px'},),
#     ],style={"height": "120px"},
#     body=True,
# )


# automl_control_5 = dbc.Card([
#     dbc.Row([
#         dbc.Label("LM Model Actually/Predict"),
#         dcc.Loading(id="automl_plot_2_loading", type="dot",
#                     children=dcc.Graph(
#                         id="automl_plot_2",
#                         figure={'data': [{'y': [0, 0] }],'layout': {'height': 450}}
#                     )
#                 )
#             ],style={'padding-top': '5px', 'padding-bottom': '5px'},
#         ),
#     ],
#     style={"height":"500px"},
# )


# automl_control_6 = dbc.Card([
#         dbc.Row([ 
#                 dbc.Col(children=[
#                      dbc.Label("Test / Predict Data"),
#                      html.H1(id='automl_DT_1'),                  
#                 ], width=12, style={'padding-top': '5px', 'padding-bottom': '5px'}, ),
#         ],style={"height": "330px",'padding-left': '10px', 'padding-right': '10px'}, ),
#     ],
#     style={"height": "500px"},
# )







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
                                ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),    
                                    # dbc.Row([
                                    #     dbc.Col([ automl_control_2 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                    #     dbc.Col([ automl_control_3 ],md=5, style={"padding-left": "10px","padding-right": "10px", }, ),
                                    # ]),
                                    # dbc.Row([
                                    #     dbc.Col([ automl_control_5 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                    #     dbc.Col([ automl_control_6 ],md=5, style={"padding-left": "10px","padding-right": "10px", }, ),
                                    # ]) ,
                                    # dbc.Row([
                                    #     dbc.Col([ automl_control_4 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                    # ]) 
                                
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        