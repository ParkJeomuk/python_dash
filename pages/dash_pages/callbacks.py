from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_admin_components as dac

import pandas as pd
import plotly.io as pio
import plotly.express as px
import time
import plotly.graph_objs as go
import json
import dash as html
import dash_table

from utils.server_function import *
from pages.dash_pages.model import *
from utils.constants import RACK_COLOR






def dash_summary_data(sDataType, sBankNo, sDate, eDate ):
    data = df_dash_data()

    data["cyc_date"] = data["cyc_date"].apply(str)

    if sDataType == "Comparison":
        data = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"]==sDate.replace('-','')) ]
    else:    
        data = data[(data["bank_no"] == int(sBankNo)) & ((data["cyc_date"] >= sDate.replace('-','')) & (data["cyc_date"] <= eDate.replace('-',''))  )]

    data['dtime'] = pd.to_datetime(data['serial_dt'],unit='s')
    data = data.sort_values(by=['rack_no','serial_dt'])
    return data



def dash_q_data(sBankNo):
    data = df_dash_q_data()
    data = data[data["rack_no"]<100]
    data["s_date"]   = data["s_date"].apply(str)
    data = data[data["bank_no"]==int(sBankNo)]
    data = data.sort_values(by=['bank_no','rack_no','s_date'])
    return data




def dash_data_table(sBankNo, sStartDate, sEndDate):
    data = df_dash_data_table_list()
    data["cyc_date"]   = data["cyc_date"].apply(str)

    data = data[(data["bank_no"]== int(sBankNo)) & 
                (data["cyc_date"] >= sStartDate.replace('-','')) & 
                (data["cyc_date"] <= sEndDate.replace('-',''))]

    data = data.sort_values(by=['bank_no','cyc_date'], ascending=False)
    data.columns = ['a','Date','Bank','Voltage','Current','ChargeQ','SunShine', 'DataCount','DataFail','UseYN','UseDesc','DTime', 'WeekDay','sid']
    
    return data[['Date','WeekDay','Bank','Voltage','Current','ChargeQ','DataCount','DataFail','UseYN','UseDesc']]


def dash_box_data(sCysDate, sBankNo):
    data = df_dash_data_box(sCysDate.replace('-',''), sBankNo)
    return data


#--------------------------------------------------------------------------------------------------------------








#---- Label 1 Change
@app.callback(Output("lbl_date1", "children"), 
              Output("lbl_date2", "children"), 
             [Input("cbo_dash_data_type", "value")])
def lbl_date1_output_text(value):
    if value is None:
        raise PreventUpdate

    if value == 'Comparison':
        rtn_val1 = 'Stand Date'
        rtn_val2 = 'Compare Date'
    else:
        rtn_val1 = 'Start Date'
        rtn_val2 = 'End Date'

    return rtn_val1, rtn_val2


 



@app.callback(Output('ds_dash_df'        , 'data' ),
              Output('ds_dash_compare_df', 'data' ),
              Output('dash_box_voltage'  , 'children'),
              Output('dash_box_cq'       , 'children'),
              Output('dash_box_datacount', 'children'),
              Output('dash_box_fail'     , 'children'),
              Output('dash_box_current_c', 'children'),
              Output('dash_box_current_d', 'children'),
              Input('dash_btn_load'      , 'n_clicks') ,
              State('cbo_dash_data_type' , 'value') ,
              State('cbo_dash_bank'      , 'value') ,
              State('dtp_dash_stand'     , 'date' ) ,
              State('dtp_dash_compare'   , 'date' ) 
              )
