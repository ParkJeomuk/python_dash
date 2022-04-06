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
                dbc.Col([    
                    html.Div(children=[
                        dcc.DatePickerRange(
                            id='date_range_cellsoh',
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
# 중앙 Select Date 패널
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_2 = dbc.Card([
    dbc.Row([
        dbc.Col(children=html.Div([
            dbc.Label("SOH", style={'margin-left': '20px', 'padding-top':'12px'}),
        ],className="d-grid gap-2",) , width=2,),    
        dbc.Col(children=[
            dbc.Label("Y :"),
        ],className="d-grid gap-2", width=1,style={'text-align':'right','padding-top':'12px'},),
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
        ],className="d-grid gap-2", width=2,style={'padding-top':'7px'},),
        dbc.Col(children=[
            html.Div([
                html.Span("Selected Date : ____-__-__")
            ],id='div_cellsoh_select_date', 
            style={'height':'40px','width':'240px', 'whiteSpace':'pre-line','border':'0px #AEAFAF solid','overflow':'auto', 'padding':'5px 5px 5px 5px'})
        ],style={'text-align':'center', 'padding-top':'7px'}, width=5,),  

        dbc.Col(children=html.Div([
            dbc.Button(  html.I(className="fa fa-search") , id="btn_cellsoh_viewdata", color="dark"),
            dbc.Tooltip(" Box select Data View!",target="btn_cellsoh_viewdata",),
        ],) , width=2,style={'text-align':'right', 'padding-top':'7px', 'padding-right':'15px'},),            
    ]),
    ],style={"height": "50px"},
)


#--------------------------------------------------------------------------------------------------------------------
# 중앙 첫번째 Plot
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_3 = dbc.Card([


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
cellsoh_control_4 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("View Type", style={'padding-top':'5px'}),
            dcc.Dropdown(id="cbo_cellsoh_detail",
                options=[
                    {'label':'Rack', 'value':'R'},
                    {'label':'Module ', 'value':'M'},
                    {'label':'Cell', 'value':'C'}
                ],
                value = 'R', 
                style={'width':'150px','margin-left':'10px'} )
        ], className="input-group flex-nowrap", width=3, style={'padding': '7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Label("Rack", style={'padding-top':'5px'}),
            dcc.Dropdown(
                id="cbo_cellsoh_detail_rack",
                options=[{"label": col, "value": col} for col in df_rack().code],
                value="1",
                multi=False,
                style={'width':'80px','margin-left':'10px'} 
            )
        ], className="input-group flex-nowrap", width=2, style={'padding': '7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Label("Module", style={'padding-top':'5px'}),
            dcc.Dropdown(id="cbo_cellsoh_detail_module",
                options=[
                    {"label": col, "value": col} for col in df_module().code
                ],
                value="1",
                multi=False,
                style={'width':'80px','margin-left':'10px'} 
            )
        ], className="input-group flex-nowrap", width=2, style={'padding': '7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Label("Cell", style={'padding-top':'5px'}),
            dcc.Dropdown(id="cbo_cellsoh_detail_cell",
                options=[
                    {"label": col, "value": col} for col in df_cell().code
                ],
                value="1",
                multi=False,
                style={'width':'100px','margin-left':'10px'} 
            )
        ],className="input-group flex-nowrap", width=2, style={'padding':'7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Button(html.Span(["Detail View", html.I(className="fas fa-arrow-alt-circle-down")]), id="btn_cellsoh_detailview", color="dark"),
            dbc.Tooltip("Detail Data View!",target="btn_cellsoh_detailview",),
        ],width=3, style={'text-align':'right', 'padding':'7px 20px 5px 5px'}),

    ])

    ],style={"height": "50px"},
)



#--------------------------------------------------------------------------------------------------------------------
# 중앙 Detail Plot
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_5 = dbc.Card([
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
    ],style={"height":"500px"},
)



