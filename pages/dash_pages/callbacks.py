from apps import app
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.io as pio
import plotly.express as px
import time
from datetime import datetime
import plotly.graph_objs as go

from pages.dash_pages.model import df_dash_data

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig


#--------------------------------------------------------------------------------------------------------------




# #------------ Raw Data Data Store -----------------------------------------------------------------------------
# @app.callback(Output('dash_raw_data', 'data'),
#               Input('dash_btn_load_raw_data', 'n_clicks') )
# def dash_raw_data_load(n_clicks):
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate
#     # data.to_parquet('d:/python_test/apps/sample_data/raw_data.parquet', compression='gzip')
                
#     data = pd.read_parquet('d:/python_test/apps/sample_data/raw_data.parquet')
#     # data = pd.read_csv('./apps/sample_data/raw_data.csv')
#     return data.to_json(date_format='iso' , orient='split')
# #--------------------------------------------------------------------------------------------------------------

@app.callback(Output('dash_df', 'data'),
              Input('dash_btn_load', 'n_clicks') )
def dash_data_load(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    
    return df_dash_data()


@app.callback(Output('dash_plot_1'       , 'figure'),
              Input('dash_df'            , 'modified_timestamp'),
              Input('dash_rdo_plot_type' , 'value'),
              State('dash_df'            , 'data'))
def dash_plot1_render_click(ts, plot_type, data):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    
    data = pd.read_json(data, orient='split')
    data = data.sort_values(by=['rack_no','serial_dt'])
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig
    
    if(plot_type == 'L'):
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'voltage', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
        fig.update_traces(mode="lines")           
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

    # # strip down the rest of the plot
    # fig.update_layout(
    #     paper_bgcolor = 'white',
    #     plot_bgcolor  = 'white',
    #     margin=dict(autoexpand=True,t=30,l=0,b=0,r=0)
    # )

    # # hide and lock down axes
    # # fig.update_xaxes(visible=True, fixedrange=True)
    # # fig.update_yaxes(visible=True, fixedrange=True)
    # # 마우스 오버시 x , y 라인을 보여줌.
    # fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    # fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # # fig.update_layout(width='100%')
    # fig.update_layout(height=500)

    return fig



#---------- Plot 2 Render -----------------------------------------------------------------------
@app.callback(Output('dash_plot_2'       , 'figure'),
              Input('dash_df'            , 'modified_timestamp'),
              Input('dash_rdo_plot_type' , 'value'),
              State('dash_df'            , 'data'))
def dash_plot2_render(ts, plot_type, data):
    if ts is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    
    data = pd.read_json(data, orient='split')
    # data = data[data['rack_no'].isin([1,2])]
    data = data.sort_values(by=['rack_no','serial_dt'])
    
    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
    if data is None:
        fig =  blank_fig() #px.scatter(x=None, y=None)        
        return fig

    
    if(plot_type == 'L'):
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'current', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )  
    elif(plot_type == 'P'):
        fig =  px.scatter(data, 
                       x = 'dtime',
                       y = 'current', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
    else:
        fig =  px.line(data, 
                       x = 'dtime',
                       y = 'current', 
                       color = 'rack_no',
                       text=data['rack_no']
                       )    
                        
    fig.update_layout(title=dict(text="Current Info",
                                 font=dict(color="blue", size=16),
                                 pad=dict(t=0,l=0,b=0,r=0)
                                ) 
                      )
       
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

    fig.update_traces(
                      hovertemplate="<b>Rack:%{text} </b><br><br>"+
                                    "DateTime: %{x} <br>" +
                                    "Voltage: %{y}") 
    
   

    fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
                                      font_size=11,
                                      font_family="Rockwell")
                     )



    # remove facet/subplot labels
    # fig.update_layout(annotations=[], overwrite=True)

    fig.update_layout(
        showlegend=True,
        legend=dict(title=dict(side='left',
                               text='Rack',
                               font=dict(size=10) ) ,
                    font=dict(size=10), #font:color,family,size           
                    bgcolor='white',
                    bordercolor='black',
                    borderwidth=0 ,
                    traceorder = 'normal', #"reversed", "grouped", "reversed+grouped", "normal"
                    itemwidth=30,
                    itemsizing='constant' , # ( "trace" | "constant" )
                    orientation = 'h' , # ( "v" | "h" ) ,
                    valign= 'bottom', # ( "top" | "middle" | "bottom" )
                    x=0.5 ,
                    y=-0.2 ,
                    xanchor='center', #( "auto" | "left" | "center" | "right" )
                    yanchor='top'  #( "auto" | "top" | "middle" | "bottom" )
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
    # fig.update_yaxes(visible=True, fixedrange=True)
    # 마우스 오버시 x , y 라인을 보여줌.
    fig.update_xaxes(showspikes=False, spikecolor="green", spikesnap="cursor", spikemode="across")
    fig.update_yaxes(showspikes=False, spikecolor="orange", spikethickness=2)

    # fig.update_layout(width='100%')
    fig.update_layout(height=400)

    return fig






# #-------- Plot3 Render ------------------------------------------------------------------------------------------
# @app.callback(Output('dash_plot_3'       , 'figure'),
#               Input('dash_btn_load_raw_data', 'n_clicks') ,
#               Input('dash_rdo_plot3_type', 'value'))
# def dash_plot3_render_click(n_clicks, plot_type):
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate
    
#     data = pd.read_parquet('./apps/sample_data/raw_data.parquet')
#     # data = pd.read_json(data, orient='split')
#     # data = data[data['rack_no'].isin([1,2])]
#     data = data.sort_values(by=['rack_no','serial_dt'])
    
#     pio.templates.default = "plotly_white"
#     plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')
    
#     if data is None:
#         fig =  blank_fig() #px.scatter(x=None, y=None)        
#         return fig
    
#     if(plot_type == 'L'):
#         fig =  px.line(data, 
#                        x = 'dtime',
#                        y = 'voltage', 
#                        color = 'rack_no',
#                        text=data['rack_no']
#                        )    
#     elif(plot_type == 'P'):
#         fig =  px.scatter(data, 
#                        x = 'dtime',
#                        y = 'voltage', 
#                        color = 'rack_no',
#                        text=data['rack_no']
#                        )    
#     else: #LP
#         fig =  px.line(data, 
#                        x = 'dtime',
#                        y = 'voltage', 
#                        color = 'rack_no',
#                        text=data['rack_no']
#                        )    
                        
#     fig.update_layout(title=dict(text="Voltage Info",
#                                  font=dict(color="blue", size=16),
#                                  pad=dict(t=0,l=0,b=0,r=0)
#                                 ) 
#                       )
       
#     # markers style
#     fig.update_traces(marker=dict(size=12,
#                                   opacity=0.5 ,
#                                   line=dict(width=1,
#                                            color='DarkSlateGrey')
#                                  ),
#                      selector=dict(mode='markers'))               

#     fig.update_traces(mode="lines")           

#     fig.update_layout(hovermode="closest") # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

#     fig.update_traces(
#                       hovertemplate="<b>Rack:%{text} </b><br><br>"+
#                                     "DateTime: %{x} <br>" +
#                                     "Voltage: %{y}") 
    
   

#     fig.update_layout(hoverlabel=dict(bgcolor="#F1FFFF",
#                                       font_size=11,
#                                       font_family="Rockwell")
#                      )



#     # remove facet/subplot labels
#     # fig.update_layout(annotations=[], overwrite=True)

#     fig.update_layout(
#         showlegend=True,
#         legend=dict(title=dict(side='left',
#                                text='Rack',
#                                font=dict(size=10) ) ,
#                     font=dict(size=10), #font:color,family,size           
#                     bgcolor='white',
#                     bordercolor='black',
#                     borderwidth=0 ,
#                     traceorder = 'normal', #"reversed", "grouped", "reversed+grouped", "normal"
#                     itemwidth=30,
#                     itemsizing='constant' , # ( "trace" | "constant" )
#                     orientation = 'h' , # ( "v" | "h" ) ,
#                     valign= 'bottom', # ( "top" | "middle" | "bottom" )
#                     x=0.5 ,
#                     y=-0.2 ,
#                     xanchor='center', #( "auto" | "left" | "center" | "right" )
#                     yanchor='top'  #( "auto" | "top" | "middle" | "bottom" )
#                     )
#         )

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
#     fig.update_layout(height=500)

#     return fig



# class Databases():
#     def __init__(self):
#         self.db = copg.connect(host='10.252.254.33' , dbname='ess_dev' , user='op_cc09628' , password='Skcc12345678!' , port=5432)
#         self.cursor = self.db.cursor()

#     def __del__(self):
#         self.db.close()
#         self.cursor.close()

#     def execute(self,query,args={}):
#         self.cursor.execute(query,args)
#         row = self.cursor.fetchall()
#         return row

#     def commit(self):
#         self.cursor.commit()
        
# class CRUD(Databases):
#     def insertDB(self,strSQL):
#         try:
#             self.cursor.execute(strSQL)
#             self.db.commit()
#         except Exception as e :
#             print(" insert DB err ",e) 
    
#     def readDB(self,strSQL):
#         try:
#             self.cursor.execute(strSQL)
#             result = self.cursor.fetchall()
#         except Exception as e :
#             result = (" read DB err",e)
        
#         return result

#     def updateDB(self,strSQL):
#         try :
#             self.cursor.execute(strSQL)
#             self.db.commit()
#         except Exception as e :
#             print(" update DB err",e)

#     def deleteDB(self,strSQL):
#         try :
#             self.cursor.execute(strSQL)
#             self.db.commit()
#         except Exception as e:
#             print( "delete DB err", e)

# db = CRUD()

# # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
# sql = "Select A.cyc_date, A.bank_no, A.rack_no From tbl_data_check_10001 A Where A.cyc_date = '20191214' "
# df = db.readDB(sql)





# df = df.sort_values(by="x")

# fig1 = go.Figure(data=[go.Scatter(x=df['serial_dt'] , y=df['current'], color=df['rack_no'])] ,
#                  layout=
#                   {
#                      'title': 'Dash Data Visualization'
#                   }
#                  )
# fig1 = go.Figure()
# fig1.add_trace(go.Scatter(x=df['serial_dt'], y=df['current'] ,color='rack_no',
#                           mode='lines',
#                           name='lines'))
# fig1.add_trace(go.Scatter(x=df['serial_dt'], y=df['voltage'],
#                           mode='lines+markers',
#                           name='lines+markers'))
     