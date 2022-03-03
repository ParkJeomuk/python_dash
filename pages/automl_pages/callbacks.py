from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date,timedelta,datetime
from tkinter import *
from tkinter import filedialog
from dash import dash_table

from sklearn.linear_model import LinearRegression
from sklearn import metrics

#h2o -----------------------
# import h2o
# from  h2o.automl import H2OAutoML
# # from  h2o.estimators.gbm import H2OGradientBootingEstimator

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
import pickle
import re
import numpy as np

from utils.server_function import *
from utils.constants  import *
from pages.automl_pages.model import *


import sys
from io import StringIO


class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()


# @app.callback(Output('automl_predict_filname' , 'children'),
#               Input('btn_automl_model_file', 'n_clicks') )
# def cb_automl_file_open(n_clicks  ):
#     if n_clicks is None:
#         raise PreventUpdate 

#     global gTestFilePath

#     root = Tk()
#     root.withdraw()
#     # root.iconbitmap(default='Extras/transparent.ico')


#     filename = filedialog.askopenfilename(initialdir='/')
#     gTestFilePath = filename
#     print('***', filename)

#     root.destroy()  # <--- SOLUTION

#     return filename






@app.callback(Output('ds_automl_train_data'     , 'data'      ),
              Output('ds_automl_test_data'      , 'data'      ),
              Output("cbo_automl_x"             , "options"   ),
              Output("cbo_automl_y"             , "options"   ),
              Input('btn_automl_dataload'       , 'n_clicks'  ) 
              )
