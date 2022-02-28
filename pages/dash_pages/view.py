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
from pages.dash_pages.model import *


dataTable_column = pd.DataFrame(columns = ['Date','Bank','WeekDay','Voltage','Current','ChargeQ','DataCount','DataFail','UseYN','UseDesc']) 
# pd.DataFrame({
#     'Date'      : [''],
#     'Bank'      : [''],
#     'WeekDay'   : [''],
#     'Voltage'   : [''],
#     'Current'   : [''],
#     'ChargeQ'   : [''],
#     'DataCount' : [''],
#     'DataFail'  : [''],
#     'UseYN'     : [''],
#     'UseDesc'   : ['']
# })

condi_1 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank")], width={"size":5, "offset":0 }),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dash_bank",
                        options=[
                            {"label": col, "value": col} for col in df_bank().code
                        ],
                        value="1",
                    )
                ], width={"size":7, "offset":0 }),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data Type")], width=5),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dash_data_type",
                        options=[
                            {"label": item, "value": item} for item in df_data_type().name
                        ],
                        value="Comparison",
                    )
                ], width=7),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    # dbc.Label("Stand Date"),
                    dbc.Label(id="lbl_date1"),
                    html.Br(),
                    dcc.DatePickerSingle(
                            id='dtp_dash_stand',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            # date=date.today()-timedelta(days=1),
                            date = datetime.strptime('2022-01-05', '%Y-%m-%d').date(),
                            display_format='YYYY-MM-DD' ,
                            style={"font-size": 8}
                        ) 
                ],style={"padding-right": "5px"}, width=6),
                dbc.Col(children=[
                    dbc.Label(id="lbl_date2"),
                    html.Br(),
                    dcc.DatePickerSingle(
                            id='dtp_dash_compare',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date=datetime.strptime('2022-01-06', '%Y-%m-%d').date(), #date.today()-timedelta(days=1),
                            display_format='YYYY-MM-DD',
                            style={ "font-size": 8}
                    )
                ],style={"align":"right", "padding-left": "5px"}, width=6),
            ], style={'width':'100%','padding-top': '5px', 'padding-bottom': '5px'}, 
            
        ),
        dbc.Row(
            [
                dbc.Col(children=html.Div([
                    html.Br(),
                    dbc.Button(html.Span(["Load", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                               id="dash_btn_load",
                               color="dark")
                ],className="d-grid gap-2",) , width=12,),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height": "280px"},
    body=True,
)

condi_2 = dbc.Card(
    [
        dbc.Row(
            [
                dcc.Loading(id="dash_plot_5_loading", type="default",
                    children=dcc.Graph(
                        id="dash_plot_5",
                        figure={
                            'data': [{'y': [0, 0] }],
                            'layout': {'height': 230}
                        })
                )
            ]
        ),
    ],
    style={"height": "280px"},
    body=True,
)



condi_3 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                 dbc.Col(
                    html.H4(id='dash_box_voltage',
                        children=dac.ValueBox( value= "0 V",
                                                subtitle="Voltage [0%]" ,
                                                color = "primary",
                                                icon = "chart-line",
                                                width=12)
                    ),
                 md=4),
                 dbc.Col(
                    html.H4(id='dash_box_cq',
                        children=dac.ValueBox(  value = "0 Ah",
                                                subtitle = "Charge Q [0%]" ,
                                                color = "info",
                                                icon = "charging-station",
                                                width=12)
                    ),
                 md=4),
                 dbc.Col(
                    html.H4(id='dash_box_datacount',
                        children=dac.ValueBox(  value = "0",
                                                subtitle = "Data Count [0%]" ,
                                                color = "warning",
                                                icon = "database",
                                                width=12)
                    ),
                 md=4),
            ]),     
            dbc.Row(
            [
                 
                 dbc.Col(
                    html.H4(id='dash_box_current_c',
                        children=dac.ValueBox(  value =  "0 A",
                                                subtitle = "Current(C) [0%]" ,
                                                color = "success",
                                                icon = "wave-square",
                                                width=12
                                            )
                    ),
                 md=4),
                 dbc.Col(
                    html.H4(id='dash_box_current_d',
                        children=dac.ValueBox(  value =  "0 A",
                                                subtitle = "Current(D) [0%]" ,
                                                color = "secondary",
                                                icon = "wave-square",
                                                width=12
                                            )
                    ), 
                 md=4),                
                 dbc.Col(
                    html.H4(id='dash_box_fail',
                        children=dac.ValueBox(  value= "0",
                                                subtitle= "Data Fail [0%]" ,
                                                color = "danger",
                                                icon = "frown",
                                                width=12
                                            )
                    ),
                 md=4),
                   
            ]),
    ],
    style={"height": "280px"},
    body=True,
)

