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
 

aging_control_1 = dbc.Card(
    [
        dbc.Row([ dbc.Col(children=[dbc.Label("Aging")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank")], width=3),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_aging_bank",
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
                   dcc.Dropdown(id="cbo_aging_rack",
                       options=[
                            {"label": col, "value": col} for col in df_rack().code
                        ],
                        value="1",
                        multi=True
                    )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Date1")], width=3),
                dbc.Col(children=[    
                    dcc.DatePickerSingle(
                            id='dtp_aging_date_1',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2020-01-08', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8, 'width':'100%'}
                        )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Date2")], width=3),
                dbc.Col(children=[    
                    dcc.DatePickerSingle(
                            id='dtp_aging_date_2',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2021-12-29', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8, 'margin-left':'10px'}
                        )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),

        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Store(id='ds_aging_df'             ,storage_type='memory'),
                    dcc.Loading(id="loading_aging_1", type="circle", children=html.Div(id="aging_loading_output1")),
                    html.Br(),
                    dbc.Button(html.Span(["Load Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_aging_dataload", color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={'height': '500px','padding-left': '10px', 'padding-right': '10px'},
    body=True,
)



aging_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dbc.Label("Aging Gap", style={'margin-left':'20px'}),
                    dcc.Loading(id="aging_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_1",
                        figure={'layout': {'height': 900}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "1000px"},
)



 



content = dac.TabItem(id='content_aging_pages',
                        children=html.Div([
                            dbc.Row([
                                dbc.Col([
                                    aging_control_1
                                ],md=3, style={"padding-left": "10px","padding-right": "10px", },),    
                                dbc.Col([
                                    aging_control_2
                                ],md=9, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        