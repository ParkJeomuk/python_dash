import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html 
import dash_admin_components as dac
from components.table import make_dash_table
from pages.dash_pages.model import df_bank, df_data_type
from datetime import date


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
                            date=date.today(),
                            display_format='YYYY-MM-DD'
                        ) 
                ], width=6),
                dbc.Col(children=[
                    dbc.Label("Compare Date"),
                    dcc.DatePickerSingle(
                            id='dtp_dash_compare',
                            min_date_allowed=date(2019, 12, 13),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            date=date.today(),
                            display_format='YYYY-MM-DD'
                    )
                ], width=6)
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    dbc.Button("Load", id="dash_btn_load", className="me-2")
                ], width=12),
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
    style={"height": "240px"},
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
    style={"height": "240px"},
    body=True,
)



condi_3 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dbc.Label("Right Info Box"), 
            ]
        ),
    ],
    style={"height": "240px"},
    body=True,
)

dash_control_1 = dbc.Card(
    [
        #dbc.FormGroup(
        dbc.Row(
            [
                dcc.Store(id='dash_df',storage_type='session'),
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


content = dac.TabItem(id='content_dash_pages',
                        children=html.Div([
                            dcc.Tabs([
                                dcc.Tab(label='Validation Raw Data ',  
                                    children=html.Div(
                                        [
                                            
                                            dbc.Row([html.Br(),]),
                                            dbc.Row(
                                                    [
                                                        dbc.Col(condi_1, md=2, style={"height": "100%"},),
                                                        dbc.Col(condi_2, md=3, style={"height": "100%"},),
                                                        dbc.Col(condi_3, md=7, style={"height": "100%"},),
                                                    ],
                                                    align="center",
                                                    style={"height": "220"},
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
                             
                                dcc.Tab(label='Tab two', children=[
                                    dcc.Store(id='dash_raw_data',storage_type='session'),
                                    # dcc.Loading(id="dash_plot_5_loading", type="default",
                                    #             children=dcc.Graph(
                                    #                 id="dash_plot_5")

                                    #             ),
                                    html.Br(),
                                    html.Div(children=[
                                        dbc.Button("Load Data", id="dash_btn_load_raw_data", className="me-2"),
                                        html.Label('Plot Type', style={"padding-left":"10px", "padding-right":"10px"}),

                                        dcc.RadioItems(id='dash_rdo_plot5_type',
                                                   options=[
                                                       {'label': 'Line','value': 'L'},
                                                       {'label': 'Point','value': 'P'},
                                                       {'label': 'Line+Point','value': 'LP'}
                                                   ],
                                                   value='L',
                                                   labelStyle={'display': 'inline-block'}
                                                   ),
                                        
                                    ],style={'display': 'flex'})
                                ]),

                            ])
                        ],
                        style={'width': '100%'}
                            # className='flex-container'
                        )
                        )