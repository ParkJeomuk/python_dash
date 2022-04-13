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
              State('ds_aging_df'        , 'data'     ),
              Input('rdo_aging_heatmaptype'  , 'value'      ),
              Input('rdo_aging_heatmap_color', 'value'      ),
              Input('rdo_aging_plottype'     , 'value'      )
              )
def cb_cellsoh_plot1_render( ts, data, s_data_type, s_color_type, s_plot_type):
    if ts is None or data is None:
        fig =  blank_fig() 
        return fig, fig, fig, fig, None, None


    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)

    # data['rack_no'] = data['rack_no'].apply(str)
    # data['module_no'] = data['module_no'].apply(str)
    # data['cell_no'] = data['cell_no'].apply(str)
    data['soh_gap'] = data.soh_x.values - data.soh_y.values
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig , fig , fig, fig , None, None
    
    if s_data_type == "C":
        tmp_df = data[['rack_no','cell_no','soh_gap']].pivot('cell_no','rack_no','soh_gap')
    else:    
        tmp_df = data[['rack_no','module_no','soh_gap']].groupby(['rack_no','module_no'],as_index=False).mean()
        tmp_df = tmp_df[['rack_no','module_no','soh_gap']].pivot('module_no','rack_no','soh_gap')



    if s_plot_type == 'H':
        if s_color_type == 'D':
            revers_col = True
        else:
            revers_col = False

        z = tmp_df.values.tolist()
        x = tmp_df.columns.tolist()
        y = tmp_df.index.tolist()

        fig1 = go.Figure(data=go.Heatmap(
                z=z,
                x=x,
                y=y,
                colorscale='hot',
                reversescale=revers_col))
        fig1.update_layout(height=870)        
    else:
        if s_color_type == 'D':
            colorMap =  [[0.0,'#FEFDFB'],[0.5, '#FCD82D'],[1,'#921205']]
        else:    
            colorMap =  [[0.0,'#921205'],[0.5, '#FCD82D'],[1,'#FEFDFB']]

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
                  hover_data=["rack_no","module_no","cell_no"],
                  labels={"soh_gap": "SOH Gap"}
                 )
    fig2.update_layout(showlegend=False)

    colList = ['rack_no','module_no','cell_no', 'soh_gap']
    ds_colList = ['rack_no','module_no','cell_no','soh','q_a','q_u','cur_avg','n','u_vol','o_vol','gap','soh_gap']
    good_df = data.sort_values(by='soh_gap', ascending=False).iloc[0:25,]
    good_df.rename(columns = {'soh_x':'soh','q_a_x':'q_a','q_u_x':'q_u',
                              'cur_avg_x':'cur_avg','n_x':'n','u_vol_x':'u_vol',
                              'o_vol_x':'o_vol','gap_x':'gap'} , inplace = True)
    good_df = good_df[ds_colList]
    r_t_df  = good_df.to_json(date_format='iso',orient='split')
    good_df = good_df[colList]


    bad_df  = data.sort_values(by='soh_gap', ascending=True ).iloc[0:25,]
    bad_df.rename(columns = {'soh_x':'soh','q_a_x':'q_a','q_u_x':'q_u',
                             'cur_avg_x':'cur_avg','n_x':'n','u_vol_x':'u_vol',
                             'o_vol_x':'o_vol','gap_x':'gap'} , inplace = True)
    bad_df  = bad_df[ds_colList]
    r_b_df  = bad_df.to_json(date_format='iso',orient='split')
    bad_df  = bad_df[colList]

    good_df['seq'] = range(1,26)
    bad_df['seq'] = range(1,26)
    
    # good_df['text'] = good_df['rack_no'] + ":" + good_df['cell_no'] + ":" + round(good_df['soh_gap'],4).apply(str)
    # bad_df['text']  = bad_df['rack_no']  + ":" + bad_df['cell_no']  + ":" + round(bad_df['soh_gap'],4).apply(str)


    fig3 = px.scatter(good_df, 
                      x="seq", 
                      y="soh_gap",
                      hover_data=["rack_no","module_no","cell_no"],
                      labels={"seq": "Seq","soh_gap": "SOH Gap"}
                      )
    


    fig4 = px.scatter(bad_df, 
                      x="seq", 
                      y="soh_gap",
                      hover_data=["rack_no","module_no","cell_no"],
                      labels={"seq": "Seq","soh_gap": "SOH Gap"}
                    #   , 
                    #   text='text'
                      )
    # fig4.update(mode='markers+lines')

    return fig1, fig2, fig3, fig4, r_t_df, r_b_df