#--------------------------------------------------------------------------------------------------------------------
# 하단 Predict 패널
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_6 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Predict Period", style={'padding-top':'5px'}),
            dcc.DatePickerRange(
                        id='pred_date_range_cellsoh',
                        initial_visible_month=date.today()+timedelta(days=30),
                        display_format='YYYY-MM-DD',
                        style = {'width':'300px','font-size':'10px','border-spacing':'0','margin-left':'10px'} 
                    )  
        ],className="input-group flex-nowrap", width=9, style={'padding':'7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Button(html.Span(["Predict", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_detail_predict", color="dark") ,
        ], width=2, style={'text-align':'right','padding':'7px 20px 0px 0px'}),

        dbc.Col(children=[
            dbc.Button(html.I(className="fa fa-search") , id="btn_cellsoh_detail_dataview", color="dark"),
            dbc.Tooltip(" Box select Data View!",target="btn_cellsoh_detail_dataview",),
        ], width=1, style={'text-align':'right','padding':'7px 20px 0px 0px'}),

    ]),
    ],style={"height": "50px"},
)

 



#--------------------------------------------------------------------------------------------------------------------
#  두번재 탭의 패널
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_21 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Date", style={'padding-top':'5px'}),
            dcc.DatePickerSingle(
                            id='dtp_cellsoh_detail_date',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2021-12-29', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8, 'margin-left':'10px'}
                        )   
        ],className="input-group flex-nowrap", width=3, style={'padding':'7px 0px 0px 20px'}),

        dbc.Col(children=[
            dbc.Label("Data Type", style={'padding':'5px 10px 0px 0px'}),
            html.Div([
                   dcc.RadioItems(
                       id='rdo_cellsoh_heatmaptype',
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
                       id='rdo_cellsoh_heatmap_color',
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
            dbc.Button(html.Span(["Heatmap View", html.I(className="fas fa-arrow-alt-circle-down ml-2")]), id="btn_cellsoh_heatview", color="dark")
        ], width=3, style={'text-align':'right','padding-left': '15px', 'padding-right': '15px', 'padding-top': '7px'},),
    ]),
    ], style={"height":"50px"},
)


