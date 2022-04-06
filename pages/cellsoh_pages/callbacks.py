from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_bio as dashbio

from datetime import date,timedelta, datetime
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
                 hover_data=["bank_no","rack_no","module_no","cell_no"] # add day column to hover data
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
              Input('btn_cellsoh_detail_predict' , 'n_clicks' ),
              State('cbo_cellsoh_detail'         , 'value'    ),
              State('cbo_cellsoh_detail_rack'    , 'value'    ),
              State('cbo_cellsoh_detail_module'  , 'value'    ),
              State('cbo_cellsoh_detail_cell'    , 'value'    ),
              State('ds_cellsoh_df'              , 'data'     ),
              State('pred_date_range_cellsoh'    , 'start_date'),
              State('pred_date_range_cellsoh'    , 'end_date'  )
              )
def cb_cellsoh_plot1_render(n_clicks, pred_clicks, view_type, rack_no, module_no, cell_no, data, start_date, end_date ):
    if data is None:
        raise PreventUpdate

    if pred_clicks is not None and (start_date is None or end_date is None) :
        pred_clicks = None



    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)
    data = data.sort_values("cyc_date",   ascending = True )
    
    data['cyc_date'] = data['cyc_date'].apply(str)
    data['bank_no'] = data['bank_no'].apply(str)
    data['rack_no'] = data['rack_no'].apply(str)
    data['module_no'] = data['module_no'].apply(str)
    data['cell_no'] = data['cell_no'].apply(str)
    

    

    

    mean_df = data[['cyc_date','soh']].groupby(['cyc_date'],as_index=False).mean()

    if view_type == 'R':
        if uf_is_empty(rack_no)==False:
            data = data[(data["rack_no"]==str(rack_no))]

        grp = ['cyc_date','rack_no']
        sColor = 'rack_no'
    elif view_type == 'M':
        if uf_is_empty(rack_no)==False:
            data = data[(data["rack_no"]==str(rack_no))]
        if uf_is_empty(module_no)==False:
            data = data[(data["module_no"]==str(module_no))]

        grp = ['cyc_date','rack_no','module_no']
        sColor = 'module_no'
    else:
        if uf_is_empty(rack_no)==False:
            data = data[(data["rack_no"]==str(rack_no))]
        if uf_is_empty(module_no)==False:
            data = data[(data["module_no"]==str(module_no))]
        if uf_is_empty(cell_no)==False:
            data = data[(data["cell_no"]==str(cell_no))]

        grp = ['cyc_date','rack_no','module_no','cell_no']
        sColor = 'cell_no'

    data =  pd.concat([data[grp], data['soh']], axis=1)
    data = data.groupby(grp, as_index=False).mean()

    #------ 기간 예측 버튼 클릭 ---------------------
    if pred_clicks is not None :
        lm_model = pickle.load(open( './model/lm_model_soh_test.sav'  , 'rb'))  # Model Load
        if start_date is None or end_date is None :
            raise PreventUpdate
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end   = datetime.strptime(end_date  , "%Y-%m-%d")

        p_data = pd.DataFrame([[(start + timedelta(days=x)).strftime("%Y%m%d"), (start + timedelta(days=x)).weekday()] for x in range(0, (end-start).days)])
        p_data.rename(columns = {0 : 'cyc_date', 1:'weekday'}, inplace = True)
        p_data = pd.DataFrame(p_data[(p_data['weekday']==2)]['cyc_date']).reset_index(drop=True) #수요일 데이타만 사용함.

        #수요일이 없을 경우 원래 데이타로 처리....
        if p_data is None or len(p_data)==0:
             p_data = pd.DataFrame([(start + timedelta(days=x)).strftime("%Y%m%d")  for x in range(0, (end-start).days)])
             p_data.rename(columns = {0 : 'cyc_date'}, inplace = True)

        data_pred= pd.DataFrame(lm_model.predict(p_data))
        data_pred.rename(columns = {0 : 'soh'}, inplace = True)
        p_data['soh'] = data_pred['soh']


    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    data["type"] = "Actually"

    if pred_clicks is not None :
        p_data["type"] = "Predict"
        p_data['rack_no'] = data['rack_no'][0]
        data = pd.concat([data[['type','cyc_date','rack_no','soh']],p_data[['type','cyc_date','rack_no','soh']] ],axis=0)
    else:
        data = data[['type','cyc_date','rack_no','soh']]

    fig = px.scatter(data, 
                     x='cyc_date', 
                     y="soh", 
                     color='type' , 
                     hover_data=["type","rack_no","cyc_date","soh"]
                    )
    fig.update_traces(marker=dict(size=11, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))

    if mean_df is not None and len(mean_df) > 0 :
        fig.add_trace(go.Scatter(x=mean_df['cyc_date'], y=mean_df['soh'], 
                    mode='lines',
                    name='Mean SOH'
                    ))

    fig.update_layout(showlegend=True)
    fig.update_layout(height=460)

    return fig


 

 