def dash_data_load(n_clicks, data_type, bank_no, sDate, eDate ):
    if n_clicks is None:
        raise PreventUpdate
    if data_type is None:
        raise PreventUpdate    
    if bank_no is None:
        raise PreventUpdate
    if sDate is None:
        raise PreventUpdate    
    if eDate is None:
        raise PreventUpdate    


    if data_type == "Comparison":
        data         = dash_summary_data(data_type, bank_no, sDate, sDate)
        compare_data = dash_summary_data(data_type, bank_no, eDate, eDate)
        compare_data = compare_data[['serial_dt','bank_no','current','voltage','avg_temp']].groupby(['serial_dt','bank_no'],as_index=False).mean()
        #----- 비교 데이타의 시간 맞추기
        cha_time     = data['serial_dt'].min()-compare_data['serial_dt'].min()
        compare_data['serial_dt'] = compare_data['serial_dt'] + cha_time
        compare_data['dtime'] = compare_data['serial_dt'].map(lambda x : datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    else:    
        data         = dash_summary_data(data_type, bank_no, sDate, eDate)
        compare_data = None


    box_data = dash_box_data(sDate, bank_no)

    box_voltage = dac.ValueBox(
                        value= str(box_data.iloc[0]['voltage']) + " V",
                        subtitle="Voltage [" + str(box_data.iloc[0]['voltage_per']) + "%]" ,
                        color = "primary",icon = "chart-line",width=12)
    box_cq    = dac.ValueBox(
                        value = str(box_data.iloc[0]['charge_q']) + " Ah",
                        subtitle = "Charge Q [" + str(box_data.iloc[0]['charge_q_per']) + "%]" ,
                        color = "info",icon = "charging-station",width=12)

    box_cnt   = dac.ValueBox(  
                        value = str(box_data.iloc[0]['data_count'])  ,
                        subtitle = "Data Count [" + str(box_data.iloc[0]['datacount_per']) + "%]" ,
                        color = "warning",icon = "database",width=12)

    box_fail  = dac.ValueBox(  
                        value = str(box_data.iloc[0]['datafail'])  ,
                        subtitle = "Data Fail [" + str(box_data.iloc[0]['datafail_per']) + "%]" ,
                        color = "danger",icon = "frown",width=12)

    box_curc  = dac.ValueBox(  
                        value = str(box_data.iloc[0]['current_c']) + " A" ,
                        subtitle = "Current(C) [" + str(box_data.iloc[0]['current_c_per']) + "%]" ,
                        color = "success",icon = "wave-square",width=12)                        

    box_curd  = dac.ValueBox(  
                        value = str(box_data.iloc[0]['current_d']) + " A" ,
                        subtitle = "Current(D) [" + str(box_data.iloc[0]['current_c_per']) + "%]" ,
                        color = "secondary",icon = "wave-square",width=12)                        
    if compare_data is None:
        compare_data = None
    else :   
        compare_data = compare_data.to_json(date_format='iso' , orient='split')

    return data.to_json(date_format='iso' , orient='split') , compare_data , box_voltage, box_cq, box_cnt, box_fail, box_curc, box_curd








@app.callback(Output('dash_store_data_table'  , 'data'),
              Input('dash_btn_load_check_data', 'n_clicks') ,
              State('dash_tab2_date_range'    , 'start_date'),
              State('dash_tab2_date_range'    , 'end_date'))
def dash_data_table_load(n_clicks, start_date, end_date ):
    if n_clicks is None:
        raise PreventUpdate
    if start_date is None:
        raise PreventUpdate
    if end_date is None:
        raise PreventUpdate    

    data = dash_data_table('1', start_date, end_date)

    return data.to_json(date_format='iso' , orient='split')









@app.callback(Output('dash_plot_1'        , 'figure'),
              Input('ds_dash_df'          , 'modified_timestamp'),
              Input('ds_dash_compare_df'  , 'modified_timestamp'),
              State('ds_dash_df'          , 'data'  ),
              State('ds_dash_compare_df'  , 'data'  ))
def dash_plot1_render(ts,compare_ts, data , compare_data ):
    if data is None:
        raise PreventUpdate
    
    data = pd.read_json(data, orient='split')
    
    if compare_data is not None :
        compare_data = pd.read_json(compare_data, orient='split')

    # pio.templates.default = "plotly_white"
    # plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    plot_type = 'L'



    if(plot_type == 'L'):

        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'voltage', 
                       color = 'rack_no',
                       line_group='rack_no',
                       text=data['rack_no']
                       )    

        
        fig.update_traces(mode="lines")   
        
        #compare data       
        if compare_data is not None :
            fig.add_trace(go.Scatter(
                x= compare_data['dtime'], 
                y= compare_data['voltage'] ,
                line = dict(color='royalblue', width=4, dash='dot')
                )
            )



    elif(plot_type == 'P'):
        fig =  px.scatter(
                data_frame=data, 
                x='dtime', 
                y='voltage', 
                color='rack_no', 
                symbol='3', 
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
                title='Voltage Info', 
                template=None, 
                width=None, 
                height=400
		)   
        # fig.update_traces(mode="markers")           
    else:
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'voltage', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
        # markers style
        fig.update_traces(marker=dict(size=12,
                                  opacity=0.5 ,
                                  line=dict(width=1
                                            # ,color='DarkSlateGrey'
                                           )
                                 ),
                     selector=dict(mode='markers'))    
        
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

    fig.update_layout(height=400)

    return fig



#---------- Plot 2 Render -----------------------------------------------------------------------
@app.callback(Output('dash_plot_2'        , 'figure'),
              Input('ds_dash_df'          , 'modified_timestamp'),
              Input('ds_dash_compare_df'  , 'modified_timestamp'),
              State('ds_dash_df'          , 'data'),
              State('ds_dash_compare_df'  , 'data'  ))
