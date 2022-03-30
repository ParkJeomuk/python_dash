from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date,timedelta,datetime
from tkinter import *
from tkinter import filedialog
from dash import dash_table


import dash_bio as dashbio
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go
import time
import json
import dash as html
import pickle
import re
import numpy as np

from utils.server_function import *
from utils.constants  import *
from pages.aging_pages.model import *





@app.callback(Output('ds_aging_df'        , 'data'     ),
              Output('loading_aging_1'    , 'children' ),
              Input('btn_aging_dataload'  , 'n_clicks' ),
              State('dtp_aging_date_1'    , 'date'     ), 
              State('dtp_aging_date_2'    , 'date'     ), 
              State('cbo_cellsoh_bank'    , 'value'    ), 
              State('cbo_cellsoh_rack'    , 'value'    ) 
              )
def cb_cellsoh_data_load(n_clicks, date1, date2, s_bank_no, s_rack_no):
    if n_clicks is None:
        raise PreventUpdate
    if date1 is None:
        uf_show_msg("Date1을 입력하세요!")
        raise PreventUpdate
    if date2 is None:
        uf_show_msg("Date2을 입력하세요!")
        raise PreventUpdate
    if s_bank_no is None or s_bank_no == '':
        uf_show_msg("뱅크번호를 선택하세요!")
        raise PreventUpdate
    
    data = aging_gap_data_load(date1, date2, s_bank_no)

    return data.to_json(date_format='iso',orient='split') ,''



 


######################################################################################
## Render Plot 1
######################################################################################
@app.callback(Output('aging_plot_1'      , 'figure'   ),
              Output('aging_plot_2'      , 'figure'   ),
              Output('aging_plot_3'      , 'figure'   ),
              Output('aging_plot_4'      , 'figure'   ),
              Output('ds_aging_top25'    , 'data'     ),
              Output('ds_aging_bottom25' , 'data'     ),
              Input('ds_aging_df'        , 'modified_timestamp'),
              State('ds_aging_df'        , 'data'     )
              )
def cb_cellsoh_plot1_render( ts, data):
    if ts is None or data is None:
        fig =  blank_fig() 
        return fig, fig, fig, fig, None, None


    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)

    data['rack_no'] = data['rack_no'].apply(str)
    data['module_no'] = data['module_no'].apply(str)
    data['cell_no'] = data['cell_no'].apply(str)
    data['soh_gap'] = data.soh_x.values - data.soh_y.values
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig , fig , fig, fig , None, None
    
    tmp_df = data[['rack_no','cell_no','soh_gap']].pivot('cell_no','rack_no','soh_gap')

    colorMap =  [[0.0,'#FEFDFB'],[0.5, '#FCD82D'],[1,'#921205']]

    columns = list(tmp_df.columns.values)
    rows = list(tmp_df.index)

    fig1 = dashbio.Clustergram(
                        data=tmp_df.loc[rows].values,
                        row_labels=rows,
                        column_labels=columns,
                        height=950,
                        width=1400,
                        center_values=False,
                        color_map= colorMap
                    )
    fig1.update_layout(showlegend=False)


    
    fig2 = px.box(data, 
                  y="soh_gap" , 
                  points="all" ,
                  hover_data=["rack_no","module_no","cell_no"]
                 )
    fig2.update_layout(showlegend=False)

    colList = ['rack_no','module_no','cell_no', 'soh_gap']
    good_df = data.sort_values(by='soh_gap', ascending=False).iloc[0:25,]
    r_t_df  = good_df.to_json(date_format='iso',orient='split')
    good_df = good_df[colList]


    bad_df  = data.sort_values(by='soh_gap', ascending=True ).iloc[0:25,]
    r_b_df  = bad_df.to_json(date_format='iso',orient='split')
    bad_df  = bad_df[colList]

    good_df['seq'] = range(1,26)
    bad_df['seq'] = range(1,26)
    
    # good_df['text'] = good_df['rack_no'] + ":" + good_df['cell_no'] + ":" + round(good_df['soh_gap'],4).apply(str)
    # bad_df['text']  = bad_df['rack_no']  + ":" + bad_df['cell_no']  + ":" + round(bad_df['soh_gap'],4).apply(str)


    fig3 = px.scatter(good_df, 
                      x="seq", 
                      y="soh_gap",
                      hover_data=["rack_no","module_no","cell_no"]
                    #   , 
                    #   text='text'
                      )
    


    fig4 = px.scatter(bad_df, 
                      x="seq", 
                      y="soh_gap",
                      hover_data=["rack_no","module_no","cell_no"]
                    #   , 
                    #   text='text'
                      )
    # fig4.update(mode='markers+lines')

    return fig1, fig2, fig3, fig4, r_t_df, r_b_df







#------------ Top 25 View -----------------------------------------------------
@app.callback(Output("aging_modal_1"   , "is_open"  ),
              Output("aging_DT_1"      , "children" ),
              Input("btn_cellsoh_good" , "n_clicks" ),
              State("aging_modal_1"    , "is_open"  ),
              State('ds_aging_top25'   , 'data'     )
              )
def cb_cellsoh_view_good_modal(n_clicks, is_open, ds_data):
    if n_clicks is None :
        raise PreventUpdate

    if ds_data is None :
        data = None
        dt_style = {'height': '50px','overflowY': 'auto', 'overflowX': 'auto'}
    else:
        data = pd.read_json(ds_data, orient='split').to_dict('rows')
        dt_style = {'height': '600px','overflowY': 'auto', 'overflowX': 'auto'}

    aging_DT1_columns = [
                            dict(id='seq'      , name='No'   , type='numeric'), 
                            dict(id='cyc_date' , name='Date' , type='text'), 
                            dict(id='rack_no'  , name='Rack' , type='text'), 
                            dict(id='module_no', name='Module' , type='text'), 
                            dict(id='cell_no'  , name='Cell' , type='text'), 
                            dict(id='soh'      , name='SOH'  , type='numeric'), 
                            dict(id='q_a'      , name='Q A'  , type='numeric'), 
                            dict(id='q_u'      , name='Q U'  , type='numeric'), 
                            dict(id='cur_avg'  , name='Current Avg'  , type='numeric'), 
                            dict(id='n'        , name='N'      , type='numeric'), 
                            dict(id='u_vol'    , name='U Vol'  , type='numeric'), 
                            dict(id='o_vol'    , name='O Vol'  , type='numeric'), 
                            dict(id='gap'      , name='Gap'    , type='numeric'), 
                        ]

    aging_DataTable_1 = dash_table.DataTable(
                    data=data,
                    columns = aging_DT1_columns,
                    editable=False,
                    style_table=dt_style,
                    style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                    column_selectable="single",
                    selected_rows=[],
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    style_cell_conditional=[
                        { 'textAlign': 'right' },
                        { 'if': {'column_id': 'cyc_date'  }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'module_no' }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'cell_no'   }, 'textAlign': 'center'},
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

    return not is_open , aging_DataTable_1

 


