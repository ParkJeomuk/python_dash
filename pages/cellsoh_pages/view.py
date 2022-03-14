from logging import PlaceHolder
import dash_bootstrap_components as dbc
from dash import dcc ,html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,datetime,timedelta
import dash_table
from dash_table.Format import Format, Group, Scheme


from utils.server_function import *
from pages.dash_pages.model import *




#--------------------------------------------------------------------------------------------------------------------
# 왼쪽 데이타 조회 조건 패널
#--------------------------------------------------------------------------------------------------------------------
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
                        multi=True
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
                        multi=True
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
                        multi=True
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


#--------------------------------------------------------------------------------------------------------------------
# 중앙 첫번째 Plot
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=html.Div([
            dbc.Label("SOH", style={'margin-left': '20px', 'padding-top':'5px'}),
        ],className="d-grid gap-2",) , width=2,),    
        dbc.Col(children=[
            dbc.Label("Y :"),
        ],className="d-grid gap-2", width=1,style={'text-align':'right','padding-top':'8px'},),
        dbc.Col(children=[
                dcc.Dropdown(
                    id="cbo_cellsoh_y",
                    options=[  {'label': 'SOH'    , 'value': 'soh'},
                               {'label': 'Q_A'    , 'value': 'q_a'},
                               {'label': 'Q_U'    , 'value': 'q_u'},
                               {'label': 'Cur Avg', 'value': 'cur_avg'},
                               {'label': 'Time'   , 'value': 'n'},
                               {'label': 'U_Vol'  , 'value': 'u_vol'},
                               {'label': 'O_Vol'  , 'value': 'o_vol'},
                               {'label': 'Gap'    , 'value': 'gap'},
                            ],
                    value="soh",),
        ],className="d-grid gap-2", width=2,style={'padding-top':'5px'},),
        # dbc.Col(children=[
        #     html.Div([
        #         html.Span("Data Count : 0")
        #     ],id='cellsoh_label_1', 
        #     style={'height':'30px','width':'200px', 'whiteSpace':'pre-line','border':'1px #AEAFAF solid','overflow':'auto', 'padding':'5px 5px 5px 5px'})
        # ],style={'text-align':'center', 'padding-top':'5px'}, width=5,),  
        dbc.Col(children=html.Div([
            dbc.Button(  html.I(className="fa fa-search") , id="btn_cellsoh_viewdata", color="dark"),
            dbc.Tooltip(" Box select Data View!",target="btn_cellsoh_viewdata",),
        ],) , width=7,style={'text-align':'right', 'padding-top':'5px', 'padding-right':'15px'},),            
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_1_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_1",
                            figure={'layout': {'height': 520}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ],),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"640px"},
)


#--------------------------------------------------------------------------------------------------------------------
# 중앙 Select Date 패널
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[dbc.Label("Veiw Type")], width=2 ,style={'text-align':'right', 'padding-left': '20px', 'padding-top':'10px'},),
        dbc.Col(children=[
            dcc.Dropdown(id="cbo_cellsoh_detail",
                options=[
                    {'label':'Rack', 'value':'R'},
                    {'label':'Module ', 'value':'M'},
                    {'label':'Cell', 'value':'C'}
                ],
                value = 'R',
            ),    
        ], width=2, style={ 'padding-top': '7px'}),

        dbc.Col(children=[dbc.Label("Rack")], width=1 ,style={'text-align':'right', 'padding-top':'10px'},),
        dbc.Col(children=[
            dcc.Dropdown(id="cbo_cellsoh_detail_rack",
                options=[
                    {"label": col, "value": col} for col in df_rack().code
                ],
                value="1",
                multi=False
            )
        ], width=1,style={'text-align':'left', 'padding-top':'7px', 'padding-left':'5px'}),
        dbc.Col(children=[dbc.Label("Module")], width=1,style={'text-align':'right', 'padding-top':'10px'},),
        dbc.Col(children=[
            dcc.Dropdown(id="cbo_cellsoh_detail_module",
                options=[
                    {"label": col, "value": col} for col in df_module().code
                ],
                value="1",
                multi=False
            )
        ], width=1, style={'text-align':'left', 'padding-top':'7px', 'padding-left':'5px'}),
        dbc.Col(children=[dbc.Label("Cell")], width=1,style={'text-align':'right', 'padding-top':'10px'},),
        dbc.Col(children=[
            dcc.Dropdown(id="cbo_cellsoh_detail_cell",
                options=[
                    {"label": col, "value": col} for col in df_cell().code
                ],
                value="1",
                multi=False
            )
        ], width=1, style={'text-align':'left', 'padding-top':'7px', 'padding-left':'5px'}),

        dbc.Col(children=[
            dbc.Button(html.Span(["Detail View", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_detailview", color="dark")
        ], width=2, style={'text-align':'right','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'}),
    ]),
    ],style={"height": "50px"},
)



