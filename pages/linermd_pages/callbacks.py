from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
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
    if data is None:
        raise PreventUpdate    

    data = pd.read_json(data, orient='split')

    train_data = linerdm_load_train_data(DATA_PATH+data['train'].iloc[0] )
    test_data  = linerdm_load_train_data(DATA_PATH+data['test'].iloc[0] )

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





@app.callback(Output('linerdm_plot_1'       , 'figure'),
              Input('btn_linerdm_apply'     , 'n_clicks'  ),
              State('cbo_linerdm_x'         , 'value'),
              State('cbo_linerdm_y'         , 'value'),
              State('ds_linerdm_train_data' , 'data'))
def cb_linerdm_plot1_render(ts, x_var, y_var, data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
        
    data = pd.read_json(data, orient='split')
    data = data.sort_values("cyc_date",   ascending = True )
    data["cyc_date"]   = data["cyc_date"].apply(str)

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    plot_type = 'L'

 
    fig =  px.scatter(
            data_frame=data, 
            x=x_var, 
            y=y_var, 
            color='cell_no', 
            # symbol='3', 
            size=None, 
            hover_name=None, 
            hover_data=None, 
            custom_data=None, 
            text=None, 
            facet_row=None, 
            facet_col=None, 
            facet_col_wrap=0, 
            facet_row_spacing=None, 
            facet_col_spacing=None, 
            error_x=None, 
            error_x_minus=None, 
            error_y=None, 
            error_y_minus=None, 
            animation_frame=None, 
            animation_group=None, 
            category_orders=None, 
            labels=None, 
            orientation=None, 
            color_discrete_sequence=None, 
            color_discrete_map=None, 
            color_continuous_scale=None, 
            range_color=None, 
            color_continuous_midpoint=None, 
            symbol_sequence=None, 
            symbol_map=None, 
            opacity=None, 
            size_max=None, 
            marginal_x=None, 
            marginal_y=None, 
            trendline=None, 
            trendline_options=None, 
            trendline_color_override=None, 
            trendline_scope='trace', 
            log_x=False, 
            log_y=False, 
            range_x=None, 
            range_y=None, 
            render_mode='auto', 
            # title='Voltage Info', 
            template=None, 
            width=None, 
            height=400
    )   
      
        
    fig.update_layout(showlegend=False) #Legend Hide
        
                        
    # fig.update_layout(title=dict(text="Voltage Info",
    #                              font=dict(color="blue", size=16),
    #                              pad=dict(t=0,l=0,b=0,r=0)
    #                             ) 
    #                   )
       
              

    

    # fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

    # fig.update_traces(
    #                   hovertemplate="<b>Rack:%{text} </b><br><br>"+
    #                                 "DateTime: %{x} <br>" +
    #                                 "Voltage: %{y}") 
    
   

    # fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
    #                                   font_size=11,
    #                                   font_family="Rockwell")
    #                  )



    # # remove facet/subplot labels
    # # fig.update_layout(annotations=[], overwrite=True)

    # fig.update_layout(
    #     showlegend=True,
    #     legend=dict(title=dict(side='left',
    #                            text='Rack',
    #                            font=dict(size=10) ) ,
    #                 font=dict(size=10), #font:color,family,size           
    #                 bgcolor='white',
    #                 bordercolor='black',
    #                 borderwidth=0 ,
    #                 traceorder = 'normal', #"reversed", "grouped", "reversed+grouped", "normal"
    #                 itemwidth=30,
    #                 itemsizing='constant' , # ( "trace" | "constant" )
    #                 orientation = 'h' , # ( "v" | "h" ) ,
    #                 valign= 'bottom', # ( "top" | "middle" | "bottom" )
    #                 x=0.5 ,
    #                 y=-0.2 ,
    #                 xanchor='center', #( "auto" | "left" | "center" | "right" )
    #                 yanchor='top'  #( "auto" | "top" | "middle" | "bottom" )
    #                 )
    #     )

    # strip down the rest of the plot
    fig.update_layout(
        paper_bgcolor = 'white',
        plot_bgcolor  = 'white',
        margin=dict(autoexpand=True,t=30,l=0,b=0,r=0)
    )

    # # hide and lock down axes
    # # fig.update_xaxes(visible=True, fixedrange=True)
    # # fig.update_yaxes(visible=True, fixedrange=True)
    # # 마우스 오버시 x , y 라인을 보여줌.
    # fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    # fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # # fig.update_layout(width='100%')
    fig.update_layout(height=580)

    return fig
