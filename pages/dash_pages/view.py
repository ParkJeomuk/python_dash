import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html 
import dash_admin_components as dac
from pages.gallery_1.model import dataframe
from components.table import make_dash_table
 
content = dac.TabItem(id='content_dash_pages',
                        children=html.Div([
                            dcc.Tabs([
                                dcc.Tab(label='Rack ', children=[
                                    dcc.Store(id='dash_df',
                                              storage_type='session'),
                                    dcc.Loading(id="dash_plot_1_loading", type="default",
                                                children=dcc.Graph(
                                                    id="dash_plot_1")
                                                ),
                                    html.Br(),
                                    html.Div(children=[
                                        dbc.Button("Load", id="dash_btn_load", className="me-2"),
                                        html.Label('Plot Type', style={"padding-left":"10px", "padding-right":"10px"}),
                                        dcc.RadioItems(id='dash_rdo_plot_type',
                                                   options=[
                                                       {'label': 'Line','value': 'L'},
                                                       {'label': 'Point','value': 'P'},
                                                       {'label': 'Line+Point','value': 'LP'}
                                                   ],
                                                   value='L',
                                                   labelStyle={'display': 'inline-block'}
                                                   ),
                                        
                                    ],style={'display': 'flex'}),
                                    html.Br(),
                                    dcc.Loading(id="dash_plot_2_loading", type="default",
                                                children=dcc.Graph(
                                                    id="dash_plot_2")
                                                )
                                ]),
                                dcc.Tab(label='Tab two', children=[
                                    dcc.Store(id='dash_raw_data',storage_type='session'),
                                    dcc.Loading(id="dash_plot_3_loading", type="default",
                                                children=dcc.Graph(
                                                    id="dash_plot_3")
                                                ),
                                    html.Br(),
                                    html.Div(children=[
                                        dbc.Button("Load Data", id="dash_btn_load_raw_data", className="me-2"),
                                        html.Label('Plot Type', style={"padding-left":"10px", "padding-right":"10px"}),
                                        dcc.RadioItems(id='dash_rdo_plot3_type',
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
                                dcc.Tab(label='Tab three', children=[
                                    dcc.Graph(
                                        figure={
                                            'data': [
                                                {'x': [1, 2, 3], 'y': [2, 4, 3],
                                                 'type': 'bar', 'name': 'SF'},
                                                {'x': [1, 2, 3], 'y': [5, 4, 3],
                                                 'type': 'bar', 'name': u'Montréal'},
                                            ]
                                        }
                                    )
                                ]),
                            ])
                        ],
                        style={'width': '100%'}
                            # className='flex-container'
                        )
                        )