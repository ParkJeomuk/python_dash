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

from scipy.spatial.distance import pdist, squareform

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
import plotly.figure_factory as ff
from pages.dash_pages.model import df_dash_q_data




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
@app.callback(Output('cellsoh_plot_1'  , 'figure'   ),
            #   Output('cellsoh_label_1' , 'children' ),
              Input('cbo_cellsoh_y'    , 'value'    ),
              Input('ds_cellsoh_df'    , 'modified_timestamp'),
              State('ds_cellsoh_df'    , 'data'     )
              )
def cb_cellsoh_plot1_render(y_val, ts, data):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    if y_val is None:
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
    
    # lbl_str = "Data Count : " + str(len(data))

    fig = px.box(data, 
                 x="cyc_date",
                 y=y_val,
                 notched=True, # used notched shape
                 labels={"cyc_date": "Date",y_val: y_val},
                 hover_data=["bank_no","rack_no","cell_no"] # add day column to hover data
                )
    fig.update_layout(clickmode='event+select')
    fig.update_layout(showlegend=False)
    fig.update_layout(height=520)

    return fig #, lbl_str





######################################################################################
## Render Plot 2
######################################################################################
@app.callback(Output('cellsoh_plot_2'            , 'figure'   ),
              Input('btn_cellsoh_detailview'     , 'n_clicks' ),
              State('cbo_cellsoh_detail'         , 'value'    ),
              State('cbo_cellsoh_detail_rack'    , 'value'    ),
              State('cbo_cellsoh_detail_module'  , 'value'    ),
              State('cbo_cellsoh_detail_cell'    , 'value'    ),
              State('ds_cellsoh_df'              , 'data'     )
              )
def cb_cellsoh_plot1_render(n_clicks,view_type, rack_no, module_no, cell_no, data):
    if n_clicks is None:
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
    

    if uf_is_empty(rack_no)==False:
        data = data[(data["rack_no"]==str(rack_no))]

    if uf_is_empty(module_no)==False:
        data = data[(data["module_no"]==str(module_no))]

    if uf_is_empty(cell_no)==False:
        data = data[(data["cell_no"]==str(cell_no))]

    if view_type == 'R':
      grp = ['cyc_date','rack_no']
      sColor = 'rack_no'
    elif view_type == 'M':
      grp = ['cyc_date','rack_no','module_no']
      sColor = 'module_no'
    else:
      grp = ['cyc_date','rack_no','module_no','cell_no']
      sColor = 'cell_no'

    # data.groupby(['rack_no', 'module_no', 'cell_no']).mean()
    data =  pd.concat([data[grp], data['soh']], axis=1)
    data = data.groupby(grp, as_index=False).mean()


    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    # lbl_str = "Data Count : " + str(len(data))

    # fig = px.box(data, 
    #              x="cyc_date",
    #              y="soh",
    #              notched=True, # used notched shape
    #              labels={"cyc_date": "Date","SOH":"soh"},
    #              hover_data=["rack_no"] # add day column to hover data
    #             )
    # fig.update_layout(clickmode='event+select')
    # fig.update_layout(showlegend=False)
    # fig.update_layout(height=520)

    fig = px.scatter(data, x='cyc_date', y="soh", color=sColor )
    fig.update_traces(marker=dict(size=11, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))
    fig.update_layout(showlegend=True)
    fig.update_layout(height=460)

    return fig


 

 
######################################################################################
## Render Plot 21
######################################################################################
@app.callback(Output('cellsoh_plot_21'         , 'figure'     ),
              Output('cellsoh_plot_22'         , 'figure'     ),
              Output('cellsoh_plot_23'         , 'figure'     ),
              Input('btn_cellsoh_heatview'     , 'n_clicks'   ),
              State('dtp_cellsoh_detail_date'  , 'date'       ), 
              State('date_range_cellsoh'       , 'start_date' ), 
              State('date_range_cellsoh'       , 'end_date'   ), 
              State('cbo_cellsoh_bank'         , 'value'      ), 
              State('cbo_cellsoh_rack'         , 'value'      ), 
              State('cbo_cellsoh_module'       , 'value'      ), 
              State('cbo_cellsoh_cell'         , 'value'      ) 
              )
