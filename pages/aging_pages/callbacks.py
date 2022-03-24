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
@app.callback(Output('aging_plot_1'  , 'figure'   ),
              Input('ds_aging_df'    , 'modified_timestamp'),
              State('ds_aging_df'    , 'data'     )
              )
def cb_cellsoh_plot1_render( ts, data):
    if ts is None or data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig


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
        return fig
    
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

    return fig1  

