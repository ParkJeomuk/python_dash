import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html 
import dash_admin_components as dac
from components.table import make_dash_table
from pages.dash_pages.model import df_bank, df_data_type
import pandas as pd
from datetime import date,timedelta
import dash_table


dataTable_column = pd.DataFrame({
    'Date'      : [''],
    'Bank'      : [''],
    'WeekDay'   : [''],
    'Voltage'   : [''],
    'Current'   : [''],
    'DataCount' : [''],
    'DataFail'  : [''],
    'UseYN'     : [''],
    'UseDesc'   : ['']
})

condi_1 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Bank")], width=5),
                dbc.Col(children=[
                   dcc.Dropdown(id="cbo_dash_bank",
                        options=[
                            {"label": col, "value": col} for col in df_bank().code
                        ],
                        value="1",
                    )
                ], width=7),
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
                    dbc.Label("Stand Date"),
                    dcc.DatePickerSingle(
                            id='dtp_dash_stand',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date=date.today()-timedelta(days=1),
                            display_format='YYYY-MM-DD' 
                        ) 
                ],style={'width':'100%'}, width=6),
                dbc.Col(children=[
                    dbc.Label("Compare Date"),
                    dcc.DatePickerSingle(
                            id='dtp_dash_compare',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date=date.today()-timedelta(days=1),
                            display_format='YYYY-MM-DD'
                    )
                ], width=6)
            ],style={'width':'100%','padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    dbc.Button("Load", id="dash_btn_load",color="dark")
                ], width=12,className="d-grid gap-2",),
                # dbc.Col(children=[
                #     html.Div(children=[
                #         html.Label('Plot Type', style={"padding-left":"10px", "padding-right":"10px"}),
                #         dcc.RadioItems(id='dash_rdo_plot_type',
                #                 options=[
                #                     {'label': 'Line','value': 'L'},
                #                     {'label': 'Point','value': 'P'},
                #                     {'label': 'Line+Point','value': 'LP'}
                #                 ],
                #                 value='L',
                #                 labelStyle={'display': 'inline-block'}
                #             ),
                #     ],style={'display': 'flex'}),
                # ], width=9),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
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
                            'layout': {'height': 200}
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
                html.Div([
                    dac.ValueBox(
                        id="dash_box_voltage",
                        value=150,
                        subtitle="New orders",
                        color = "primary",
                        icon = "shopping-cart",
                        href = "#" ,
                        width=4
                    ),
                    dac.ValueBox(
                        id="dash_box_cq",
                        value = "53%",
                        subtitle = "New orders",
                        color = "danger",
                        icon = "cogs",
                        width=4
                    ),
                    dac.ValueBox(
                        id="dash_box_datacount",
                        value = "44",
                        subtitle = "User Registrations",
                        color = "warning",
                        icon = "suitcase",
                        width=4
                    )
                ], className='row'),
                html.Div([
                    dac.ValueBox(
                        id="dash_box_fail",
                        value=150,
                        subtitle="New orders",
                        color = "primary",
                        icon = "shopping-cart",
                        href = "#" ,
                        width=4
                    ),
                    dac.ValueBox(
                        id="dash_box_current_c",
                        value = "53%",
                        subtitle = "New orders",
                        color = "danger",
                        icon = "cogs",
                        width=4
                    ),
                    dac.ValueBox(
                        id="dash_box_current_d",
                        value = "44",
                        subtitle = "User Registrations",
                        color = "warning",
                        icon = "suitcase",
                        width=4
                    )
                ], className='row'),
            ]
        ),
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
                dcc.Loading(id="dash_plot_1_loading", type="default",
                    children=dcc.Graph(id="dash_plot_1")
                )
            ]
        ),
    ],
    body=True,
)

dash_control_2 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Current by Rack"),
                dcc.Loading(id="dash_plot_2_loading", type="default",
                    children=dcc.Graph(id="dash_plot_2")
                )
            ]
        ),
    ],
    body=True,
)

dash_control_3 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Temperature by Rack"),
                dcc.Loading(id="dash_plot_3_loading", type="default",
                    children=dcc.Graph(id="dash_plot_3")
                )
            ]
        ),
    ],
    body=True,
)

