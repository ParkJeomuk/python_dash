import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_admin_components as dac
from components.table import make_dash_table
import pandas as pd
from datetime import date,timedelta
import dash_table
from dash_table.Format import Format, Group, Scheme

from utils.server_function import *
from pages.dash_pages.model import *


linerdm_model_columns = [
    dict(id='X'     , name='X'      , type='text'), 
    dict(id='Coefficient' , name='Coefficient' , type='numeric', format=Format(precision=30, scheme=Scheme.fixed).group(True)), 
]


linderdm_model_coef_DT = dash_table.DataTable(
                id='linerdm_md_coef_DT',
                columns = linerdm_model_columns,
                style_table={'height': '220px', 'overflowY': 'auto', 'overflowX': 'auto'},
                style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                sort_action='none',
                page_action='native',
                page_current=0,
                page_size=25,
                style_cell_conditional=[
                    { 'if': {'column_id': 'X'     }, 'textAlign': 'center', 'width': '40%' },
                    { 'if': {'column_id': 'Coefficient' }, 'textAlign': 'right', 'width': '60%' },
                ],
                style_header={'backgroundColor': '#626464','fontWeight': 'bold','textAlign': 'center','height':'40px'},
            )

linerdm_DT3_columns = [
    dict(id='Error'   , name='Error'   , type='text'), 
    dict(id='Model'   , name='Model'   , type='numeric'), 
    dict(id='Predict' , name='Predict' , type='numeric'), 
    dict(id='Pred/Model', name='Pred/Model[%]', type='numeric'), 
]

linerdm_DataTable_3 = dash_table.DataTable(
            id = 'linerdm_DT_3',
            columns = linerdm_DT3_columns,
            editable=False,
            style_table={'height': '450px', 'overflowY': 'auto', 'overflowX': 'auto'},
            style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
            column_selectable="single",
            selected_rows=[],
            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_cell_conditional=[
                { 'if': {'column_id': 'Error'   }, 'textAlign': 'left'},
                { 'if': {'column_id': 'Model'   }, 'textAlign': 'right'},
                { 'if': {'column_id': 'Predict' }, 'textAlign': 'right'},
                { 'if': {'column_id': 'Pred/Model'}, 'textAlign': 'right'},
                {'fontSize' : '16px'},
            ],
            style_header={
                'backgroundColor': '#929494',
                'fontWeight': 'bold',
                'fontSize' : '16px',
                'textAlign': 'center',
                'height':'40px'
            },
            export_headers='display',
        )
 




linerdm_condi_2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(children=[dbc.Label("Data Information")], width=12),
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.Div(id='div_linerdm_datainfo', 
                             style={'height':'440px', 'whiteSpace':'pre-line','border':'0px black solid','overflow':'scroll'}
                             )
                ], width=12)
            ],style={'padding-top': '5px', 'padding-bottom': '5px'}
        ),
    ],
    style={"height": "520px"},
    body=True,
)



linerdm_control_1 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dcc.Store(id='ds_linerdm_train_data' ,storage_type='memory'),
            dcc.Store(id='ds_linerdm_test_data'  ,storage_type='memory'),
            html.Br(), 
            dcc.Loading(id="loading_linerdm_1", type="circle", children=html.Div(id="linerdm_loading_output1")),
            dbc.Button(html.Span(["Data Load", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_linerdm_dataload", color="dark"),
        ], width=1,style={'padding-top': '7px'},),
        dbc.Col(children=[
            html.Br(), 
            dbc.Button(html.Span(["Data Info", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_linerdm_datainfo", color="dark"),
        ], width=1,style={'padding-top': '7px'},),
        dbc.Col(children=[
            dbc.Label("Model"),
            dcc.Dropdown(id="cbo_linerdm_model",options=[{"label": 'LM', "value": 'LM'}],value="LM",)
        ], width=1),
        dbc.Col(children=[
            dbc.Label("Y Var"),
            dcc.Dropdown(id="cbo_linerdm_y",options=[{"label": '', "value": ''}],value="",)
        ], width=2),
        dbc.Col(children=[
            dbc.Label("X Var"),
            dcc.Dropdown(id="cbo_linerdm_x",options=[{"label": '', "value": ''}],value="",multi=True)
        ], width=6),
        dbc.Col(children=[
            html.Br(), 
            dbc.Button(html.Span(["Calc", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_linerdm_model_apply", color="dark") 
        ], width=1,style={'padding-top': '7px', 'text-align':'right'},),
    ],style={'height': '100%'},),
    ],style={"height": "120px"},
    body=True,
)



linerdm_control_2 = dbc.Card([
    dbc.Row([
        dbc.Label("LM Model"),
        dcc.Loading(id="linerdm_plot_1_loading", type="dot",
                    children=dcc.Graph(
                        id="linerdm_plot_1",
                        figure={'data': [{'y': [0, 0] }],'layout': {'height': 450}}
                    )
                )
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height":"510px"},
)






linerdm_control_3 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Model Summary"),
            html.Div(id='div_linerdm_model_info', style={'height':'440px', 'whiteSpace':'pre-line','border':'1px #AEAFAF solid','overflow':'auto'})
        ], width=12, style={'padding-left': '15px', 'padding-right': '15px', 'padding-top': '15px', 'padding-bottom': '15px'}),
    ]),
    ],style={"height": "500px"},
)




