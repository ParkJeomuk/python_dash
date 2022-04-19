from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date,timedelta,datetime
from dash import dash_table


import dash_bio as dashbio
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import time
import json
import dash as html
import pickle
import re
import numpy as np
import statsmodels.api as sm
from math import dist
from sklearn.metrics.pairwise import euclidean_distances
from scipy.cluster.hierarchy import dendrogram, linkage, cut_tree 
# from pyearth import Earth

from utils.server_function import *
from utils.constants  import *
from pages.trend_pages.model import *



def uf_trend_minmax_calc (data):
    if data is None:
        raise PreventUpdate
    
    cols = ['cyc_date','min_rack','max_rack','min_soh','max_soh','gap','n']
    df = pd.DataFrame(columns = cols)

    for cyc_date, group_data in data[['cyc_date','rack_no','soh']].groupby('cyc_date'):
        tdf = group_data.groupby(['cyc_date','rack_no']).sum()
        soh_lst = tdf.soh.values.tolist()
        min_idx = soh_lst.index(min(soh_lst))
        max_idx = soh_lst.index(max(soh_lst))
        min_soh = min(soh_lst)
        max_soh = max(soh_lst)
        gap_soh = max_soh - min_soh
        # if cyc_date == '20200527':
        #     dist_df = None
        dist_df = euclidean_distances(tdf[['soh']].reset_index(drop=True))
        linked = linkage(dist_df, 'single')
        n = len(pd.DataFrame(cut_tree(linked,height=3)).value_counts())

        df = df.append( {'cyc_date':cyc_date, 'min_rack':min_idx,'max_rack':max_idx,'min_soh':min_soh,'max_soh':max_soh,'gap':gap_soh, 'n':n },ignore_index=True )
        df = df.loc[df["min_rack"]>0] # 데이타가 NA일 경우 0으로 처리되어 제외 처리
    return df



@app.callback(Output('ds_trend_df'        , 'data'      ),
              Output('ds_trend_data'      , 'data'      ),
              Output('loading_trend_1'    , 'children'  ),
              Input('btn_trend_dataload'  , 'n_clicks'  ),
              State('date_range_trend'    , 'start_date'), 
              State('date_range_trend'    , 'end_date'  ), 
              State('cbo_trend_bank'      , 'value'     ) 
              )
def cb_trend_data_load(n_clicks, s_date, e_date , s_bank_no ):
    if n_clicks is None:
        raise PreventUpdate
    if s_date is None:
        uf_show_msg("Start Date을 입력하세요!")
        raise PreventUpdate
    if e_date is None:
        uf_show_msg("End Date을 입력하세요!")
        raise PreventUpdate
    if s_bank_no is None or s_bank_no == '':
        uf_show_msg("Bank를 선택하세요!")
        raise PreventUpdate
    
    data = trend_data_load(s_date, e_date, s_bank_no)

    df = uf_trend_minmax_calc(data)

    return df.to_json(date_format='iso',orient='split') ,data.to_json(date_format='iso',orient='split'),''



 


######################################################################################
## Render Plot 1
######################################################################################
@app.callback(Output('trend_plot_1' , 'figure'   ),
              Output('trend_plot_2' , 'figure'   ), 
              Input('ds_trend_df'   , 'modified_timestamp'),
              State('ds_trend_df'   , 'data'     )
              )
def cb_trend_plot1_render( ts, data):
    if ts is None or data is None:
        raise PreventUpdate


    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None or len(data)<1:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig , fig  

    data['cyc_date'] = pd.to_datetime(data['cyc_date'], format='%Y%m%d')

    # lowess = sm.nonparametric.lowess
    # y_hat1 = lowess(data['cyc_date'], data['gap'])

    fig1 = px.scatter(data, 
                      x="cyc_date", 
                      y="gap", 
                      title='SOH Gap(Risk1) Trend',
                      trendline="lowess",
                      trendline_color_override="red")
    
    fig1.update_traces(mode='lines+markers')
    
    fig1.update_layout(hovermode="closest")
    fig1.update_layout(showlegend=False)
    fig1.update_layout(yaxis_range=[3,7])
    fig1.update_layout(height=480)



    fig2 = px.scatter(data, 
                      x="cyc_date", 
                      y="n", 
                      title='Rack Clustering by SOH(h=3)')
    
    fig2.update_traces(marker={'size': 12})  
    fig2.update_traces(mode='lines+markers')
    fig2.update_layout(hovermode="closest")
    fig2.update_layout(showlegend=False)
    fig2.update_layout(height=480)

    return fig1 , fig2


 



 
@app.callback(Output("trend_plot_3"  , "figure"),
              Output("div_trend_select_date"  , "children"),
              Input("trend_plot_1"   , "clickData"),
              Input("trend_plot_2"   , "clickData"),
              State("ds_trend_data"  , "data"))
def cb_trend_click_date(plot1_clickData, plot2_clickData, data):
    if plot1_clickData is None and plot2_clickData is None:
        raise PreventUpdate
    
    if data is None:
        raise PreventUpdate

    selectDate = ""    

    if plot1_clickData is not None and len(plot1_clickData)>0:
        df =  pd.DataFrame(plot1_clickData['points'])
        if len(df)>0:
            selectDate = df['x'][0] 
    
    if plot2_clickData is not None and len(plot2_clickData)>0:
        df =  pd.DataFrame(plot2_clickData['points'])
        if len(df)>0:
            selectDate = df['x'][0] 


    if selectDate == "" or len(data)<1:
        fig =  blank_fig()
        return fig 

    data = pd.read_json(data, orient='split')
    data['cyc_date'] = data['cyc_date'].apply(str)

    data = data[data['cyc_date'] == selectDate.replace('-','')]

    div_selectDate = "Dendrograme  Date : " + selectDate

    tdf = data[['rack_no','soh']].groupby('rack_no').sum()
    dist_df = euclidean_distances(tdf[['soh']].reset_index(drop=True))

    # linked = linkage(dist_df, 'single')    
    fig = ff.create_dendrogram(dist_df, 
                           orientation='bottom',
                           linkagefun=lambda x: linkage(x, 'single'),)

    return fig , div_selectDate

