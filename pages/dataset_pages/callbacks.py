from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import io

import pandas as pd
import plotly.io as pio
import plotly.express as px
import time
import plotly.graph_objs as go
import json
import dash as html
import dash_table
import pickle

from utils.server_function import *
from pages.dash_pages.model import *
from pages.dataset_pages.model import *
 

@app.callback(Output('ds_dataset_original_df'    , 'data'      ),
              Output('dataset_loading_output1'   , 'children'  ),
              Output("dataset_alert"             , "is_open"   ),
              Input('btn_dataset_dataload'       , 'n_clicks'  ),
              State('date_range_dataset'         , 'start_date'),
              State('date_range_dataset'         , 'end_date'  ),
              State('rdo_dataset_datatype'       , 'value'     ),
              State('cbo_dataset_bank'           , 'value'     ), 
              State('cbo_dataset_rack'           , 'value'     ),
              State('cbo_dataset_module'         , 'value'     ),
              State('cbo_dataset_cell'           , 'value'     ) 
              )
def cb_dataset_data_load(n_clicks, sStartDate, sEndDate, sDataType, sBankNo, sRackNo, sModuleNo, sCellNo):
    if n_clicks is None:
        raise PreventUpdate
    if sDataType is None:
        raise PreventUpdate    
    if sBankNo is None:
        raise PreventUpdate

    # (sDataType, sDate, eDate, sBankNo, sRackNo, sModuleNo, sCellNo)?
    data = dataset_load_data(sDataType, sStartDate, sEndDate, sBankNo, sRackNo, sModuleNo, sCellNo)

    popup_sw = False
    if data is None or len(data) == 0:
        popup_sw = True

    if data is None:
        return None, '', popup_sw
    else:    
        return data.to_json(date_format='iso' , orient='split')  ,'', popup_sw
    



@app.callback(Output('div_dataset_datainfo'    , 'children' ),
              Output('div_dataset_datasummary' , 'children' ),
              Output('dataset_DT'              , 'data'     ),
              Input('btn_dataset_datainfo'     , 'n_clicks' ) ,
              State('ds_dataset_original_df'   , 'data'     ) 
              )
def cb_dataset_data_info(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    
    buf = io.StringIO()
    data = pd.read_json(data, orient='split')
    data.info(buf=buf)
    strResult = buf.getvalue()

    summary_df = str(data.describe())
    
    c_list = data.columns.values.tolist()
    col_list = pd.DataFrame({'column':c_list})

    return strResult, summary_df, col_list.to_dict('rows')
  
 

@app.callback(
    Output('ds_dataset_df'        , 'data'    ),
    Input('btn_dataset_set_data'  , 'n_clicks'),
    State('dataset_DT'            , 'derived_virtual_selected_rows'),
    State('ds_dataset_original_df', 'data'     ) )
def cb_dataset_set_data(n_clicks, selected_columns, data):
    if n_clicks is None:
        raise PreventUpdate
    if selected_columns is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate

    selected_columns_list = set(selected_columns or [])
    data = pd.read_json(data, orient='split')
    data = data.iloc[:,list(selected_columns_list)]

    return data.to_json(date_format='iso' , orient='split') 







@app.callback(Output('dataset_DT_2'        , 'children' ),
              Input('rdo_dataset_dataview' , 'value'),
              Input('ds_dataset_df'        , 'modified_timestamp'),
              State('ds_dataset_df'        , 'data'))
def cb_dataset_DT_2(data_view_type ,ts, data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate    
    if data_view_type is None:
        raise PreventUpdate

    data = pd.read_json(data, orient='split')

    columns = [{"name": i, "id": i, } for i in data.columns]

    if (data_view_type == "H"):
        df_data = data.head(30).to_dict('rows')
    elif (data_view_type == "T"):
        df_data = data.tail(30).to_dict('rows')
    else:
        df_data = data.head(30).to_dict('rows')

    dataset_DataTable_2 = dash_table.DataTable(
                    data=df_data,
                    columns = columns,
                    editable=False,
                    style_table={'height': '500px', 'overflowY': 'auto', 'overflowX': 'auto'},
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
                    style_data_conditional=[
                        {
                            'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
                            # data_bars(dataTable_column, 'ChargeQ')  +
                            # data_bars(dataTable_column, 'Voltage'),
                        },
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

    return dataset_DataTable_2
  





@app.callback(Output('dataset_DT_Train'      , 'children' ),
              Output('dataset_DT_Test'       , 'children' ),
              Output('ds_train_test_file'    , 'data' ),
              Output('dataset_DT_3'          , 'children' ),
              Output('dataset_DT_4'          , 'children' ),
              Input('btn_dataset_split_data' , 'n_clicks'),
              State('ds_dataset_df'          , 'data'))
def cb_dataset_DT_2(n_clicks , data ):
    if n_clicks is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate    

    data = pd.read_json(data, orient='split')

    train_df = data.sample(frac=0.7, random_state=200) #random state is a seed value
    test_df  = data.drop(train_df.index)

    train_file_name = 'tmp_train.pkl'
    test_file_name  = 'tmp_test.pkl'

    train_str = str(len(train_df)) + '/' + train_file_name
    test_str  = str(len(test_df))  + '/' + test_file_name

    train_df.to_pickle('./data/'+ train_file_name)
    test_df.to_pickle('./data/' + test_file_name)

    file_data = {'train':[train_file_name], 'test':[test_file_name]}
    f_data = pd.DataFrame(file_data) 
    
    
    
    columns = [{"name": i, "id": i, } for i in train_df.columns]
    train_df = train_df.head(30).to_dict('rows')
    dataset_DataTable_3 = dash_table.DataTable(
                    data=train_df,
                    columns = columns,
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
                    style_data_conditional=[
                        {
                            'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
                            # data_bars(dataTable_column, 'ChargeQ')  +
                            # data_bars(dataTable_column, 'Voltage'),
                        },
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
    
    columns4 = [{"name": i, "id": i, } for i in test_df.columns]
    test_df = test_df.head(30).to_dict('rows')
    dataset_DataTable_4 = dash_table.DataTable(
                    data=test_df,
                    columns = columns4,
                    editable=False,
                    style_table={'height': '400px','overflowY': 'auto', 'overflowX': 'auto'},
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
                    style_data_conditional=[
                        {
                            'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
                            # data_bars(dataTable_column, 'ChargeQ')  +
                            # data_bars(dataTable_column, 'Voltage'),
                        },
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
    
    return train_str, test_str ,f_data.to_json(date_format='iso' , orient='split') , dataset_DataTable_3 , dataset_DataTable_4
  
  
  
  
@app.callback(
    Output("dataset_modal_data"  , "is_open"),
    Input("btn_dataset_data_view", "n_clicks"),
    State("dataset_modal_data", "is_open"),
)
def cb_dataset_toggle_modal(n, is_open):
    if n:
        return not is_open
        
    return is_open