######################################################################################
## Render Plot 21
######################################################################################
@app.callback(Output('cellsoh_plot_21'         , 'figure'     ),
              Output('cellsoh_plot_22'         , 'figure'     ),
            #   Output('cellsoh_plot_23'         , 'figure'     ),
              Output('cellsoh_plot_24'         , 'figure'     ),
              Output('cellsoh_plot_25'         , 'figure'     ),
              Output('ds_cellsoh_good_df'      , 'data'       ),
              Output('ds_cellsoh_bad_df'       , 'data'       ),
              Output('ds_cellsoh_plot23_df'    , 'data'       ),              
              Output('input_cellsoh_upper'     , 'value'      ),
              Output('input_cellsoh_lower'     , 'value'      ),
              Input('btn_cellsoh_heatview'     , 'n_clicks'   ),
              Input('btn_cellsoh_redraw'       , 'n_clicks'   ),
              State('dtp_cellsoh_detail_date'  , 'date'       ), 
              State('date_range_cellsoh'       , 'start_date' ), 
              State('date_range_cellsoh'       , 'end_date'   ), 
              State('cbo_cellsoh_bank'         , 'value'      ),
              State('rdo_cellsoh_heatmaptype'  , 'value'      ),
              State('rdo_cellsoh_heatmap_color', 'value'      ),
              State('input_cellsoh_upper'      , 'value'      ),
              State('input_cellsoh_lower'      , 'value'      ),
              State('dtp_cellsoh_stand_date'   , 'date'       )
              )