def cb_cellsoh_plot21_render(n_clicks, s_date, start_date, end_date, s_bank_no, s_rack_no, s_module_no, s_cell_no):
    if n_clicks is None:
        raise PreventUpdate

    
    # # get data
    # data = np.genfromtxt("http://files.figshare.com/2133304/ExpRawData_E_TABM_84_A_AFFY_44.tab",
    #                     names=True,usecols=tuple(range(1,30)),dtype=float, delimiter="\t")
    # data_array = data.view((np.float, len(data.dtype.names)))
    # data_array = data_array.transpose()
    # labels = data.dtype.names

    # # Initialize figure by creating upper dendrogram
    # fig = ff.create_dendrogram(data_array, orientation='bottom', labels=labels)
    # for i in range(len(fig['data'])):
    #     fig['data'][i]['yaxis'] = 'y2'

    # # Create Side Dendrogram
    # dendro_side = ff.create_dendrogram(data_array, orientation='right')
    # for i in range(len(dendro_side['data'])):
    #     dendro_side['data'][i]['xaxis'] = 'x2'

    # # Add Side Dendrogram Data to Figure
    # for data in dendro_side['data']:
    #     fig.add_trace(data)

    # # Create Heatmap
    # dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    # dendro_leaves = list(map(int, dendro_leaves))
    # data_dist = pdist(data_array)
    # heat_data = squareform(data_dist)
    # heat_data = heat_data[dendro_leaves,:]
    # heat_data = heat_data[:,dendro_leaves]

    # heatmap = [
    #     go.Heatmap(
    #         x = dendro_leaves,
    #         y = dendro_leaves,
    #         z = heat_data,
    #         colorscale = 'Blues'
    #     )
    # ]

    #------ Soh Cell Raw Data Loading ----------------
    df = cellsoh_data_load(start_date, end_date, s_bank_no, s_rack_no, s_module_no, s_cell_no )
    df = df[df['cyc_date']== s_date.replace('-','') ]
    df = df[['rack_no','cell_no','soh']]
    gb = df.groupby('cell_no')
    ldf = [gb.get_group(x) for x in gb.groups]
    ld = np.array([ldf[x]['soh'].tolist()  for x in range(len(ldf))])

    x_list = list(range(1,29))
    y_list = list(range(1,277))

    # heatmap = [
    #     go.Heatmap(
    #         x = x_list,
    #         y = y_list,
    #         z = ld,
    #         colorscale = 'Blues'
    #     )
    # ]

    # fig = go.Heatmap(
    #         x = x_list,
    #         y = y_list,
    #         z = ld,
    #         colorscale = 'Blues'
    #       )

    pio.templates.default = "plotly_white"


    fig1 = go.Figure(data=go.Heatmap( z=ld,
                                      x=x_list,
                                      y=y_list,
                                      hoverongaps = False))
    # heatmap[0]['x'] = fig['layout']['xaxis']['tickvals']
    # heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    # for data in heatmap:
    #     fig.add_trace(data)

    # Edit Layout
    fig1.update_layout({'height':600,'showlegend':False, 'hovermode': 'closest',})

    # # Edit xaxis
    # fig.update_layout(xaxis={'domain': [.15, 1],
    #                                 'mirror': False,
    #                                 'showgrid': False,
    #                                 'showline': False,
    #                                 'zeroline': False,
    #                                 'ticks':""})
    # # Edit xaxis2
    # fig.update_layout(xaxis2={'domain': [0, .15],
    #                                 'mirror': False,
    #                                 'showgrid': False,
    #                                 'showline': False,
    #                                 'zeroline': False,
    #                                 'showticklabels': False,
    #                                 'ticks':""})

    # # Edit yaxis
    # fig.update_layout(yaxis={'domain': [0, .85],
    #                                 'mirror': False,
    #                                 'showgrid': False,
    #                                 'showline': False,
    #                                 'zeroline': False,
    #                                 'showticklabels': False,
    #                                 'ticks': ""
    #                         })
    # # Edit yaxis2
    # fig.update_layout(yaxis2={'domain':[.825, .975],
    #                                 'mirror': False,
    #                                 'showgrid': False,
    #                                 'showline': False,
    #                                 'zeroline': False,
    #                                 'showticklabels': False,
    #                                 'ticks':""})



    fig2 = px.box(df, 
                 x="rack_no",
                 y="soh",
                 title="Boxplot of SOH",
                 notched=True, # used notched shape
                 labels={"rack_no": "Rack","soh": "SOH"},
                 hover_data=["rack_no","cell_no","soh"] # add day column to hover data
                )
    fig2.update_layout(clickmode='event+select')
    fig2.update_layout(showlegend=False)
    fig2.update_layout(height=450)



    sum_df = df[['rack_no','soh']].groupby(['rack_no'],as_index=False).sum()
    sum_df['minmax']=''

    sum_df['minmax'][sum_df['soh'].idxmax()] = 'MAX :' + str(sum_df['soh'].max())
    sum_df['minmax'][sum_df['soh'].idxmin()] = 'MIN :' + str(sum_df['soh'].min())
    minmax_gap = str(sum_df['soh'].max() - sum_df['soh'].min())

    fig3 =  px.line(sum_df, 
                    x = 'rack_no',
                    y = 'soh', 
                    title='Rack Sums & Max Gap [ ' + minmax_gap + ' ]',
                    labels={"rack_no": "Rack","soh": "SOH Sums"},
                    text=sum_df['minmax'],
                    markers=True
                    ) 
    fig3.update_traces(marker=dict(size=18,opacity=0.5 ,line=dict(width=1)),selector=dict(mode='markers'))               
    # fig3.update_traces(mode="lines")           
    fig3.update_layout(hovermode="closest")
    fig3.update_layout(showlegend=False)
    fig3.update_layout(height=450)


    return fig1 , fig2 , fig3







