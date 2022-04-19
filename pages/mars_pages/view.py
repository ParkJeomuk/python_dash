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
 

mars_control_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("Aging Speed")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Date1", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[    
                    html.Div(children=[
                        dcc.DatePickerRange(
                            id='date_range_mars',
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
                dbc.Col(children=[dbc.Label("Bank", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_mars_bank",
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
                dbc.Col(children=[dbc.Label("Rack", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_mars_rack",
                       options=[
                            {"label": col, "value": col} for col in df_rack().code
                        ],
                        value="2",
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Store(id='ds_mars_df' ,storage_type='memory'),
                    dcc.Store(id='ds_mars_pie' ,storage_type='memory'),
                    dcc.Loading(id="loading_mars_1", type="circle", children=html.Div(id="mars_loading_output1")),
                    html.Br(),
                    dbc.Button(html.Span(["Load Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_mars_dataload", color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={'height': '380px','padding-left': '10px', 'padding-right': '10px'},
    body=True,
)


 

mars_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="mars_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="mars_plot_1",
                        figure={'layout': {'height': 680}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "700px"},
)

mars_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="mars_plot_2_loading", type="dot",
                    children=dcc.Graph(
                        id="mars_plot_2",
                        figure={'layout': {'height': 580}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
        # dbc.Col(children=[
        #             dcc.Loading(id="mars_plot_3_loading", type="dot",
        #             children=dcc.Graph(
        #                 id="mars_plot_3",
        #                 figure={'layout': {'height': 280}}
        #             )
        #         )
        # ], width=4, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
        # dbc.Col(children=[
        #             dcc.Loading(id="mars_plot_4_loading", type="dot",
        #             children=dcc.Graph(
        #                 id="mars_plot_4",
        #                 figure={'layout': {'height': 280}}
        #             )
        #         )
        # ], width=4, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),                
    ]),
    # dbc.Row([
    #     dbc.Col(children=[
    #                 dcc.Loading(id="mars_plot_5_loading", type="dot",
    #                 children=dcc.Graph(
    #                     id="mars_plot_5",
    #                     figure={'layout': {'height': 280}}
    #                 )
    #             )
    #     ], width=4, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    #     dbc.Col(children=[
    #                 dcc.Loading(id="mars_plot_6_loading", type="dot",
    #                 children=dcc.Graph(
    #                     id="mars_plot_6",
    #                     figure={'layout': {'height': 280}}
    #                 )
    #             )
    #     ], width=4, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    #     dbc.Col(children=[
    #                 html.Br()
    #     ], width=4, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),                
    # ]),
    ],style={"height": "600px"},
)

  


content = dac.TabItem(id='content_mars_pages',
                        children=html.Div([
                            dbc.Row([
                                dbc.Col([
                                    mars_control_1
                                ],md=3, style={"padding-left": "10px","padding-right": "10px", },),    
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            mars_control_2 ,
                                            mars_control_3  
                                        ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ]),
                                    
                                ],md=9, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        