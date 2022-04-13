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
        dbc.Row([ dbc.Col(children=[dbc.Label("Aging Gap")], width=12), ],style={'padding-top': '5px', 'padding-bottom': '5px'}),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank", style={'padding-top':'5px'})], width=3),
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
                dbc.Col(children=[dbc.Label("Date1", style={'padding-top':'5px'})], width=3),
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
                dbc.Col(children=[dbc.Label("Date2", style={'padding-top':'5px'})], width=3),
                dbc.Col(children=[    
                    dcc.DatePickerSingle(
                            id='dtp_aging_date_2',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2021-12-29', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8, 'width':'100%'}
                        )
                ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),

        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    dcc.Store(id='ds_aging_df' ,storage_type='memory'),
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
            dbc.Label("Aging Gap", style={'padding':'5px 10px 0px 0px'})
        ],className="input-group flex-nowrap", width=2, style={'padding':'7px 0px 0px 30px'}),
        dbc.Col(children=[
            dbc.Label("Plot Type", style={'padding':'5px 10px 0px 0px'}),
            html.Div([
                   dcc.RadioItems(
                       id='rdo_aging_plottype',
                       options=[ 
                                dict(label='Heat'   ,value='H'),
                                dict(label='Cluster',value='C')
                                ], 
                       value='H' ,
                       labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'10px'}
                       )
            ],style={'height':'37px','width':'200px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
        ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Label("Data Type", style={'padding':'5px 10px 0px 0px'}),
            html.Div([
                   dcc.RadioItems(
                       id='rdo_aging_heatmaptype',
                       options=[ 
                                dict(label='Cell'  ,value='C'),
                                dict(label='Module',value='M')
                                ], 
                       value='M' ,
                       labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'10px'}
                       )
            ],style={'height':'37px','width':'150px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
        ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),


       dbc.Col(children=[
            dbc.Label("Color Type", style={'padding':'5px 10px 0px 0px'}),
            html.Div([
                   dcc.RadioItems(
                       id='rdo_aging_heatmap_color',
                       options=[ 
                                dict(label='Asc'  ,value='A'),
                                dict(label='Desc' ,value='D')
                                ], 
                       value='D' ,
                       labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'20px'}
                       )
            ],style={'height':'37px','width':'150px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
        ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),
        dbc.Col(children=[
            html.Br()
        ], width=1, style={'text-align':'right','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'},),
    ]),
    ], style={"height":"50px"},
)


aging_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="aging_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_1",
                        figure={'layout': {'height': 870}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "900px"},
)

aging_control_4 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="aging_plot_5_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_5",
                        figure={'layout': {'height': 260}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '0px', 'padding-bottom': '0px'}),
    ]),
    ],style={"height": "270px"},
)


aging_control_5 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Abnomal Outlier", style={'margin-left':'20px'})
        ],width=8,style={'text-align':'left', 'padding-top':'7px', 'padding-left':'15px'},),            
        dbc.Col(children=[
            dbc.Button(  html.I(className="fa fa-search") , id="btn_aging_outlier_data", color="dark"),
            dbc.Tooltip("Abnomal Outlier Data View!",target="btn_aging_outlier_data",),
        ], width=4,style={'text-align':'right', 'padding-top':'7px', 'padding-right':'15px'},),            
    ]),
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="aging_plot_2_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_2",
                        figure={'layout': {'height': 440}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)


aging_control_6 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Top 25", style={'margin-left':'20px'})
        ],width=8,style={'text-align':'left', 'padding-top':'7px', 'padding-left':'15px'},),            
        dbc.Col(children=[
            dbc.Button(  html.I(className="fa fa-search") , id="btn_aging_top25_data", color="dark"),
            dbc.Tooltip(" Top 25 Data View!",target="btn_aging_top25_data",),
        ], width=4,style={'text-align':'right', 'padding-top':'7px', 'padding-right':'15px'},),            
    ]),
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="aging_plot_3_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_3",
                        figure={'layout': {'height': 440}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)


aging_control_7 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Bottom 25", style={'margin-left':'20px'})
        ],width=8,style={'text-align':'left', 'padding-top':'7px', 'padding-left':'15px'},),            
        dbc.Col(children=[
            dbc.Button(  html.I(className="fa fa-search") , id="btn_aging_bottom25_data", color="dark"),
            dbc.Tooltip(" Bottom 25 Data View!",target="btn_aging_bottom25_data",),
        ], width=4,style={'text-align':'right', 'padding-top':'7px', 'padding-right':'15px'},),            
    ]),
    dbc.Row([
        dbc.Col(children=[
                    dcc.Loading(id="aging_plot_4_loading", type="dot",
                    children=dcc.Graph(
                        id="aging_plot_4",
                        figure={'layout': {'height': 440}}
                    )
                )
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)

 
#--------------------------------------------------------------------------------------------------------------------
# Top 25 Modal Popup
#--------------------------------------------------------------------------------------------------------------------
aging_top25_popup = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Top 25 Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='aging_DT_1') ,
            ]),
    ],
    id="aging_modal_1",
    className="modal-dialog modal-lg"
)

#--------------------------------------------------------------------------------------------------------------------
# Bottom 25 Modal Popup
#--------------------------------------------------------------------------------------------------------------------
aging_bottom25_popup = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Bottom 25 Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='aging_DT_2') ,
            ]),
    ],
    id="aging_modal_2",
    className="modal-dialog modal-lg"
)


#--------------------------------------------------------------------------------------------------------------------
# Abnomal Outlier Data Modal Popup
#--------------------------------------------------------------------------------------------------------------------
aging_outlier_popup = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Abnomal Outlier Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='aging_DT_3') ,
            ]),
    ],
    id="aging_modal_3",
    className="modal-dialog modal-lg"
)





content = dac.TabItem(id='content_aging_pages',
                        children=html.Div([
                            dbc.Row([
                                dbc.Col([
                                    aging_control_1
                                ],md=3, style={"padding-left": "10px","padding-right": "10px", },),    
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            aging_control_2,
                                            aging_control_3,
                                            aging_control_4
                                        ],md=12, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Store(id='ds_aging_top25'      ,storage_type='memory'),
                                            dcc.Store(id='ds_aging_bottom25'   ,storage_type='memory'),
                                            aging_top25_popup,
                                            aging_bottom25_popup,
                                            aging_outlier_popup,
                                            aging_control_5
                                        ],md=4, style={"padding-left": "10px","padding-right": "10px", },),    
                                        dbc.Col([
                                            aging_control_6
                                        ],md=4, style={"padding-left": "10px","padding-right": "10px", },),    
                                        dbc.Col([
                                            aging_control_7
                                        ],md=4, style={"padding-left": "10px","padding-right": "10px", },),    
                                    ]),
                                ],md=9, style={"padding-left": "10px","padding-right": "10px", },),    
                            ],),
                            
						] ,style={'width': '100%'} )
                            # className='flex-container'
                     )                        