#------------ Top 25 View -----------------------------------------------------
@app.callback(Output("aging_modal_1"       , "is_open"  ),
              Output("aging_DT_1"          , "children" ),
              Input("btn_aging_top25_data" , "n_clicks" ),
              State("aging_modal_1"        , "is_open"  ),
              State('ds_aging_top25'       , 'data'     ) )
def cb_aging_good_modal(n_clicks, is_open, ds_data):
    if n_clicks is None :
        raise PreventUpdate

    if ds_data is None :
        data = None
        dt_style = {'height': '50px','overflowY': 'auto', 'overflowX': 'auto'}
    else:
        data = pd.read_json(ds_data, orient='split').to_dict('rows')
        dt_style = {'height': '600px','overflowY': 'auto', 'overflowX': 'auto'}

    aging_DT1_columns = [
                            dict(id='rack_no'  , name='Rack'         , type='text'), 
                            dict(id='module_no', name='Module'       , type='text'), 
                            dict(id='cell_no'  , name='Cell'         , type='text'), 
                            dict(id='soh'      , name='SOH'          , type='numeric'), 
                            dict(id='q_a'      , name='Q A'          , type='numeric'), 
                            dict(id='q_u'      , name='Q U'          , type='numeric'), 
                            dict(id='cur_avg'  , name='Current Avg'  , type='numeric'), 
                            dict(id='n'        , name='N'            , type='numeric'), 
                            dict(id='u_vol'    , name='U Vol'        , type='numeric'), 
                            dict(id='o_vol'    , name='O Vol'        , type='numeric'), 
                            dict(id='gap'      , name='Gap'          , type='numeric'), 
                            dict(id='soh_gap'  , name='SOH Gap'      , type='numeric'), 
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

 

#------------ Bottom 25 View -----------------------------------------------------
@app.callback(Output("aging_modal_2"          , "is_open"  ),
              Output("aging_DT_2"             , "children" ),
              Input("btn_aging_bottom25_data" , "n_clicks" ),
              State("aging_modal_2"           , "is_open"  ),
              State('ds_aging_bottom25'       , 'data'     )  )
def cb_aging_bad_modal(n_clicks, is_open, ds_data):
    if n_clicks is None :
        raise PreventUpdate

    if ds_data is None :
        data = None
        dt_style = {'height': '50px','overflowY': 'auto', 'overflowX': 'auto'}
    else:
        data = pd.read_json(ds_data, orient='split').to_dict('rows')
        dt_style = {'height': '600px','overflowY': 'auto', 'overflowX': 'auto'}

    aging_DT2_columns = [
                            dict(id='rack_no'  , name='Rack'         , type='text'), 
                            dict(id='module_no', name='Module'       , type='text'), 
                            dict(id='cell_no'  , name='Cell'         , type='text'), 
                            dict(id='soh'      , name='SOH'          , type='numeric'), 
                            dict(id='q_a'      , name='Q A'          , type='numeric'), 
                            dict(id='q_u'      , name='Q U'          , type='numeric'), 
                            dict(id='cur_avg'  , name='Current Avg'  , type='numeric'), 
                            dict(id='n'        , name='N'            , type='numeric'), 
                            dict(id='u_vol'    , name='U Vol'        , type='numeric'), 
                            dict(id='o_vol'    , name='O Vol'        , type='numeric'), 
                            dict(id='gap'      , name='Gap'          , type='numeric'), 
                            dict(id='soh_gap'  , name='SOH Gap'      , type='numeric'), 
                        ]

    aging_DataTable_2 = dash_table.DataTable(
                    data=data,
                    columns = aging_DT2_columns,
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

    return not is_open , aging_DataTable_2




@app.callback(Output("aging_modal_3"           , "is_open" ),
              Output("aging_DT_3"              , "children"),
              Input("btn_aging_outlier_data"   , "n_clicks"),
              State("aging_modal_3"            , "is_open" ),
              State("aging_plot_2"             , "selectedData")
              )
def cb_aging_toggle_outlier_modal(n_clicks,is_open, selectedData):
    if n_clicks is None :
        raise PreventUpdate

    if len(selectedData['points']) > 0 :
        df = pd.DataFrame(selectedData['points'])
        ddata = df[['y']]
        cdata = pd.DataFrame(df['customdata'].tolist())
        data = pd.concat([ddata,cdata],axis=1)
        data = data.rename(columns={'y': 'soh_gap', 0:'rack_no', 1:'module_no', 2:'cell_no'})
        data = data[['rack_no','module_no', 'cell_no', 'soh_gap']]
        data = data.to_dict('rows')
    else:
        data = None

    aging_DT3_columns = [
                            dict(id='rack_no'   , name='Rack'    , type='text'), 
                            dict(id='module_no' , name='Module'  , type='text'), 
                            dict(id='cell_no'   , name='Cell'    , type='text'), 
                            dict(id='soh_gap'   , name='SOH Gap' , type='numeric'), 
                        ]

    aging_DataTable_3 = dash_table.DataTable(
                    data=data,
                    columns = aging_DT3_columns,
                    editable=False,
                    style_table={'height': '400px',  'overflowY': 'auto', 'overflowX': 'auto'},
                    style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
                    column_selectable="single",
                    selected_rows=[],
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    style_cell_conditional=[
                        { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'module_no' }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'cell_no'   }, 'textAlign': 'center'},
                        { 'if': {'column_id': 'soh_gap'   }, 'textAlign': 'right' },
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

    return not is_open, aging_DataTable_3




@app.callback(Output('aging_plot_5'         , 'figure'   ),
              Input('aging_plot_1'          , 'clickData'),
              State('dtp_aging_date_1'      , 'date'     ), 
              State('dtp_aging_date_2'      , 'date'     ), 
              State('cbo_cellsoh_bank'      , 'value'    ),
              State('rdo_aging_heatmaptype' , 'value'    ),
              State('rdo_aging_plottype'    , 'value'    )
              
             )
def aging_plot1_click(clickData, sDate, eDate, sBankNo, sDataType, sPlotType):
    if clickData is None :
        raise PreventUpdate

    # Clustergrame일 경우 현재  x,y 값이 안돼는 문제.... 
    if sPlotType == 'C': 
        fig =  blank_fig()
        return fig 

    x = clickData['points'][0]['x']
    y = clickData['points'][0]['y']
    
    if sDataType == "C":
        sRackNo = x 
        sModuleNo = 0
        sCellNo = y
    else:
        sRackNo = x 
        sModuleNo = y
        sCellNo = 0

    df = aging_data_load(sDate, eDate, sDataType, sBankNo, sRackNo, sModuleNo, sCellNo) 
    df = df.sort_values(["cell_no","cyc_date"],   ascending = True )
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    soh_diff = df.groupby('cell_no')['soh'].diff().fillna(0)
    df['gap_trend'] = soh_diff


    if df is None:
        fig =  blank_fig()
        return fig 

    fig = px.line(df, 
                  x = 'cyc_date',
                  y = 'gap_trend', 
                  color = 'cell_no',
                  line_group='cell_no',
                  title = 'Cell SOH Gap Trend'
                  )    

    fig.update_traces(mode="markers+lines")   
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(height=260)        
    return fig 