dash_control_4 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Charge/Discharge Q by Rack"),
                dcc.Loading(id="dash_plot_4_loading", type="default",
                    children=dcc.Graph(id="dash_plot_4")
                )
            ]
        ),
    ],
    body=True,
)


# dash_DT = dash_table.DataTable(
#     id='dash_dt',
#     columns=[{"name": i, "id": i}  for i in dataTable_column.columns],
#     data = dataTable_column,
#     style_as_list_view=True,
#     style_cell={'padding': '2px'},
#     style_table={'height': '600px', 'overflowY': 'auto'},
#     style_cell_conditional=[
#         { 'if': {'column_id': 'date'   }, 'textAlign': 'center' },
#         { 'if': {'column_id': 'voltage'}, 'textAlign': 'right'  },
#         { 'if': {'column_id': 'current'}, 'textAlign': 'right'  },
#         { 'if': {'column_id': 'cq'     }, 'textAlign': 'right'  },
#     ],
#     style_data_conditional=[
#         {
#             'if': {'row_index': 0},
#             'backgroundColor': '#FFF2CC',
#         },
#     ],
#     style_header={
#         'backgroundColor': 'white',
#         'fontWeight': 'bold',
#         'textAlign': 'center'
#     },
# )




content = dac.TabItem(id='content_dash_pages',
                        children=html.Div([
                            dcc.Tabs([
                                dcc.Tab(label='Validation Raw Data ',  
                                    children=html.Div(
                                        [
                                            dcc.Store(id='dash_store_df',storage_type='session'),
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
                             
                                dcc.Tab(label='Validation Calendar', children=[
                                    html.Br(),
                                    html.Div(children=[
                                        dcc.DatePickerRange(
                                            id='dash_tab2_date_range',
                                            min_date_allowed=date(2019, 12, 13),
                                            max_date_allowed=date.today()-timedelta(days=1),
                                            initial_visible_month=date.today()-timedelta(days=30),
                                            end_date=date.today()-timedelta(days=1),
                                            display_format='YYYY-MM-DD'
                                        ),
                                        dbc.Button("Load Data", id="dash_btn_load_check_data", className="me-2")
                                     ]),
                                     html.Br(),
                                     html.Div(children=[    
                                        dcc.Store(id='dash_store_data_table',storage_type='session'),
                                        dash_table.DataTable(
                                                id='dash_DT',
                                                columns=[ {"name": i, "id": i} for i in dataTable_column.columns ],
                                                page_current=0,
                                                page_size=30,
                                                page_action='custom',
                                                # style_as_list_view=True,
                                                style_cell={'padding-top': '2px','padding-bottom': '2px','padding-right': '5px'},
                                                style_table={'height': '600px', 'overflowY': 'auto'},
                                                style_cell_conditional=[
                                                    { 'if': {'column_id': 'Date'     }, 'textAlign': 'center' },
                                                    { 'if': {'column_id': 'Bank'     }, 'textAlign': 'center' },
                                                    { 'if': {'column_id': 'WeekDay'  }, 'textAlign': 'center' },
                                                    { 'if': {'column_id': 'Voltage'  }, 'textAlign': 'right'  },
                                                    { 'if': {'column_id': 'Current'  }, 'textAlign': 'right'  },
                                                    { 'if': {'column_id': 'ChargeQ'  }, 'textAlign': 'right'  },
                                                    { 'if': {'column_id': 'DataFail' }, 'textAlign': 'right'  },
                                                    { 'if': {'column_id': 'DataCount'}, 'textAlign': 'right'  },
                                                    { 'if': {'column_id': 'UseYN'    }, 'textAlign': 'center' },
                                                    { 'if': {'column_id': 'UseDesc'  }, 'textAlign': 'left'   },
                                                ],
                                                style_data_conditional=[
                                                    {
                                                        'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC',
                                                    },
                                                ],
                                                style_header={
                                                    'backgroundColor': '#BBBFBF',
                                                    'fontWeight': 'bold',
                                                    'textAlign': 'center'
                                                },
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