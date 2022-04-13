import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,timedelta, datetime
from dash import dash_table
from dash_table.Format import Format, Group, Scheme

from utils.server_function import *
 

trend_control_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("Aging Trend")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_trend_bank",
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
                dbc.Col(children=[dbc.Label("Date1", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[    
                    html.Div(children=[
                        dcc.DatePickerRange(
                            id='date_range_trend',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today()-timedelta(days=1),
                            initial_visible_month=date.today()-timedelta(days=30),
                            start_date=datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
                            end_date  =datetime.strptime('2021-12-31', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD',
                            className='date-range-picker'
                        )
                    ],style={'width': '100%'}),
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
       
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Store(id='ds_trend_df' ,storage_type='memory'),
                    dcc.Store(id='ds_trend_data' ,storage_type='memory'),
                    dcc.Loading(id="loading_trend_1", type="circle", children=html.Div(id="trend_loading_output1")),
                    html.Br(),
                    dbc.Button(html.Span(["Load Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_trend_dataload", color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={'height': '380px','padding-left': '10px', 'padding-right': '10px'},
    body=True,
)



# trend_control_2 = dbc.Card([
#      dbc.Row([
#         dbc.Col(children=[
#             dbc.Label("Aging Gap", style={'padding':'5px 10px 0px 0px'})
#         ],className="input-group flex-nowrap", width=2, style={'padding':'7px 0px 0px 30px'}),
#         dbc.Col(children=[
#             dbc.Label("Plot Type", style={'padding':'5px 10px 0px 0px'}),
#             html.Div([
#                    dcc.RadioItems(
#                        id='rdo_trend_plottype',
#                        options=[ 
#                                 dict(label='Heat'   ,value='H'),
#                                 dict(label='Cluster',value='C')
#                                 ], 
#                        value='H' ,
#                        labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'10px'}
#                        )
#             ],style={'height':'37px','width':'200px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
#         ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),

#         dbc.Col(children=[
#             dbc.Label("Data Type", style={'padding':'5px 10px 0px 0px'}),
#             html.Div([
#                    dcc.RadioItems(
#                        id='rdo_trend_heatmaptype',
#                        options=[ 
#                                 dict(label='Cell'  ,value='C'),
#                                 dict(label='Module',value='M')
#                                 ], 
#                        value='M' ,
#                        labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'10px'}
#                        )
#             ],style={'height':'37px','width':'150px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
#         ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),


#        dbc.Col(children=[
#             dbc.Label("Color Type", style={'padding':'5px 10px 0px 0px'}),
#             html.Div([
#                    dcc.RadioItems(
#                        id='rdo_trend_heatmap_color',
#                        options=[ 
#                                 dict(label='Asc'  ,value='A'),
#                                 dict(label='Desc' ,value='D')
#                                 ], 
#                        value='D' ,
#                        labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'20px'}
#                        )
#             ],style={'height':'37px','width':'150px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
#         ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),
#         dbc.Col(children=[
#             html.Br()
#         ], width=1, style={'text-align':'right','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'},),
#     ]),
#     ], style={"height":"50px"},
# )


trend_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="trend_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="trend_plot_1",
                        figure={'layout': {'height': 480}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "500px"},
)

trend_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="trend_plot_2_loading", type="dot",
                    children=dcc.Graph(
                        id="trend_plot_2",
                        figure={'layout': {'height': 480}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "500px"},
)

 
trend_control_4 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            html.Div([
                html.Span("Dendrograme  Date : ____-__-__")
            ],id='div_trend_select_date', 
            style={'height':'40px','width':'280px', 'whiteSpace':'pre-line','border':'0px #AEAFAF solid','overflow':'auto', 'padding':'5px 5px 5px 20px'})
        ],style={'text-align':'left', 'padding-top':'7px'}, width=5,),  
        dbc.Col([
           html.Br()
        ],className="input-group flex-nowrap", width=7, style={'padding':'7px 0px 0px 20px'}),
    ]),
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="trend_plot_3_loading", type="dot",
                    children=dcc.Graph(
                        id="trend_plot_3",
                        figure={'layout': {'height': 480}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "550px"},
)





content = dac.TabItem(id='content_trend_pages',
                        children=html.Div([
                            dbc.Row([
                                dbc.Col([
                                    trend_control_1
                                ],md=3, style={"padding-left": "10px","padding-right": "10px", },),    
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            trend_control_2 ,
                                            trend_control_3 ,
                                            trend_control_4 
                                        ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ]),
                                    
                                ],md=9, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        