linerdm_control_4 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[dbc.Label("Model Tuning/Save")], width=12),
    ]),
    dbc.Row([
        dbc.Col(children=[dbc.Label("Parameter")], width=2),
        dbc.Col(children=[dcc.Dropdown(id="cbo_linerdm_model_para",options=[{"label": 'x', "value": 'x'}],value="1",)], width=1),
        dbc.Col(children=[dbc.Button(html.Span(["Apply", html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_model_tune",color="dark") ], width=2),
        dbc.Col(children=[dbc.Label("Model Name")], width=2),
        dbc.Col(children=[html.Div(id="linderdm_div_save_model_name"), ], width=3),
        dbc.Col(children=[dbc.Button(html.Span(["Save" , html.I(className="fas fa-arrow-alt-circle-right ml-2")]),id="btn_linerdm_model_save",color="dark") ], width=2),
    ],style={'padding-left': '20px', 'padding-top': '5px', 'padding-bottom': '5px'},),
    ],style={"height": "120px"},
    body=True,
)


linerdm_control_5 = dbc.Card([
    dbc.Row([
        dbc.Label("LM Model Actually/Predict"),
        dcc.Loading(id="linerdm_plot_2_loading", type="dot",
                    children=dcc.Graph(
                        id="linerdm_plot_2",
                        figure={'data': [{'y': [0, 0] }],'layout': {'height': 450}}
                    )
                )
            ],style={'padding-top': '5px', 'padding-bottom': '5px'},
        ),
    ],
    style={"height":"500px"},
)


linerdm_control_6 = dbc.Card([
        dbc.Row([ 
                dbc.Col(children=[
                     dbc.Label("Test / Predict Data"),
                     html.H1(id='linerdm_DT_1'),                  
                ], width=12, style={'padding-top': '5px', 'padding-bottom': '5px'}, ),
        ],style={"height": "330px",'padding-left': '10px', 'padding-right': '10px'}, ),
    ],
    style={"height": "500px"},
)


linerdm_control_7 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Choice Model"),
            dcc.Dropdown(
                id="cbo_linerdm_model_choice",
                options=[
                    {"label": md_name, "value": md_name} for md_name in uf_load_model_list().md_name
                ],
                value="MODEL",
                multi=True)
        ], width=3),
        dbc.Col(children=[
            dbc.Label("Predict File"),html.Br(),
            html.Div(id='linerdm_predict_filname', style={'height':'35px','width':'100%', 'whiteSpace':'pre-line','border':'1px #E8EBEB solid','overflow':'auto'}) ,
        ], width=5),
        dbc.Col(children=[
            html.Br(), 
            dbc.Button(html.Span(["File Choice", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_linerdm_model_file", color="dark") 
        ], width=2,style={'padding-top': '7px'},),
        dbc.Col(children=[
            html.Br(), 
            dbc.Button(html.Span(["Predict", html.I(className="fas fa-arrow-alt-circle-right ml-2")]), id="btn_linerdm_model_predict", color="dark") 
        ], width=2,style={'padding-top': '7px', 'text-align':'right'},),
    ],style={'height': '100%'},),
    ],style={"height": "120px"},
    body=True,
)