def cb_cellsoh_plot21_render(n_clicks,redraw_clicks, s_date, start_date, end_date, s_bank_no, s_data_type, s_color_type, n_upper_soh, n_lower_soh, stand_date):
    if n_clicks is None:
        raise PreventUpdate


    #------ Soh Cell Raw Data Loading ----------------
    s_rack_no = ""
    s_module_no = "" 
    s_cell_no = ""
    df = cellsoh_data_load(start_date, end_date, s_bank_no, s_rack_no, s_module_no, s_cell_no )
    stand_df = df[df['cyc_date']== stand_date.replace('-','') ]
    df = df[df['cyc_date']== s_date.replace('-','') ]
    
    if s_data_type == "C":
        tmp_df = df[['rack_no','cell_no','soh']].pivot('cell_no','rack_no','soh')
    else:    
        tmp_df = df[['rack_no','module_no','soh']].groupby(['rack_no','module_no'],as_index=False).mean()
        tmp_df = tmp_df[['rack_no','module_no','soh']].pivot('module_no','rack_no','soh')

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if df is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig, fig, fig, fig, fig, None, None, None, None

    if s_color_type == 'D':
        colorMap =  [[0.0, '#FEFDFB'],[0.2, '#FCD82D'],[1.0, '#921205']]
    else:    
        colorMap =  [[0.0, '#921205'],[0.8, '#FCD82D'],[1.0, '#FEFDFB']]

    columns = list(tmp_df.columns.values)
    rows = list(tmp_df.index)

    fig1 = dashbio.Clustergram(
                        data=tmp_df.loc[rows].values,
                        row_labels=rows,
                        column_labels=columns,
                        height=750,
                        width=1400,
                        center_values=False,
                        color_map= colorMap
                    )
    fig1.update_layout(showlegend=False)


    df['RackNo'] = df['rack_no'].apply(str)
    fig2 = px.box(df, 
                 x="RackNo",
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
    # minmax_gap = str(sum_df['soh'].max() - sum_df['soh'].min())
    sum_df['rack_color'] = sum_df['rack_no']
    sum_df['rack_no'] = sum_df['rack_no'].apply(str)

    # fig3 =  px.line(sum_df, 
    #                 x = 'rack_no',
    #                 y = 'soh', 
    #                 title='Rack Sums & Max Gap [ ' + minmax_gap + ' ]',
    #                 labels={"rack_no": "Rack","soh": "SOH Sums"},
    #                 text=sum_df['minmax']  
    #                 ) 
    # fig3.add_scatter(x=sum_df['rack_no'], 
    #                  y=sum_df['soh'], 
    #                  mode='markers', 
    #                  marker_color=sum_df['rack_color'], 
    #                  marker_size=15)

    
    # min_y = min(sum_df['soh'])-5
    # max_y = max(sum_df['soh'])+5
    # fig3 = px.histogram(sum_df, x="rack_no", y="soh")
    # fig3.update_layout(yaxis=dict(range=[min_y,max_y]))
    # fig3.update_layout(hovermode="closest")
    # fig3.update_layout(showlegend=False)
    # fig3.update_layout(height=450)

    colList = ['cyc_date','bank_no','rack_no','module_no','cell_no','soh','q_a','q_u','cur_avg','n','u_vol','o_vol','gap']
    good_df = df[colList].sort_values(by='soh', ascending=False).iloc[0:50,]
    bad_df  = df[colList].sort_values(by='soh', ascending=True ).iloc[0:50,]
    good_df['seq'] = range(1,51)
    bad_df['seq'] = range(1,51)

    if n_clicks is not None:
        n_upper_soh = None
        n_lower_soh = None

    if n_upper_soh is None:
        good_line = good_df['soh'].iloc[49]
    else :
        good_line = n_upper_soh

    if n_lower_soh is None:
        bad_line  = bad_df['soh'].iloc[49]
    else :
        bad_line = n_lower_soh

    

    df4 = df[['soh']].sort_values(by='soh', ascending=True)
    df4['idx'] = range(1,len(df4)+1)
    stand_df = stand_df[['soh']].sort_values(by='soh', ascending=True)
    stand_df['idx'] = range(1,len(stand_df)+1)

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
                        mode='markers',
                        x=df4['idx'],
                        y=df4['soh'],
                        opacity=0.5,
                        marker=dict(
                            color='MediumPurple',
                            size=12,
                            line=dict(color='MediumPurple',width=0)
                        ),
                        name=s_date
                    )
                )
    fig4.add_trace(go.Scatter(x=stand_df['idx'],
                              y=stand_df['soh'], 
                              mode='markers',
                              marker=dict(
                                            color='red',
                                            size=3,
                                            line=dict(color='yellow',width=0)
                                        ),
                              name=stand_date
                              )
                              
                   )
    fig4.add_hline(y=good_line , line_width=2, line_dash="dash", line_color="red")
    fig4.add_hline(y=bad_line, line_width=2, line_dash="dash", line_color="red")
    fig4.update_layout(showlegend=True)
    fig4.update_layout(height=460)

    hist_data = [df.soh.values , stand_df.soh.values]
    group_labels = [s_date, stand_date] # name of the dataset
    fig5 = ff.create_distplot(hist_data, group_labels, bin_size=.05, show_hist=False, show_rug=False)
    fig5 = fig5.add_vline(x=bad_line,  line_width=2, line_dash="dash", line_color="red" )
    fig5 = fig5.add_vline(x=good_line, line_width=2, line_dash="dash", line_color="red" )
    fig5.update_layout(height=460)     

    rtn_good_df = good_df.to_json(date_format='iso',orient='split')
    rtn_bad_df  = bad_df.to_json(date_format='iso',orient='split')
    rtn_sum_df  = sum_df.to_json(date_format='iso',orient='split')

    return fig1 , fig2 , fig4, fig5, rtn_good_df, rtn_bad_df, rtn_sum_df,  good_line, bad_line