#--------------------------------------------------------------------------------------------------------------------
# 중앙 Detail Plot
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_4 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_2_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_2",
                            figure={'layout': {'height': 460}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=12),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"500px"},
)


#--------------------------------------------------------------------------------------------------------------------
#  두번재 탭의 패널
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_21 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[dbc.Label("Seleted Date")], width=2 ,style={'text-align':'right', 'padding-left': '20px', 'padding-top':'10px'},),
        dbc.Col(children=[
            dcc.DatePickerSingle(
                            id='dtp_cellsoh_detail_date',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2021-12-29', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8}
                        ) 
        ], width=4, style={'text-align':'left','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'},),
        dbc.Col(children=[
            dbc.Button(html.Span(["Heatmap View", html.I(className="fas fa-arrow-alt-circle-down ml-2")]), id="btn_cellsoh_heatview", color="dark")
        ], width=6, style={'text-align':'right','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'},),
    ]),
    ], style={"height":"50px"},
)


cellsoh_control_22 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_21_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_21",
                            figure={'layout': {'height': 600}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=12),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"700px"},
)


#--------------------------------------------------------------------------------------------------------------------
#  두번재 탭의 2번째 PLOT
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_23 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_22_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_22",
                            figure={'layout': {'height': 460}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=12),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"500px"},
    body=True,
)


#--------------------------------------------------------------------------------------------------------------------
#  두번재 탭의 3번째 PLOT
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_24 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_23_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_23",
                            figure={'layout': {'height': 460}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=12),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"500px"},
    body=True,
)


#--------------------------------------------------------------------------------------------------------------------
# 첫째 패널의 박스 선택 부분의 데이타 뷰 모달 팝업
#--------------------------------------------------------------------------------------------------------------------
cellsoh_dataview_popup = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("View Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='cellsoh_DT_1') ,
            ]),
    ],
    id="cellsoh_modal_1",
    size="lg",
)






content = dac.TabItem(id='content_cellsoh_pages',
                        children=html.Div([
                            dbc.Row([

                                dbc.Col([ cellsoh_control_1 ],md=3,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                dbc.Col([ 
                                    dbc.Tabs([
                                        #------First Tab Start --------------------------------------------------------------------------
                                        dbc.Tab(label="SOH[Cell]", active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                        children=html.Div([
                                                dbc.Row([
                                                    dbc.Col([ 
                                                        cellsoh_dataview_popup,
                                                        cellsoh_control_2,
                                                        cellsoh_control_3,
                                                        cellsoh_control_4
                                                    ],md=12,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                ],),
                                            ],),  
                                        ),
                                        #------First Tab End    --------------------------------------------------------------------------
                                        #------Second Tab Start --------------------------------------------------------------------------
                                        dbc.Tab(label='Second Page', active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                        children=[
                                            dbc.Row([
                                                dbc.Col([
                                                    cellsoh_control_21 ,
                                                    cellsoh_control_22 ,
                                                    cellsoh_control_23 ,
                                                    cellsoh_control_24 
                                                ],md=12,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                            ],),
                                        ]),
                                        #------Second Tab End   --------------------------------------------------------------------------
                                    ])
                                ],md=9,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),


                            ],),



                            # dbc.Tabs([
                            #     #------First Tab Start --------------------------------------------------------------------------
                            #     dbc.Tab(label="SOH[Cell]", active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                            #         children=html.Div([
                            #                 dbc.Row([
                            #                     dbc.Col([ cellsoh_control_1 ],md=3,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                            #                     dbc.Col([ 
                            #                         cellsoh_dataview_popup,
                            #                         cellsoh_control_2,
                            #                         cellsoh_control_3,
                            #                         cellsoh_control_4
                            #                      ],md=9,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                            #                 ],),
                            #             ],
                            #         ),  
                            #     ),
                            #     #------First Tab End    --------------------------------------------------------------------------
                            #     #------Second Tab Start --------------------------------------------------------------------------
                            #     dbc.Tab(label='Second Page', active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                            #     children=[
                            #         dbc.Row([
                            #             dbc.Col([
                            #                   cellsoh_control_21 ,
                            #                   cellsoh_control_22
                            #             ],md=12, style={"height": "100%"},),
                            #         ],),
                            #     ]),
                            #     #------Second Tab End   --------------------------------------------------------------------------
                            # ])
                               
						] ,style={'width': '100%'} )
                            # className='flex-container'
         )                        