linerdm_control_8 = dbc.Card([
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Model Predict Result"),
            dcc.Loading(id="linerdm_plot_3_loading", type="dot",
                        children=dcc.Graph(
                            id="linerdm_plot_3",
                            figure={'data': [{'y': [0, 0] }],'layout': {'height': 530}}
                        )
                    )
        ], width=12, style={'padding-top': '5px', 'padding-bottom': '5px'}, ),            
    ],style={'padding-top': '5px', 'padding-bottom': '5px'},), #dbc.Row
    ],style={"height":"600px"},
    body=True,
)




linerdm_control_10 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Model Coefficient"),
            linderdm_model_coef_DT
        ], width=12),
    ],style={'height': '100%'},),
    ],style={"height": "300px"},
    body=True,
)


linerdm_control_11 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Prediction Result"),
            linerdm_DataTable_3
        ], width=12),
    ],style={'height': '100%'},),
    ],style={"height": "300px"},
    body=True,
)

linerdm_control_9 = dbc.Card([
        dbc.Row([ 
                dbc.Col(children=[
                     dbc.Label("Prediction Data"),
                     html.H1(id='linerdm_DT_2'),    
                ], width=12, style={'height': '100%'}, ),
        ],style={"height": "330px"}, ),
    ],style={"height": "600px"},
    body=True,
)


linerdm_control_12 = dbc.Card([  
    dbc.Row([
        dbc.Col(children=[
            dbc.Label("Model Desc")
        ], width=12),
    ],style={'height': '100%'},),
    ],style={"height": "300px"},
    body=True,
)





content = dac.TabItem(id='content_linermd_pages',
                        children=html.Div([
                            dbc.Tabs([
                                #------First Tab Start --------------------------------------------------------------------------
                                dbc.Tab(label="Modeling", active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                    children=html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Col([ linerdm_control_1 ],md=12, style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                    ]),
                                                    dbc.Row([
                                                        dbc.Col([ linerdm_control_2 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                                        dbc.Col([ linerdm_control_3 ],md=5, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                    ]),
                                                    dbc.Row([
                                                        dbc.Col([ linerdm_control_5 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                                        dbc.Col([ linerdm_control_6 ],md=5, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                    ]) ,
                                                    dbc.Row([
                                                        dbc.Col([ linerdm_control_4 ],md=7, style={"padding-left": "10px","padding-right": "10px", },),
                                                    ]) 
                                                ],md=12, style={"height": "100%"},),
                                            ],),
                                        ],
                                    ),  
                                ),
                                #------First Tab End    --------------------------------------------------------------------------
                                #------Second Tab Start --------------------------------------------------------------------------
                                dbc.Tab(label='Prediction', active_label_class_name="fw-bold", tab_class_name="flex-grow-1 text-center",
                                children=[
                                    dbc.Row([
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Col([ 
                                                            linerdm_control_7 
                                                        ],md=12, style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                    ]),
                                                    dbc.Row([
                                                        dbc.Col([ 
                                                            linerdm_control_12
                                                        ],md=3, style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                        dbc.Col([ 
                                                            linerdm_control_10
                                                        ],md=3, style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                        dbc.Col([ 
                                                            linerdm_control_11
                                                        ],md=6, style={"padding-top": "10px","padding-left": "10px","padding-right": "10px", }, ),
                                                    ]),
                                                    dbc.Row([
                                                        dbc.Col([ 
                                                            linerdm_control_8 
                                                        ],md=6, style={"padding-left": "10px","padding-right": "10px", },),
                                                        dbc.Col([ 
                                                            linerdm_control_9 
                                                        ],md=6, style={"padding-left": "10px","padding-right": "10px", }, ),
                                                    ])
                                                ],md=12, style={"height": "100%"},),
                                            ],),
                                    ]),
                                #------Second Tab End   --------------------------------------------------------------------------
                            ])
                               
						] ,style={'width': '100%'} )
                            # className='flex-container'
         )                        