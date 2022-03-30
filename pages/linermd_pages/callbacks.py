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
from pages.linermd_pages.model import *


n_linerdm_mae = 0
n_linerdm_mse = 0
n_linerdm_rmse = 0



@app.callback(Output('linerdm_predict_filname' , 'children'),
              Input('btn_linerdm_model_file', 'n_clicks') )
def cb_linerdm_file_open(n_clicks  ):
    if n_clicks is None:
        raise PreventUpdate 

    global gTestFilePath

    root = Tk()
    root.withdraw()
    # root.iconbitmap(default='Extras/transparent.ico')

    filename = filedialog.askopenfilename(initialdir='/')
    gTestFilePath = filename
    print('***', filename)

    root.destroy()  # <--- SOLUTION

    return filename






@app.callback(Output('ds_linerdm_train_data'     , 'data'      ),
              Output('ds_linerdm_test_data'      , 'data'      ),
              Output("cbo_linerdm_x"             , "options"   ),
              Output("cbo_linerdm_y"             , "options"   ),
              Output("linerdm_loading_output1"   , "children"  ),
              Input('btn_linerdm_dataload'       , 'n_clicks'  ),
              State('ds_train_test_file'         , 'data'      ) 
              )
def cb_linerdm_data_load(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    # if data is None:
    #     raise PreventUpdate    

    # data = pd.read_json(data, orient='split')

    # train_data = linerdm_load_train_data(DATA_PATH+data['train'].iloc[0] )
    # test_data  = linerdm_load_train_data(DATA_PATH+data['test'].iloc[0] )
    train_data = linerdm_load_train_data(DATA_PATH+'tmp_train.pkl' )
    test_data  = linerdm_load_train_data(DATA_PATH+'tmp_test.pkl' )

    col_df = pd.DataFrame({'code':pd.DataFrame(train_data.columns).iloc[:,0]})

    opt = [{'label': col, 'value': col} for col in train_data.columns]
    # opt = [{"label": col, "value": col}] for col in col_df.code
    

    return train_data.to_json(date_format='iso',orient='split')  ,test_data.to_json(date_format='iso',orient='split') ,  opt ,  opt ,''







@app.callback(Output('div_linerdm_datainfo', 'children' ),
              Input('ds_linerdm_train_data'  , 'modified_timestamp'),
              State('ds_linerdm_train_data'  , 'data'))
def cb_linerdm_data_info(ts, data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate    

    buf = io.StringIO()
    data = pd.read_json(data, orient='split')
    data.info(buf=buf)
    strResult = buf.getvalue()
  
    return strResult


######################################################################################
## Model Save
######################################################################################
@app.callback(Output('linderdm_div_save_model_name', 'children' ),
              Output("cbo_linerdm_model_choice" , "options" ), 
              Input('btn_linerdm_model_save'    , 'n_clicks'),
              State('ds_linerdm_train_data'     , 'data'),
              State('cbo_linerdm_x'             , 'value'   ),
              State('cbo_linerdm_y'             , 'value'   )
              )
def cb_linerdm_data_info(ts, data, x_var, y_var ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate    

    md_file = './model/lm_model.sav'
    loaded_model = pickle.load(open(md_file  , 'rb'))
    

    sFileName = "lm_model_" + str(date.today()) + ".sav"
    pickle.dump(loaded_model, open('./model/'+sFileName, 'wb'))

    global n_linerdm_mae
    global n_linerdm_mse
    global n_linerdm_rmse

    dModel = {'md_name': re.sub('.sav','',sFileName), 
              'md_path': './model/', 
              'md_filename': sFileName, 
              'md_x_var': x_var, 
              'md_y_var': y_var, 
              'md_mae'  : n_linerdm_mae ,
              'md_mse'  : n_linerdm_mse ,
              'md_rmse' : n_linerdm_rmse,
              'md_desc' :'desc'}
    
    uf_save_model_list(dModel)

    # #기존 파일 삭제
    # try:
    #   os.remove(md_file)
    # except:
    #     print('Not Exists File')
  
    md_list = os.listdir('./model/')
    opt = [{'label': re.sub('.sav','',col), 'value': re.sub('.sav','',col)} for col in md_list]
    
    return sFileName , opt





######################################################################################
## Model Calc
######################################################################################
@app.callback(Output('linerdm_plot_1'         , 'figure'  ),
              Output('linerdm_plot_2'         , 'figure'  ),
              Output('div_linerdm_model_info' , 'children'),
              Output('linerdm_DT_1'           , 'children'),
              Input('btn_linerdm_model_apply' , 'n_clicks'),
              State('cbo_linerdm_x'           , 'value'   ),
              State('cbo_linerdm_y'           , 'value'   ),
              State('ds_linerdm_train_data'   , 'data'    ),
              State('ds_linerdm_test_data'    , 'data'    )
              )
def cb_linerdm_plot1_render(ts, x_var, y_var, data , test_data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    if test_data is None:
        raise PreventUpdate    
    if x_var is None or x_var=='':
        # uf_set_modal('Error','X Variable Error')
        raise PreventUpdate
    if y_var is None or y_var=='':
        raise PreventUpdate    

    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)
    data = data.sort_values("cyc_date",   ascending = True )
    # data["cyc_date"]   = data["cyc_date"].apply(str)
    
    test_data = pd.read_json(test_data, orient='split')
    test_data = test_data.dropna(axis=0)
    test_data = test_data.sort_values("cyc_date",   ascending = True )

    x_data = data[x_var]
    test_x_data = test_data[x_var]
    if(len(x_data.columns)<2):
       x_data = pd.DataFrame(x_data.values.reshape(-1,1), columns=['cyc_date'])
       test_x_data = test_x_data.values.reshape(-1,1)

    y_data = data[y_var]

    #----- Column Not Number Type  Cast Float Type ----
    x_data = pd.DataFrame(x_data)
    col_type = x_data.dtypes

    for key,value in col_type.items():
        if value != 'int64' and value != 'float64':
            x_data[key] = x_data[key].apply(float)
    #----- Column Not Number Type  Cast Float Type ----

    line_fitter = LinearRegression()
    lm = line_fitter.fit(x_data, y_data)

    data_pred= lm.predict(x_data)
    test_pred = lm.predict(test_x_data)
    
    filename = './model/lm_model.sav'
    pickle.dump(lm, open(filename, 'wb'))
    
    

    compare_data = pd.concat([test_data.reset_index(drop=True), pd.DataFrame(test_pred, columns=['pred']),pd.DataFrame(range(1,len(test_data)+1),columns=['seq'])], axis=1)
    com_data = pd.DataFrame({'cyc_date':compare_data['cyc_date'],'seq':compare_data['seq'], 'value':compare_data[y_var], 'type':'act'}).append(pd.DataFrame({'cyc_date':compare_data['cyc_date'], 'seq':compare_data['seq'], 'value':compare_data['pred'], 'type':'pred'}))

    line_x = pd.DataFrame(x_data).iloc[:,0]
    line_y = pd.DataFrame(data_pred).iloc[:,0]

    nCoef = lm.coef_[0]
    nIntercept = lm.intercept_

    #-----------StatsMOdels --------------------------------------------------------
    if len(x_data.columns) == 1 :
        x_data = x_data.to_numpy()

    result = sm.OLS(y_data, sm.add_constant(x_data)).fit()
    str_fit_result =(result.summary().as_text())

    #----------- Test/Prediction Data Table -----------------------------------------
    columns = [{"name": i, "id": i, } for i in compare_data.columns]

    linerdm_DataTable_1 = dash_table.DataTable(
                    data = compare_data.to_dict('rows'),
                    columns = columns,
                    editable=False,
                    style_table={'height': '450px', 'overflowY': 'auto', 'overflowX': 'auto'},
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
    #----------- Test/Prediction Data Table -----------------------------------------

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    if(x_var[0]=='cyc_date'):
        data["cyc_date"] = data["cyc_date"].apply(str)
        com_data["cyc_date"] = com_data["cyc_date"].apply(str)
        line_x = line_x.apply(str)


    fig = px.scatter(data, x=x_var[0], y=y_var )
    fig.update_traces(marker=dict(size=14, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))

    fig.add_trace(
        go.Scatter(
            x=[line_x.iloc[0],line_x.iloc[len(line_x)-1]],
            y=[line_y.iloc[0],line_y.iloc[len(line_y)-1]],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False)
    )

    fig.update_layout(showlegend=False)
    fig.update_layout(height=450)

    y_actl = compare_data[y_var]
    y_pred = compare_data['pred']

    global n_linerdm_mae
    global n_linerdm_mse
    global n_linerdm_rmse

    n_linerdm_mae = metrics.mean_absolute_error(y_actl, y_pred)
    n_linerdm_mse = metrics.mean_squared_error(y_actl, y_pred)
    n_linerdm_rmse = np.sqrt(metrics.mean_squared_error(y_actl, y_pred))

    #---------- Plot 2 ------------------------------------------------------
    fig1 = px.scatter(com_data, x=x_var[0], y="value", color="type" )
    fig1.update_traces(marker=dict(size=14, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))
    fig1.update_layout(showlegend=True)
    fig1.update_layout(height=450)
    

    return fig, fig1, str_fit_result, linerdm_DataTable_1










######################################################################################
## Data Predict
######################################################################################
@app.callback(Output('linerdm_plot_3'          , 'figure'  ),
              Output('linerdm_DT_2'            , 'children'),
              Output('linerdm_md_coef_DT'      , 'data'    ),
              Output('linerdm_DT_3'            , 'data'    ),
              Input('btn_linerdm_model_predict', 'n_clicks'),
              State('cbo_linerdm_model_choice' , 'value'   ),
              State('ds_linerdm_train_data'    , 'data'    )
              )
def cb_linerdm_predict(n_clicks, model_name, data ):
    if data is None:
        raise PreventUpdate
    if n_clicks is None:
        raise PreventUpdate    
    if model_name is None:
        raise PreventUpdate  
    if gTestFilePath is None:
        raise PreventUpdate  

    data = linerdm_load_predict_data(gTestFilePath)

    data = data.dropna(axis=0)

    md_list = uf_load_model_list()
    r = (md_list.md_name == model_name[0])

    md = md_list.loc[r,:]

    model_path = md['md_path'].item()  + md['md_filename'].item()
    lm_model = pickle.load(open(model_path, 'rb'))
    # lm_model = pickle.load(open( './model/lm_model_2022-02-23.sav'  , 'rb'))

    feature_column =  lm_model.feature_names_in_  #md['md_x_var'][0]

    if lm_model.n_features_in_ == 1 :
        p_data = data[feature_column].values.reshape(-1,1)
    else :    
        p_data = data[feature_column]

    data_pred= lm_model.predict(p_data)

    result_data = pd.concat([data.reset_index(drop=True), pd.DataFrame(data_pred, columns=['pred'])] , axis=1)
    
    if isinstance(md['md_y_var'], str) :
        y_val = md['md_y_var'].item()
    else:
        y_val = md['md_y_var'].item()

    model_coef = pd.DataFrame(lm_model.coef_, lm_model.feature_names_in_, columns=['Coefficient'])
    model_coef = pd.concat([model_coef.reset_index(drop=True), pd.DataFrame(model_coef.index, columns=['X'])] , axis=1)

    
    # 모델 검증
    y_actl = result_data[y_val]
    y_pred = result_data['pred']

    nMean_Absolute_Error = metrics.mean_absolute_error(y_actl, y_pred)
    nMean_Squared_Error = metrics.mean_squared_error(y_actl, y_pred)
    nRoot_Mean_Squared_Error = np.sqrt(metrics.mean_squared_error(y_actl, y_pred))
    
    # 불러온 기존 모델의 값
    nOld_mae  = md['md_mae'].item()
    nOld_mse  = md['md_mse'].item()
    nOld_rmse = md['md_rmse'].item()

    d = {'Error':  ['Mean Absolute Error', 'Mean Squared Error', 'Root Mean Squared Error'], 
         'Model':  [nOld_mae,nOld_mse,nOld_rmse ] ,
         'Predict':[nMean_Absolute_Error,nMean_Squared_Error,nRoot_Mean_Squared_Error] ,
         'Pred/Model':[nMean_Absolute_Error/nOld_mae*100, nMean_Squared_Error/nOld_mse*100,nRoot_Mean_Squared_Error/nOld_rmse*100 ]
         }
    df_result = pd.DataFrame(data=d, index=[0, 1, 2])
    # pred_result = 'Mean Absolute Error : ' + str(nMean_Absolute_Error) + '\nMean Squared Error : ' + str(nMean_Squared_Error) + '\nRoot Mean Squared Error : ' + str(nRoot_Mean_Squared_Error)


    plot_data = pd.DataFrame({'cyc_date':result_data['cyc_date'],
                              'value':result_data[y_val],
                               'type':'act'}).append(pd.DataFrame({'cyc_date':result_data['cyc_date'], 
                                                                   'value':result_data['pred'], 
                                                                   'type':'pred'}))


    #----------- Test/Prediction Data Table -----------------------------------------
    columns = [{"name": i, "id": i, } for i in result_data.columns]

    linerdm_DataTable_1 = dash_table.DataTable(
                    data = result_data.to_dict('rows'),
                    columns = columns,
                    editable=False,
                    style_table={'height': '535px', 'overflowY': 'auto', 'overflowX': 'auto'},
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
    #----------- Test/Prediction Data Table -----------------------------------------

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if isinstance(feature_column, str) :
        f_column = feature_column
    else :    
        f_column = "cyc_date"


    plot_data[f_column] = plot_data[f_column].apply(str)

    fig = px.line(plot_data, x=f_column , y='value', color='type', title="LM Model Predict Result")
    fig.update_traces(mode='lines+markers')
    fig.update_layout(showlegend=True)
    fig.update_layout(hovermode="x") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
    fig.update_traces(hovertemplate="<b>Value: %{y}</b>") 
    fig.update_layout(height=450)

    return fig, linerdm_DataTable_1, model_coef.to_dict('records'), df_result.to_dict('recoreds')