@app.callback(Output("cellsoh_modal_1"    , "is_open"),
              Output("cellsoh_DT_1"       , "children"),
              Input("btn_cellsoh_viewdata", "n_clicks"),
              State("cellsoh_modal_1"     , "is_open"),
              State("cellsoh_plot_1"      , "selectedData"))
def cb_cellsoh_toggle_modal(n_clicks, is_open, selectedData):
    if n_clicks is None:
        raise PreventUpdate
   
    data= json.dumps(selectedData , indent=2)

    if len(selectedData['points']) > 0 :
        df = pd.DataFrame(selectedData['points'])

        ddata = df[['x','y']]
        cdata = pd.DataFrame(df['customdata'].tolist())
        data = pd.concat([ddata,cdata],axis=1)
        data = data.rename(columns={'x': 'cyc_date', 'y': 'soh', 0:'bank_no', 1:'rack_no', 2:'cell_no'})
        data = data[['cyc_date','bank_no','rack_no','cell_no','soh']]
        data = data.to_dict('rows')
    else:
        data = None

    cellsoh_DT1_columns = [
                            dict(id='cyc_date', name='Date' , type='text'), 
                            dict(id='bank_no' , name='Bank' , type='text'), 
                            dict(id='rack_no' , name='Rack' , type='text'), 
                            dict(id='cell_no' , name='Cell' , type='text'), 
                            dict(id='soh'     , name='SOH'  , type='numeric'), 
                          ]

    cellsoh_DataTable_1 = dash_table.DataTable(
                    data=data,
                    columns = cellsoh_DT1_columns,
                    editable=False,
                    style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
                    style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                    column_selectable="single",
                    selected_rows=[],
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    style_cell_conditional=[
                        { 'if': {'column_id': 'cyc_date'  }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'bank_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'cell_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'soh'       }, 'textAlign': 'right' },
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

    return not is_open, cellsoh_DataTable_1






# @app.callback(Output("div_cellsoh_select_date" , "children"),
#               Input("cellsoh_plot_1"           , "clickData"))
# def cb_cellsoh_click_date(clickData):
#     if clickData is None:
#         raise PreventUpdate
    
#     if len(clickData)>0:
#         df =  pd.DataFrame(clickData['points'])
#         if len(df)>0:
#             selectDate = df['x'][0] #첫번째 포인트의 일자
#             selectDate = selectDate[0:4] + "-" + selectDate[4:6] + "-" + selectDate[6:8]
#         else:
#             selectDate = "____-__-__"    
#     else:
#         selectDate = "____-__-__"
    
#     return selectDate