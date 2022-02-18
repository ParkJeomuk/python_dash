from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
from sklearn.linear_model import LinearRegression

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

from utils.server_function import *
from utils.constants  import *
from pages.linermd_pages.model import *


 


@app.callback(Output('ds_linerdm_train_data'     , 'data'      ),
              Output('ds_linerdm_test_data'      , 'data'      ),
              Output("cbo_linerdm_x"             , "options"   ),
              Output("cbo_linerdm_y"             , "options"   ),
              Input('btn_linerdm_dataload'       , 'n_clicks'  ),
              State('ds_train_test_file'         , 'data'      ) 
              )
def cb_linerdm_data_load(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    # if data is None:
    #     raise PreventUpdate    

    data = pd.read_json(data, orient='split')

    # train_data = linerdm_load_train_data(DATA_PATH+data['train'].iloc[0] )
    # test_data  = linerdm_load_train_data(DATA_PATH+data['test'].iloc[0] )
    train_data = linerdm_load_train_data(DATA_PATH+'tmp_train.pkl' )
    test_data  = linerdm_load_train_data(DATA_PATH+'tmp_test.pkl' )

    col_df = pd.DataFrame({'code':pd.DataFrame(train_data.columns).iloc[:,0]})

    opt = [{'label': col, 'value': col} for col in train_data.columns]
    # opt = [{"label": col, "value": col}] for col in col_df.code
    

    return train_data.to_json(date_format='iso',orient='split')  ,test_data.to_json(date_format='iso',orient='split') ,  opt ,  opt 






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




# @app.callback(
#     Output("modal-alert"            , "is_open" ),
#     [State("modal-backdrop", "is_open")],
# )
# def toggle_modal(is_open):
#     return is_open

@app.callback(Output('linerdm_plot_1'         , 'figure'  ),
              Output('linerdm_plot_2'         , 'figure'  ),
              Output('div_linerdm_model_info' , 'children'),
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
    if x_var is None:
        # toggle_modal(True)
        raise PreventUpdate
    if y_var is None:
        # toggle_modal(True)
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
       x_data = x_data.values.reshape(-1,1)
       test_x_data = test_x_data.values.reshape(-1,1)

    y_data = data[y_var]

    line_fitter = LinearRegression()
    lm = line_fitter.fit(x_data, y_data)

    data_pred= lm.predict(x_data)

    test_pred = lm.predict(test_x_data)

    compare_data = pd.concat([test_data.reset_index(drop=True), pd.DataFrame(test_pred, columns=['pred']),pd.DataFrame(range(1,len(test_data)+1),columns=['seq'])], axis=1)
    com_data = pd.DataFrame({'seq':compare_data['seq'], 'value':compare_data[y_var], 'type':'act'}).append(pd.DataFrame({'seq':compare_data['seq'], 'value':compare_data['pred'], 'type':'pred'}))

    line_x = pd.DataFrame(x_data).iloc[:,0]
    line_y = pd.DataFrame(data_pred).iloc[:,0]

    nCoef = lm.coef_[0]
    nIntercept = lm.intercept_

    #-----------StatsMOdels --------------------------------------------------------
    result = sm.OLS(y_data, sm.add_constant(x_data)).fit()
    str_fit_result =(result.summary().as_text())

    

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    if(x_var[0]=='cyc_date'):
        data["cyc_date"] = data["cyc_date"].apply(str)
        line_x = line_x.apply(str)


    fig = px.scatter(data, x=x_var[0], y=y_var, 
                    title="LM Model")

    fig.add_trace(
        go.Scatter(
            x=[line_x.iloc[0],line_x.iloc[len(line_x)-1]],
            y=[line_y.iloc[0],line_y.iloc[len(line_y)-1]],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False)
    )

    fig.update_layout(showlegend=False)
    
#     fig =  px.scatter(data, 
#                        x = data[x_var[0]].apply(str),
#                        y = data[y_var], 
#                        color = 'cell_no'
#                        )  
    
#    # fig.update_layout(title=dict(text="Current Info",
#     #                              font=dict(color="blue", size=16),
#     #                              pad=dict(t=0,l=0,b=0,r=0)
#     #                             ) 
#     #                   )
       
#     # markers style
#     fig.update_traces(marker=dict(size=12,
#                                   opacity=0.5 ,
#                                   line=dict(width=1
#                                         #    , color='DarkSlateGrey'
#                                            )
#                                  ),
#                      selector=dict(mode='markers'))               

#     # fig.update_traces(mode="lines")           

#     fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

#     # fig.update_traces(
#     #                   hovertemplate="<b>Rack:%{text} </b><br><br>"+
#     #                                 "DateTime: %{x} <br>" +
#     #                                 "Voltage: %{y}") 
    
   

#     # fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
#     #                                   font_size=11,
#     #                                   font_family="Rockwell")
#     #                  )


#     fig.update_layout(showlegend=False)

#     # remove facet/subplot labels
#     # fig.update_layout(annotations=[], overwrite=True)

#     # fig.update_layout(
#     #     showlegend=True,
#     #     legend=dict(title=dict(side='left',
#     #                            text='Rack',
#     #                            font=dict(size=10) ) ,
#     #                 font=dict(size=10), #font:color,family,size           
#     #                 bgcolor='white',
#     #                 bordercolor='black',
#     #                 borderwidth=0 ,
#     #                 traceorder = 'normal', #"reversed", "grouped", "reversed+grouped", "normal"
#     #                 itemwidth=30,
#     #                 itemsizing='constant' , # ( "trace" | "constant" )
#     #                 orientation = 'h' , # ( "v" | "h" ) ,
#     #                 valign= 'bottom', # ( "top" | "middle" | "bottom" )
#     #                 x=0.5 ,
#     #                 y=-0.2 ,
#     #                 xanchor='center', #( "auto" | "left" | "center" | "right" )
#     #                 yanchor='top'  #( "auto" | "top" | "middle" | "bottom" )
#     #                 )
#     #     )

#     # strip down the rest of the plot
#     fig.update_layout(
#         paper_bgcolor = 'white',
#         plot_bgcolor  = 'white',
#         margin=dict(autoexpand=True,t=30,l=0,b=0,r=0)
#     )

#     # hide and lock down axes
#     # fig.update_xaxes(visible=True, fixedrange=True)
#     # fig.update_yaxes(visible=True, fixedrange=True)
#     # 마우스 오버시 x , y 라인을 보여줌.
#     fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
#     fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

#     # fig.update_layout(width='100%')
    fig.update_layout(height=450)


    fig1 = px.scatter(com_data, x="seq", y="value", color="type",
                    title="LM Model")

    fig1.update_layout(showlegend=True)
    fig1.update_layout(height=450)

    return fig, fig1, str_fit_result