dash_control_1 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                
                dbc.Label("Voltage by Rack"),
                dcc.Loading(id="dash_plot_1_loading", type="cube",
                    children=dcc.Graph(
                        id="dash_plot_1",
                        figure={'layout': {'height': 400}}
                    )
                )
            ]
        ),
    ],
    style={"height": "460px"},
    body=True,
)




dash_control_2 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Current by Rack"),
                dcc.Loading(id="dash_plot_2_loading", type="default",
                    children=dcc.Graph(
                        id="dash_plot_2",
                        figure={
                            'data': [{'y': [0, 0] }],
                            'layout': {'height': 400}
                        })
                )
            ]
        ),
    ],
    style={"height": "460px"},
    body=True,
)

dash_control_3 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Temperature by Rack"),
                dcc.Loading(id="dash_plot_3_loading", type="dot",
                    children=dcc.Graph(
                        id="dash_plot_3",
                        figure={
                            'data': [{'y': [0, 0] }],
                            'layout': {'height': 400}
                        })
                )
            ]
        ),
    ],
    style={"height": "460px"},
    body=True,
)

dash_control_4 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Charge/Discharge Q by Rack"),
                dcc.Loading(id="dash_plot_4_loading", type="circle",
                    children=dcc.Graph(
                        id="dash_plot_4",
                        figure={
                            'data': [{'y': [0, 0] }],
                            'layout': {'height': 400}
                        })
                )
            ]
        ),
    ],
    style={"height": "460px"},
    body=True,
)



dash_plot_selection_dataview = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Train/Test Data")),
        dbc.ModalBody(
            children=[
                dbc.Label("Selected Data"),
                 html.H1(id='dash_selection_DT') 
            ]),
    ],
    id="dash_modal_selection_data",
    size="xl",
    fullscreen=False,
)


dash_DataTable_1_columns = [
    dict(id='Date'     , name='Date'      , type='text'), 
    dict(id='Bank'     , name='Bank'      , type='text'), 
    dict(id='WeekDay'  , name='WeekDay'   , type='text'), 
    dict(id='Voltage'  , name='Voltage'   , type='numeric', format=Format(precision=2, scheme=Scheme.fixed).group(True)), 
    dict(id='Current'  , name='Current'   , type='numeric', format=Format(precision=2, scheme=Scheme.fixed).group(True)), 
    dict(id='ChargeQ'  , name='Charge Q'  , type='numeric', format=Format(precision=2, scheme=Scheme.fixed).group(True)), 
    dict(id='DataFail' , name='Data Fail' , type='numeric', format=Format(precision=0, scheme=Scheme.fixed).group(True)), 
    dict(id='DataCount', name='Data Count', type='numeric', format=Format(precision=0, scheme=Scheme.fixed).group(True)), 
    dict(id='UseYN'    , name='Use Y/N'   , type='text'), 
    dict(id='UseDesc'  , name='Use Desc.' , type='text'), 
]