def cb_automl_data_load(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    train_data = automl_load_train_data(DATA_PATH+'tmp_train.pkl' )
    test_data  = automl_load_train_data(DATA_PATH+'tmp_test.pkl' )

    col_df = pd.DataFrame({'code':pd.DataFrame(train_data.columns).iloc[:,0]})

    opt = [{'label': col, 'value': col} for col in train_data.columns]

    return train_data.to_json(date_format='iso',orient='split')  ,test_data.to_json(date_format='iso',orient='split') ,  opt ,  opt 





@app.callback(Output('automl_plot_1'           , 'figure'  ),
              Output("div_automl_data_info"    , "children"   ),
              Output('automl_DT_1'             , 'children'),
              Input('btn_automl_model_apply'   , 'n_clicks'  ) ,
              State("cbo_automl_x"             , "value"   ),
              State("cbo_automl_y"             , "value"   )
              )
def cb_linerdm_data_info(n_clicks, x_varlist, y_varlist):
    if n_clicks is None:
        raise PreventUpdate

    if x_varlist is None:
        raise PreventUpdate

    if y_varlist is None:
        raise PreventUpdate        

    # train_data = automl_load_train_data(DATA_PATH+'tmp_train.pkl' )
    # test_data  = automl_load_train_data(DATA_PATH+'tmp_test.pkl' )


    # max_runtime_secs = 60

    # automl_train = h2o.H2OFrame(train_data)
    # automl_valid = h2o.H2OFrame(test_data)

    # y_var = y_varlist #'soh'
    # x_var = x_varlist#['q_u','gap','u_vol','o_vol','n','cyc_date','cur_avg','soh'] #list(test_data.columns)
    # if y_var in x_var :
    #     x_var.remove(y_var)

    # # For binary classification, response should be a factor
    # # automl_train[y_var] = automl_train[y_var].asfactor()
    # # automl_valid[y_var] = automl_valid[y_var].asfactor()
    # automl_train[y_var] = automl_train[y_var]
    # automl_valid[y_var] = automl_valid[y_var]

    # # ###############################################################    
    # # Run AutoML for 120 seconds
    # aml = H2OAutoML(max_runtime_secs=max_runtime_secs, exclude_algos =['XGBoost', 'StackedEnsemble','DeepLearning'])
    # aml.train(x = x_var, y = y_var, training_frame=automl_train, leaderboard_frame=automl_valid)
    
    # ###############################################################
    # ## save metric
    # # Print Leaderboard (ranked by xval metrics)
    # leaderboard = aml.leaderboard
    # performance = aml.leader.model_performance(automl_valid)  # (Optional) Evaluate performance on a test set

    
    # #     return fig
    # # fig = aml.leader.varimp_plot()

    # strResult = "" #str(aml.leader)
    
    # with RedirectedStdout() as out:
    #     print(aml.leader)
    #     strResult = str(out)

    # lst_vi = aml.leader.varimp()
    # df_vi = pd.DataFrame(lst_vi, columns=['variable','relative_importance','scaled_importance','percentage'])

    # #----------- Test/Prediction Data Table -----------------------------------------
    # columns = [{"name": i, "id": i, } for i in df_vi.columns]

    # automl_DataTable_1 = dash_table.DataTable(
    #                 data = df_vi.to_dict('rows'),
    #                 columns = columns,
    #                 editable=False,
    #                 style_table={'height': '350px', 'overflowY': 'auto', 'overflowX': 'auto'},
    #                 style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
    #                 column_selectable="single",
    #                 selected_rows=[],
    #                 sort_action='custom',
    #                 sort_mode='multi',
    #                 sort_by=[],
    #                 style_cell_conditional=[  
    #                     { 'if': {'column_id': 'variable'  }, 'textAlign': 'center'},
    #                     { 'if': {'column_id': 'relative_importance'   }, 'textAlign': 'right' },
    #                     { 'if': {'column_id': 'scaled_importance'     }, 'textAlign': 'right' },
    #                     { 'if': {'column_id': 'percentage'            }, 'textAlign': 'right' },
    #                     {'fontSize' : '16px'},
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
    # #----------- Test/Prediction Data Table -----------------------------------------





    # if df_vi is None:
    #     fig =  blank_fig() #px.scatter(x=None, y=None)        
    # else:
    #     df_vi = df_vi.sort_values(by='scaled_importance',ascending=True, ignore_index=True)
    #     fig = px.bar(df_vi, x='scaled_importance', y='variable', orientation='h')
    #     fig.update_layout(
    #         paper_bgcolor = 'white',
    #         plot_bgcolor  = 'white',
    #         margin=dict(autoexpand=True,t=30,l=0,b=0,r=0)
    #     )

    # return fig , strResult, automl_DataTable_1
    return None, None, None


# @app.callback(Output('div_automl_datainfo', 'children' ),
#               Input('ds_automl_train_data'  , 'modified_timestamp'),
#               State('ds_automl_train_data'  , 'data'))
# def cb_automl_data_info(ts, data ):
#     if ts is None:
#         raise PreventUpdate
#     if data is None:
#         raise PreventUpdate    

#     buf = io.StringIO()
#     data = pd.read_json(data, orient='split')
#     data.info(buf=buf)
#     strResult = buf.getvalue()
  
#     return strResult







# @app.callback(Output('automl_div_save_model_name', 'children' ),
#               Output("cbo_automl_model_choice" , "options" ), 
#               Input('btn_automl_model_save'    , 'n_clicks'),
#               State('ds_automl_train_data'     , 'data'),
#               State('cbo_automl_x'             , 'value'   ),
#               State('cbo_automl_y'             , 'value'   )
#               )
# def cb_automl_data_info(ts, data, x_var, y_var ):
#     if ts is None:
#         raise PreventUpdate
#     if data is None:
#         raise PreventUpdate    

#     md_file = './model/lm_model.sav'
#     loaded_model = pickle.load(open(md_file  , 'rb'))
    

#     sFileName = "lm_model_" + str(date.today()) + ".sav"
#     pickle.dump(loaded_model, open('./model/'+sFileName, 'wb'))

#     dModel = {'md_name': re.sub('.sav','',sFileName), 
#               'md_path': './model/', 
#               'md_filename': sFileName, 
#               'md_x_var': x_var, 
#               'md_y_var': y_var, 
#               'md_desc':'desc'}
    
#     uf_save_model_list(dModel)

#     # #기존 파일 삭제
#     # try:
#     #   os.remove(md_file)
#     # except:
#     #     print('Not Exists File')
  
#     md_list = os.listdir('./model/')
#     opt = [{'label': re.sub('.sav','',col), 'value': re.sub('.sav','',col)} for col in md_list]
    
#     return sFileName , opt





  
# @app.callback(Output('automl_plot_1'         , 'figure'  ),
#               Output('automl_plot_2'         , 'figure'  ),
#               Output('div_automl_model_info' , 'children'),
#               Output('automl_DT_1'           , 'children'),
#               Input('btn_automl_model_apply' , 'n_clicks'),
#               State('cbo_automl_x'           , 'value'   ),
#               State('cbo_automl_y'           , 'value'   ),
#               State('ds_automl_train_data'   , 'data'    ),
#               State('ds_automl_test_data'    , 'data'    )
#               )
# def cb_automl_plot1_render(ts, x_var, y_var, data , test_data ):
#     if ts is None:
#         raise PreventUpdate
#     if data is None:
#         raise PreventUpdate
#     if test_data is None:
#         raise PreventUpdate    
#     if x_var is None:
#         # toggle_modal(True)
#         raise PreventUpdate
#     if y_var is None:
#         # toggle_modal(True)
#         raise PreventUpdate    


#     max_runtime_secs = 300

#     data = pd.read_json(data, orient='split')
#     data = data.dropna(axis=0)
#     data = data.sort_values("cyc_date",   ascending = True )
    
    
#     test_data = pd.read_json(test_data, orient='split')
#     test_data = test_data.dropna(axis=0)
#     test_data = test_data.sort_values("cyc_date",   ascending = True )

#     x_data = data[x_var]
#     test_x_data = test_data[x_var]
#     if(len(x_data.columns)<2):
#        x_data = pd.DataFrame(x_data.values.reshape(-1,1), columns=['cyc_date'])
#        test_x_data = test_x_data.values.reshape(-1,1)

#     y_data = data[y_var]

#     #----- Column Not Number Type  Cast Float Type ----
#     x_data = pd.DataFrame(x_data)
#     col_type = x_data.dtypes

#     for key,value in col_type.items():
#         if value != 'int64' and value != 'float64':
#             x_data[key] = x_data[key].apply(float)
#     #----- Column Not Number Type  Cast Float Type ----


#     h2o.init()
#     h2o.no_progress()


#     automl_train = h2o.H2OFrame(x_data)
#     automl_valid = h2o.H2OFrame(test_x_data)


#     # For binary classification, response should be a factor
#     automl_train[y_var] = automl_train[y_var].asfactor()
#     automl_valid[y_var] = automl_valid[y_var].asfactor()

#     # ###############################################################    
#     # Run AutoML for 120 seconds
#     aml = H2OAutoML(max_runtime_secs=max_runtime_secs, exclude_algos =['XGBoost', 'StackedEnsemble'])
#     aml.train(x = x_var, y = y_var, training_frame=automl_train, leaderboard_frame=automl_valid)

#     data_pred= ''
#     test_pred = ''
    

#     compare_data = pd.concat([test_data.reset_index(drop=True), pd.DataFrame(test_pred, columns=['pred']),pd.DataFrame(range(1,len(test_data)+1),columns=['seq'])], axis=1)
#     com_data = pd.DataFrame({'cyc_date':compare_data['cyc_date'],'seq':compare_data['seq'], 'value':compare_data[y_var], 'type':'act'}).append(pd.DataFrame({'cyc_date':compare_data['cyc_date'], 'seq':compare_data['seq'], 'value':compare_data['pred'], 'type':'pred'}))

#     line_x = pd.DataFrame(x_data).iloc[:,0]
#     line_y = pd.DataFrame(data_pred).iloc[:,0]

#     nCoef = lm.coef_[0]
#     nIntercept = lm.intercept_

#     #-----------StatsMOdels --------------------------------------------------------
#     if len(x_data.columns) == 1 :
#         x_data = x_data.to_numpy()

#     result = sm.OLS(y_data, sm.add_constant(x_data)).fit()
#     str_fit_result =(result.summary().as_text())

#     #----------- Test/Prediction Data Table -----------------------------------------
#     columns = [{"name": i, "id": i, } for i in compare_data.columns]

#     automl_DataTable_1 = dash_table.DataTable(
#                     data = compare_data.to_dict('rows'),
#                     columns = columns,
#                     editable=False,
#                     style_table={'height': '450px', 'overflowY': 'auto', 'overflowX': 'auto'},
#                     style_cell={'padding-top':'2px','padding-bottom':'2px','padding-left':'5px','padding-right':'5px'},
#                     column_selectable="single",
#                     selected_rows=[],
#                     sort_action='custom',
#                     sort_mode='multi',
#                     sort_by=[],
#                     style_cell_conditional=[
#                         { 'if': {'column_id': 'cyc_date'  }, 'textAlign': 'center'},
#                         { 'if': {'column_id': 'bank_no'   }, 'textAlign': 'center'},
#                         { 'if': {'column_id': 'rack_no'   }, 'textAlign': 'center'},
#                         { 'if': {'column_id': 'cell_no'   }, 'textAlign': 'center'},
#                         { 'if': {'column_id': 'soh'       }, 'textAlign': 'right' },
#                         {'fontSize' : '16px'},
#                     ],
#                     style_data_conditional=[
#                         {
#                             'if': {'row_index': 0}, 'backgroundColor': '#FFF2CC'  ,
#                             # data_bars(dataTable_column, 'ChargeQ')  +
#                             # data_bars(dataTable_column, 'Voltage'),
#                         },
#                     ],
#                     style_header={
#                         'backgroundColor': '#929494',
#                         'fontWeight': 'bold',
#                         'fontSize' : '16px',
#                         'textAlign': 'center',
#                         'height':'40px'
#                     },
#                     export_headers='display',
#                 )
#     #----------- Test/Prediction Data Table -----------------------------------------

#     pio.templates.default = "plotly_white"
#     plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

#     if data is None:
#         fig =  blank_fig() #px.scatter(x=None, y=None)        
#         return fig
    
#     if(x_var[0]=='cyc_date'):
#         data["cyc_date"] = data["cyc_date"].apply(str)
#         com_data["cyc_date"] = com_data["cyc_date"].apply(str)
#         line_x = line_x.apply(str)


#     fig = px.scatter(data, x=x_var[0], y=y_var )
#     fig.update_traces(marker=dict(size=14, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))

#     fig.add_trace(
#         go.Scatter(
#             x=[line_x.iloc[0],line_x.iloc[len(line_x)-1]],
#             y=[line_y.iloc[0],line_y.iloc[len(line_y)-1]],
#             mode="lines",
#             line=go.scatter.Line(color="gray"),
#             showlegend=False)
#     )

#     fig.update_layout(showlegend=False)
#     fig.update_layout(height=450)



#     #---------- Plot 2 ------------------------------------------------------
#     fig1 = px.scatter(com_data, x=x_var[0], y="value", color="type" )
#     fig1.update_traces(marker=dict(size=14, line=dict(width=0,color='DarkSlateGrey')), selector=dict(mode='markers'))
#     fig1.update_layout(showlegend=True)
#     fig1.update_layout(height=450)
    

#     return fig, fig1, str_fit_result, automl_DataTable_1









