from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
from datetime import date,timedelta
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import tkinter

from sklearn.linear_model import LinearRegression
from sklearn import metrics

import os
import statsmodels.api as sm
import io
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go
import time
import json
import dash as html
import dash_table
import pickle
import re
import numpy as np

from utils.server_function import *
from utils.functions import *
from utils.constants  import *
from pages.cellsoh_pages.model import *

 
    
    

   


@app.callback(Output('ds_cellsoh_df'           , 'data'       ),
              Output('loading_cellsoh_1'       , 'children'   ),
              Input('btn_cellsoh_dataload'     , 'n_clicks'   ),
              State('date_range_cellsoh'       , 'start_date' ), 
              State('date_range_cellsoh'       , 'end_date'   ), 
              State('cbo_cellsoh_bank'         , 'value'      ), 
              State('cbo_cellsoh_rack'         , 'value'      ), 
              State('cbo_cellsoh_module'       , 'value'      ), 
              State('cbo_cellsoh_cell'         , 'value'      ) 
              )
def cb_cellsoh_data_load(n_clicks, start_date, end_date, s_bank_no, s_rack_no, s_module_no, s_cell_no):
    if n_clicks is None:
        raise PreventUpdate
    if start_date is None:
        raise PreventUpdate
    if end_date is None:
        raise PreventUpdate
    if s_bank_no is None or s_bank_no == '':
        uf_show_msg("뱅크번호를 선택하세요!")
        raise PreventUpdate
    
    #------ Soh Cell Raw Data Loading ----------------
    data = cellsoh_data_load(start_date, end_date, s_bank_no, s_rack_no, s_module_no, s_cell_no )

    return data.to_json(date_format='iso',orient='split') ,''




 


######################################################################################
## Render Plot 1
######################################################################################
@app.callback(Output('cellsoh_plot_1'  , 'figure'  ),
              Output('cellsoh_label_1' , 'children'  ),
              Input('ds_cellsoh_df'    , 'modified_timestamp'),
              State('ds_cellsoh_df'    , 'data'    )
              )
def cb_cellsoh_plot1_render(ts, data):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate


    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)
    data = data.sort_values("cyc_date",   ascending = True )
    
    data['cyc_date'] = data['cyc_date'].apply(str)
    data['bank_no'] = data['bank_no'].apply(str)
    data['rack_no'] = data['rack_no'].apply(str)
    data['module_no'] = data['module_no'].apply(str)
    data['cell_no'] = data['cell_no'].apply(str)
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    lbl_str = "Data Count : " + str(len(data))

    fig = px.box(data, 
                 x="cyc_date",
                 y="soh",
                 notched=True, # used notched shape
                 labels={"cyc_date": "Date","soh": "SOH"},
                 hover_data=["bank_no","rack_no","cell_no"] # add day column to hover data
                )
    fig.update_layout(clickmode='event+select')
    fig.update_layout(showlegend=False)
    fig.update_layout(height=520)

    return fig , lbl_str


 

# @app.callback(Output("cellsoh_modal_1"    , "is_open"),
#               Input("btn_cellsoh_viewdata", "n_clicks"),
#               State("cellsoh_modal_1"     , "is_open"),
#               Input("cellsoh_plot_1"      , "relayoutData"))
# def cb_cellsoh_toggle_modal(n, is_open, relayoutData):
    # if n:
    #     return not is_open
   
    # data= json.dumps(relayoutData , indent=2)

    # columns = [{"name": i, "id": i, } for i in train_df.columns]
    # train_df = train_df.head(30).to_dict('rows')
    # dataset_DataTable_3 = dash_table.DataTable(
    #                 data=train_df,
    #                 columns = columns,
    #                 editable=False,
    #                 style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
    #                 style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
    #                 column_selectable="single",
    #                 selected_rows=[],
    #                 sort_action='custom',
    #                 sort_mode='multi',
    #                 sort_by=[],
    #                 style_cell_conditional=[
    #                     { 'if': {'column_id': 'cyc_date'  }, 'textAlign': 'center'},
    #                     { 'if': {'column_id': 'bank_no'   }, 'textAlign': 'center'},
    #                     { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
    #                     { 'if': {'column_id': 'cell_no'   }, 'textAlign': 'center'},
    #                     { 'if': {'column_id': 'soh'       }, 'textAlign': 'right' },
    #                     {'fontSize' : '16px'},
    #                 ],
    #                 style_data_conditional=[
    #                     {
    #                         'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
    #                         # data_bars(dataTable_column, 'ChargeQ')  +
    #                         # data_bars(dataTable_column, 'Voltage'),
    #                     },
    #                 ],
    #                 style_header={
    #                     'backgroundColor': '#929494',
    #                     'fontWeight': 'bold',
    #                     'fontSize' : '16px',
    #                     'textAlign': 'center',
    #                     'height':'40px'
    #                 },
    #                 export_headers='display',
    #             )

    # return is_open