dash_DataTable_1 = dash_table.DataTable(
                id='dash_DT',
                
                columns = dash_DataTable_1_columns,
                
                style_table={'height': '800px', 'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                
                sort_action='custom',
                sort_mode='multi',
                sort_by=[],
                
                page_action='native',
                page_current=0,
                page_size=25,
                
                # fixed_columns={'headers': True, 'data': 1}, 
                # style_as_list_view=True,
                
                
                style_cell_conditional=[
                    { 'if': {'column_id': 'Date'     }, 'textAlign': 'center', 'width': '7%' },
                    { 'if': {'column_id': 'Bank'     }, 'textAlign': 'center', 'width': '5%' },
                    { 'if': {'column_id': 'WeekDay'  }, 'textAlign': 'center', 'width': '7%' },
                    { 'if': {'column_id': 'Voltage'  }, 'textAlign': 'right' , 'width': '10%' },
                    { 'if': {'column_id': 'Current'  }, 'textAlign': 'right' , 'width': '10%' },
                    { 'if': {'column_id': 'ChargeQ'  }, 'textAlign': 'right' , 'width': '10%' },
                    { 'if': {'column_id': 'DataFail' }, 'textAlign': 'right' , 'width': '10%' },
                    { 'if': {'column_id': 'DataCount'}, 'textAlign': 'right' , 'width': '10%' },
                    { 'if': {'column_id': 'UseYN'    }, 'textAlign': 'center', 'width': '6%' },
                    { 'if': {'column_id': 'UseDesc'  }, 'textAlign': 'left'  , 'width': '25%' },
                ],
                # style_data_conditional=[
                #     {
                #         'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
                #         # data_bars(dataTable_column, 'ChargeQ')  +
                #         # data_bars(dataTable_column, 'Voltage'),
                #     },
                # ],
                style_header={
                    'backgroundColor': '#626464',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'height':'40px'
                },
                # export_format='xlsx',
                # export_headers='display',
            )




content = dac.TabItem(id='content_dash_pages',
                        children=html.Div([
                            dbc.Tabs([
                                dbc.Tab(label="Validation Raw Data",
                                        active_label_class_name="fw-bold",
                                        tab_class_name="flex-grow-1 text-center",
                                    children=html.Div(
                                        [
                                            dcc.Store(id='ds_dash_df',storage_type='memory'),
                                            dcc.Store(id='ds_dash_compare_df',storage_type='memory'),
                                            dcc.Store(id='ds_dash_box_data',storage_type='memory'),
                                            dbc.Row([html.Br(),]),
                                            dbc.Row(
                                                    [
                                                        dbc.Col(condi_1, md=3, style={"height": "100%"},),
                                                        dbc.Col(condi_2, md=3, style={"height": "100%"},),
                                                        dbc.Col(condi_3, md=6, style={"height": "100%"},),
                                                    ],
                                                    align="center",
                                                    style={"height": "290"},
                                            ),
                                            dbc.Row(
                                                    [
                                                        dbc.Col(dash_control_1, md=6),
                                                        dbc.Col(dash_control_2, md=6),
                                                    ],
                                                    align="center",
                                            ),
                                            dbc.Row(
                                                    [
                                                        dbc.Col(dash_control_3, md=6),
                                                        dbc.Col(dash_control_4, md=6),
                                                    ],
                                                    align="center",
                                            ),
                                        ], 
                                        className='row'
                                    )
                                ),
                                dbc.Tab(label='Validation Calendar', 
                                        active_label_class_name="fw-bold",
                                        tab_class_name="flex-grow-1 text-center",
                                children=[
                                    html.Br(),
                                    html.Div(children=[
                                        dcc.DatePickerRange(
                                            id='dash_tab2_date_range',
                                            min_date_allowed=date(2019, 12, 13),
                                            max_date_allowed=date.today()-timedelta(days=1),
                                            initial_visible_month=date.today()-timedelta(days=30),
                                            start_date=datetime.strptime('2020-01-05', '%Y-%m-%d').date(),
                                            end_date=date.today()-timedelta(days=1),
                                            display_format='YYYY-MM-DD'
                                        ),
                                        dbc.Button(html.Span(["Load Data", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),
                                                   id="dash_btn_load_check_data",
                                                   color="dark",
                                                   style={"margin-left":"15px"})
                                     ]),
                                     html.Br(),
                                     html.Div(children=[    
                                        dcc.Store(id='dash_store_data_table',storage_type='memory'),
                                        dcc.Loading(id="dash_DT_1_loading", type="default",
                                        children=[dash_DataTable_1],
                                        )
                                        ])
                                    ])
                                ,

                            ])
                        ],
                        style={'width': '100%'}
                            # className='flex-container'
                        )
                        )