######################################################################################
## Render Plot 21
######################################################################################
@app.callback(Output('cellsoh_plot_23'           , 'figure'  ),
              Input('rdo_cellsoh_tab2_plot_type' , 'value'   ),
              Input('ds_cellsoh_plot23_df'       , 'data'    )
              )
def cb_cellsoh_plot21_render(plot_type,data):
    if plot_type is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate

    sum_df = pd.read_json(data, orient='split') 
    sum_df['rack_no']    = sum_df['rack_no'].apply(str)
    # sum_df['rack_color'] = sum_df['rack_color'].apply(str)

    if plot_type == "B":
        min_y = min(sum_df['soh'])-5
        max_y = max(sum_df['soh'])+5
        fig = px.histogram(sum_df, x="rack_no", y="soh", color="rack_color")
        fig.update_layout(yaxis=dict(range=[min_y,max_y]))
    else:
        minmax_gap = str(sum_df['soh'].max() - sum_df['soh'].min())
        fig =  px.line(sum_df, 
                        x = 'rack_no',
                        y = 'soh', 
                        title='Rack Sums & Max Gap [ ' + minmax_gap + ' ]',
                        labels={"rack_no": "Rack","soh": "SOH Sums"},
                        text=sum_df['minmax']  
                        ) 
        fig.add_scatter(x=sum_df['rack_no'], 
                        y=sum_df['soh'], 
                        mode='markers', 
                        marker_color=sum_df['rack_color'], 
                        marker_size=15)
    
    fig.update_layout(hovermode="closest")
    fig.update_layout(showlegend=False)
    fig.update_layout(height=450)

    return fig




@app.callback(Output("cellsoh_modal_1"           , "is_open"),
              Output("cellsoh_DT_1"              , "children"),
              Input("btn_cellsoh_viewdata"       , "n_clicks"),
              State("cellsoh_modal_1"            , "is_open"),
              State("cellsoh_plot_1"             , "selectedData")
              )
def cb_cellsoh_toggle_modal(n_clicks,is_open, selectedData):
    if n_clicks is None :
        raise PreventUpdate

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
                    style_table={'height': '400px',  'overflowY': 'auto', 'overflowX': 'auto'},
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






@app.callback(Output("cellsoh_modal_2"           , "is_open"),
              Output("cellsoh_DT_2"              , "children"),
              Input("btn_cellsoh_detail_dataview", "n_clicks"),
              State("cellsoh_modal_2"            , "is_open"),
              State("cellsoh_plot_2"             , "selectedData"),
              )