cellsoh_control_22 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_21_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_21",
                            figure={'layout': {'height': 650}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=12),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"720px"},
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
            dbc.Label("Plot Type", style={'padding':'5px 10px 0px 0px'}),
            html.Div([
                   dcc.RadioItems(
                       id='rdo_cellsoh_tab2_plot_type',
                       options=[ 
                                dict(label='Bar'        ,value='B'),
                                dict(label='Line+Point' ,value='L')
                                ], 
                       value='B' ,
                       labelStyle = {'display': 'inline', 'cursor': 'pointer',   'padding-right':'20px'}
                       )
            ],style={'height':'37px','width':'200px', 'whiteSpace':'pre-line','border':'1px #D3D3D3 solid', 'padding':'5px 5px 5px 10px','border-radius': '5px'})  
        ],className="input-group flex-nowrap", width=4, style={'padding':'7px 0px 0px 20px'}),
        dbc.Col([
           html.Br()
        ],className="input-group flex-nowrap", width=8, style={'padding':'7px 0px 0px 20px'}),
    ]),
    dbc.Row([
        dbc.Col(children=[
            dcc.Store(id='ds_cellsoh_plot23_df' ,storage_type='memory'),
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
    style={"height":"530px"},
    body=True,
)


#--------------------------------------------------------------------------------------------------------------------
#  두번재 탭의 4,5번째 PLOT
#--------------------------------------------------------------------------------------------------------------------
cellsoh_control_25 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Stand Date", style={'padding':'5px 10px 0px 0px'}),
            dcc.DatePickerSingle(
                            id='dtp_cellsoh_stand_date',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date = datetime.strptime('2020-01-08', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 6, 'margin-left':'10px'}
                        )   
        ],className="input-group flex-nowrap", width=3,),
        dbc.Col(children=[
            dcc.Store(id='ds_cellsoh_good_df'    ,storage_type='memory'),
            dcc.Store(id='ds_cellsoh_bad_df'     ,storage_type='memory'),

            dbc.Label("Upper Cut SOH", style={'padding':'5px 10px 0px 0px'}),
            dbc.Input(type="number", min=0, max=2,   id='input_cellsoh_upper', style={'height':'36px', 'width':'80px'}),
            
            dbc.Label("Lower Cut SOH", style={'padding':'5px 10px 0px 30px'}),
            dbc.Input(type="number", min=0, max=2,   id='input_cellsoh_lower', style={'height':'36px', 'width':'80px','padding-top':'1px'}),
        ],className="input-group flex-nowrap", width=5,),
        dbc.Col(children=[
            dbc.Button(html.Span(["View Plot", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_redraw", color="dark"),
            dbc.Button(html.Span(["Good Cell 50", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_good", color="dark"),
            dbc.Button(html.Span(["Bad Cell 50", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_cellsoh_bad", color="dark")
        ],className="input-group flex-nowrap", width=4, style={'justify-content':'space-between', 'text-align':'right','padding-right': '0px', 'padding-top': '0px'},),
        
    ]),
    dbc.Row([
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_24_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_24",
                            figure={'layout': {'height': 460}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=6),        
        dbc.Col(children=[
            dcc.Loading(id="cellsoh_plot_25_loading", type="dot",
                        children=dcc.Graph(
                            id="cellsoh_plot_25",
                            figure={'layout': {'height': 460}},
                            config={'modeBarButtons': [['zoom2d','pan2d','select2d','zoomIn2d','zoomOut2d','resetScale2d','toImage']]} 
                        )
                    )
        ], width=6),        
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},),
    ],
    style={"height":"560px"},
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
    className="modal-dialog modal-lg"
)


#--------------------------------------------------------------------------------------------------------------------
# 첫째 탭의 상세 패널의 박스 선택 부분의 데이타 뷰 모달 팝업
#--------------------------------------------------------------------------------------------------------------------
cellsoh_dataview_popup2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("View Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='cellsoh_DT_2') ,
            ]),
    ],
    id="cellsoh_modal_2",
    centered=True,
    is_open=False,
    className="modal-dialog modal-lg"
)

#--------------------------------------------------------------------------------------------------------------------
# 둘째 탭의 Good 데이타 뷰 모달 팝업
#--------------------------------------------------------------------------------------------------------------------
cellsoh_dataview_popup3 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Good Cell 50 Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='cellsoh_DT_3') ,
            ]
        ),
    ],
    id="cellsoh_modal_3",
    centered=True,
    is_open=False,
    className="modal-dialog modal-lg"
)

#--------------------------------------------------------------------------------------------------------------------
# 둘째 탭의 Bad 데이타 뷰 모달 팝업
#--------------------------------------------------------------------------------------------------------------------
cellsoh_dataview_popup4 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Bad Cell 50 Data")),
        dbc.ModalBody(
            children=[
                 html.H1(id='cellsoh_DT_4') ,
            ]),
    ],
    id="cellsoh_modal_4",
    centered=True,
    is_open=False,
    className="modal-dialog modal-lg"
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
                                                        cellsoh_dataview_popup2,
                                                        cellsoh_control_2,
                                                        cellsoh_control_3,
                                                        cellsoh_control_4,
                                                        cellsoh_control_5,
                                                        cellsoh_control_6,
                                                        html.Br(),html.Br()
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
                                                    cellsoh_dataview_popup3,
                                                    cellsoh_dataview_popup4,
                                                    cellsoh_control_21 ,
                                                    cellsoh_control_22 ,
                                                    cellsoh_control_23 ,
                                                    cellsoh_control_24 ,
                                                    cellsoh_control_25
                                                    
                                                ],md=12,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                            ],),
                                        ]),
                                        #------Second Tab End   --------------------------------------------------------------------------
                                    ])
                                ],md=9,style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),


                            ],),
						] ,style={'width': '100%'} ),
                        className='flex-container'
         )                        