def dash_plot2_render(ts,compare_ts, data, compare_data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate

    data = pd.read_json(data, orient='split')

    if compare_data is not None :
        compare_data = pd.read_json(compare_data, orient='split')

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig

    plot_type = 'L'
    

    fig =  px.line(data, 
                    x = 'dtime',
                    y = 'current', 
                    color = 'rack_no',
                    text=data['rack_no']
                    )  
    #compare data       
    if compare_data is not None :                
        fig.add_trace(go.Scatter(
            x= compare_data['dtime'], 
            y= compare_data['current'] ,
            line = dict(color='royalblue', width=4, dash='dot')
            )
        )               
                            
    # fig.update_layout(title=dict(text="Current Info",
    #                              font=dict(color="blue", size=16),
    #                              pad=dict(t=0,l=0,b=0,r=0)
    #                             ) 
    #                   )
       
    # markers style
    fig.update_traces(marker=dict(size=12,
                                  opacity=0.5 ,
                                  line=dict(width=1
                                        #    , color='DarkSlateGrey'
                                           )
                                 ),
                     selector=dict(mode='markers'))               

    fig.update_traces(mode="lines")           

    fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

    # fig.update_traces(
    #                   hovertemplate="<b>Rack:%{text} </b><br><br>"+
    #                                 "DateTime: %{x} <br>" +
    #                                 "Voltage: %{y}") 
    
   

    # fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
    #                                   font_size=11,
    #                                   font_family="Rockwell")
    #                  )


    fig.update_layout(showlegend=False)

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

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

    # hide and lock down axes
    # fig.update_xaxes(visible=True, fixedrange=True)
    # fig.update_yaxes(visible=True, fixedrange=True)
    # 마우스 오버시 x , y 라인을 보여줌.
    fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # fig.update_layout(width='100%')
    fig.update_layout(height=400)

    return fig






#---------- Plot 3 Render -----------------------------------------------------------------------
@app.callback(Output('dash_plot_3'       , 'figure'),
              Input('ds_dash_df'          , 'modified_timestamp'),
              Input('ds_dash_compare_df'  , 'modified_timestamp'),
              State('ds_dash_df'          , 'data'  ),
              State('ds_dash_compare_df'  , 'data'  ))
def dash_plot3_render(ts,compare_ts, data, compare_data ):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate

    data         = pd.read_json(data, orient='split')

    if compare_data is not None :
        compare_data = pd.read_json(compare_data, orient='split')
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
     
    plot_type = 'L'    

    if(plot_type == 'L'):
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'avg_temp', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )  
        #compare data 
        if compare_data is not None :                      
            fig.add_trace(go.Scatter(
                x= compare_data['dtime'], 
                y= compare_data['avg_temp'] ,
                line = dict(color='royalblue', width=4, dash='dot')
                )
            )                  
    elif(plot_type == 'P'):
        fig =  px.scatter(data, 
                       x = 'dtime',
                       y = 'avg_temp', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
    else:
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'avg_temp', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
                        
    # fig.update_layout(title=dict(text="Current Info",
    #                              font=dict(color="blue", size=16),
    #                              pad=dict(t=0,l=0,b=0,r=0)
    #                             ) 
    #                   )
       
    # markers style
    fig.update_traces(marker=dict(size=12,
                                  opacity=0.5 ,
                                  line=dict(width=1
                                        #    , color='DarkSlateGrey'
                                           )
                                 ),
                     selector=dict(mode='markers'))               

    fig.update_traces(mode="lines")           

    fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

    # fig.update_traces(
    #                   hovertemplate="<b>Rack:%{text} </b><br><br>"+
    #                                 "DateTime: %{x} <br>" +
    #                                 "Voltage: %{y}") 
    
   

    # fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
    #                                   font_size=11,
    #                                   font_family="Rockwell")
    #                  )


    fig.update_layout(showlegend=False)

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

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

    # hide and lock down axes
    # fig.update_xaxes(visible=True, fixedrange=True)
    # fig.update_yaxes(visible=True, fixedrange=True)
    # 마우스 오버시 x , y 라인을 보여줌.
    fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # fig.update_layout(width='100%')
    fig.update_layout(height=400)

    return fig




#---------- Plot 4 Render -----------------------------------------------------------------------
@app.callback(Output('dash_plot_4'       , 'figure'),
              State('dtp_dash_stand'     , 'date' ),
              State('cbo_dash_bank'      , 'value' ),
              Input('dash_btn_load'      , 'n_clicks') )
def dash_plot4_render(stand_date, sBank_no, n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    if stand_date is None:
        raise PreventUpdate
    if sBank_no is None:
        raise PreventUpdate

    data = dash_q_data(sBank_no)
    data = data[data["s_date"] == stand_date.replace('-','')]

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig

    


    fig = px.bar(data, 
                 x="rack_no", 
                 y="q_amt", 
                 color="data_type", 
                 barmode="group" ,
                 text=data['data_type']
                ) 

    y_min = data["q_amt"].min()                        
    y_max = data["q_amt"].max()                        
    # fig.update_layout(title=dict(text="Current Info",
    #                              font=dict(color="blue", size=16),
    #                              pad=dict(t=0,l=0,b=0,r=0)
    #                             ) 
    #                   )
       
    # markers style
    # fig.update_traces(marker=dict(size=12,
    #                               opacity=0.5 ,
    #                               line=dict(width=1
    #                                     #    , color='DarkSlateGrey'
    #                                        )
    #                              ),
    #                  selector=dict(mode='markers'))               
 
    # fig.update_traces(mode="lines")           

    fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

    fig.update_traces(hovertemplate="<b>Rack: %{x} <br>" +
                                    "DataType: %{text} <br>" +
                                    "Q Amount: %{y}</b>") 
    
   

    # fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
    #                                   font_size=11,
    #                                   font_family="Rockwell")
    #                  )


    # fig.update_layout(showlegend=False)

    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)


    fig.update_layout(
        showlegend=True,
        legend=dict(
                    title=dict(side='left',
                               text='Data Type',
                               font=dict(size=10) ) ,
                    font=dict(size=10), #font:color,family,size           
                    bgcolor='white',
                    bordercolor='black',
                    borderwidth=0.3 ,
                    traceorder = 'normal', #"reversed", "grouped", "reversed+grouped", "normal"
                    itemwidth=30,
                    itemsizing='constant' , # ( "trace" | "constant" )
                    orientation = 'h' , # ( "v" | "h" ) ,
                    valign= 'bottom', # ( "top" | "middle" | "bottom" )
                    x=1 ,
                    y=0.99 ,
                    xanchor='right', #( "auto" | "left" | "center" | "right" )
                    yanchor='middle'  #( "auto" | "top" | "middle" | "bottom" )
                    )
        )

    # strip down the rest of the plot
    fig.update_layout(
        paper_bgcolor = 'white',
        plot_bgcolor  = 'white',
        margin=dict(autoexpand=True,t=30,l=0,b=0,r=0)
    )

    # hide and lock down axes
    # fig.update_xaxes(visible=True, fixedrange=True)
    fig.update_yaxes(visible=True, fixedrange=True,range=[y_min-20,y_max+10])
    # fig.update_yaxes(visible=True, fixedrange=True)
    # 마우스 오버시 x , y 라인을 보여줌.
    fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # fig.update_layout(width='100%')
    fig.update_layout(height=400)

    return fig



#---------- Plot 5 Polar Render -----------------------------------------------------------------------
@app.callback(Output('dash_plot_5'       , 'figure'),
              Input('dash_btn_load'      , 'n_clicks') )
def dash_plot5_render(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    
    data = df_dash_polar_data()
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        fig.update_layout(height=230)
        return fig
    
    fig = px.line_polar(data, 
                        r='value', 
                        theta='item', 
                        line_close=False)
    fig.update_traces(fill='toself')
    
    fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
    fig.update_layout(showlegend=False)

    # strip down the rest of the plot
    fig.update_layout(
        paper_bgcolor = 'white',
        plot_bgcolor  = 'white',
        margin=dict(autoexpand=True,t=15,l=10,b=15,r=10)
    )
    fig.update_layout(height=230)

    return fig




 




@app.callback(
    Output('dash_DT', 'data'),
    Input('dash_store_data_table', 'modified_timestamp'),
    Input('dash_DT', "page_current"),
    Input('dash_DT', "page_size"),
    State('dash_store_data_table', 'data'))
def dash_render_datatable(ts, page_current, page_size, data):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    if page_current is None:
        raise PreventUpdate
    if page_size is None:
        raise PreventUpdate        
    
    data = pd.read_json(data, orient='split')
    # data = data.sort_values(by=['rack_no','serial_dt'])

    # return data.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')
    return data.to_dict('records')




@app.callback(
    Output('dash_selection_DT', 'children'),
    Input('dash_plot_1', 'selectedData'))
def dash_plot1_selected_data(selectedData):

    df = json.dumps(selectedData, indent=2)

    columns = [{"name": i, "id": i, } for i in df.columns]

    dash_selected_data = dash_table.DataTable(
                    data=df,
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

    return dash_selected_data