def cb_cellsoh_toggle_modal(n_clicks, is_open, selectedData):
    if n_clicks is None :
        raise PreventUpdate
    
    if selectedData is not None and  len(selectedData['points']) > 0 :
        df = pd.DataFrame(selectedData['points'])
        ddata = df[['x','y']]
        cdata = pd.DataFrame(df['customdata'].tolist())
        data = pd.concat([ddata,cdata],axis=1)
        data = data.rename(columns={'x': 'cyc_date', 'y': 'soh', 0:'type', 1:'rack_no'})
        data = data[['cyc_date','type', 'rack_no', 'soh']]
        data = data.to_dict('rows')
    else:
        data = None


    cellsoh_DT2_columns = [
                            dict(id='type'    , name='Type' , type='text'), 
                            dict(id='cyc_date', name='Date' , type='text'), 
                            dict(id='rack_no' , name='Rack' , type='text'), 
                            dict(id='soh'     , name='SOH'  , type='numeric'), 
                        ]

    cellsoh_DataTable_2 = dash_table.DataTable(
                    data=data,
                    columns = cellsoh_DT2_columns,
                    editable=False,
                    style_table={'height': '400px', 'overflowY': 'auto', 'overflowX': 'auto'},
                    style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                    column_selectable="single",
                    selected_rows=[],
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    style_cell_conditional=[
                        { 'if': {'column_id': 'type'      }, 'textAlign': 'left'  }, 
                        { 'if': {'column_id': 'cyc_date'  }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
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

    return not is_open, cellsoh_DataTable_2





@app.callback(Output("div_cellsoh_select_date"  , "children"),
              Output("cbo_cellsoh_detail_rack"  , "value") ,
              Output("cbo_cellsoh_detail_module", "value") ,
              Output("cbo_cellsoh_detail_cell"  , "value") ,
              Output("dtp_cellsoh_detail_date"  , "date" ) ,
              Input("cellsoh_plot_1"            , "clickData"))
def cb_cellsoh_click_date(clickData):
    if clickData is None:
        raise PreventUpdate
    
    selectRack   = None
    selectModule = None
    selectCell   = None
    returnDate   = None
    if len(clickData)>0:
        df =  pd.DataFrame(clickData['points'])
        if len(df)>0:
            selectDate = df['x'][0] #첫번째 포인트의 일자
            
            selectRack   = df['customdata'][0][1]
            selectModule = df['customdata'][0][2]
            selectCell   = df['customdata'][0][3]

            selectDate = selectDate[0:4] + "-" + selectDate[4:6] + "-" + selectDate[6:8]
            returnDate = datetime.strptime(selectDate, '%Y-%m-%d').date()
            selectDate = "Selected Date : " + selectDate

        else:
            selectDate = "Selected Date : ____-__-__"    
    else:
        selectDate = "Selected Date : ____-__-__"
    
    return selectDate, selectRack, selectModule, selectCell, returnDate


 
#------------ Good Cell View -----------------------------------------------------
@app.callback(Output("cellsoh_modal_3"           , "is_open"  ),
              Output("cellsoh_DT_3"              , "children" ),
              Input("btn_cellsoh_good"           , "n_clicks" ),
              State("cellsoh_modal_3"            , "is_open"  ),
              State('ds_cellsoh_good_df'         , 'data'     )
              )
def cb_cellsoh_view_good_modal(n_clicks, is_open, ds_data):
    if n_clicks is None :
        raise PreventUpdate

    if ds_data is None :
        data = None
        dt_style = {'height': '50px','overflowY': 'auto', 'overflowX': 'auto'}
    else:
        data = pd.read_json(ds_data, orient='split').to_dict('rows')
        dt_style = {'height': '800px','overflowY': 'auto', 'overflowX': 'auto'}

    cellsoh_DT3_columns = [
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

    cellsoh_DataTable_3 = dash_table.DataTable(
                    data=data,
                    columns = cellsoh_DT3_columns,
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

    return not is_open , cellsoh_DataTable_3

 
#------------ Bad Cell View -----------------------------------------------------
@app.callback(Output("cellsoh_modal_4"    , "is_open"  ),
              Output("cellsoh_DT_4"       , "children" ),
              Input("btn_cellsoh_bad"     , "n_clicks" ),
              State("cellsoh_modal_4"     , "is_open"  ),
              State('ds_cellsoh_bad_df'   , 'data'     )
              )
def cb_cellsoh_view_good_modal(n_clicks, is_open, ds_data):
    if n_clicks is None :
        raise PreventUpdate

    if ds_data is None :
        data = None
        dt_style = {'height': '50px','overflowY': 'auto', 'overflowX': 'auto'}
    else:
        data = pd.read_json(ds_data, orient='split').to_dict('rows')
        dt_style = {'height': '800px','overflowY': 'auto', 'overflowX': 'auto'}

    cellsoh_DT4_columns = [
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

    cellsoh_DataTable_4 = dash_table.DataTable(
                    data=data,
                    columns = cellsoh_DT4_columns,
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

    return not is_open, cellsoh_DataTable_4