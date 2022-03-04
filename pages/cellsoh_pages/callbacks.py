from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
from datetime import date,timedelta
from tkinter import *
from tkinter import filedialog

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
from utils.constants  import *
from pages.cellsoh_pages.model import *

 
 



@app.callback(Output('ds_cellsoh_df'           , 'data'       ),
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
    if s_bank_no is None:
        raise PreventUpdate
    
    #------ Soh Cell Raw Data Loading ----------------
    data = cellsoh_data_load(start_date, end_date, str(s_bank_no), str(s_rack_no), str(s_module_no), str(s_cell_no) )

    return data.to_json(date_format='iso',orient='split') 




 


######################################################################################
## Render Plot 1
######################################################################################
@app.callback(Output('cellsoh_plot_1'  , 'figure'  ),
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
 
    fig = px.box(data, 
                 x="cyc_date",
                 y="soh",
                #  color="smoker",
                 notched=True, # used notched shape
                 title="SOH",
                 hover_data=["bank_no","rack_no","cell_no"] # add day column to hover data
                )

    fig.update_layout(showlegend=False)
    fig.update_layout(height=500)

    return fig




 