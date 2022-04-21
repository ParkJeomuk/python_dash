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
from   plotly.subplots import make_subplots
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
from pages.mars_pages.model import *


def uf_scale_mm_calc (data):
    if data is None:
        raise PreventUpdate
    
    rtn = (data - min(data)) / (max(data) - min(data))

    return rtn



def uf_mars_calc (data):
    if data is None:
        raise PreventUpdate
    if len(data)<1 :
        raise PreventUpdate

    return data



@app.callback(Output('ds_mars_df'        , 'data'      ),
              Output('ds_mars_pie'       , 'data'      ),
              Output('loading_mars_1'    , 'children'  ),
              Input('btn_mars_dataload'  , 'n_clicks'  ),
              State('date_range_mars'    , 'start_date'), 
              State('date_range_mars'    , 'end_date'  ), 
              State('cbo_mars_bank'      , 'value'     ),
              State('cbo_mars_rack'      , 'value'     )  
              )
def cb_mars_data_load(n_clicks, s_date, e_date , s_bank_no , s_rack_no ):
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
    
    data_cuts = (18619,18619,18815,18500,18717)
    data_cuts = list(set(data_cuts))
    data_cuts = np.array(data_cuts)
    data_cuts = pd.DataFrame(data_cuts)
    data_cuts[1]=''
    data_cuts = data_cuts.rename(columns={0:'no',1:'cyc_date'})

    data = mars_data_load(s_date, e_date, s_bank_no, s_rack_no)
    df = uf_mars_calc(data)

    raw_data = mars_raw_data_load(s_date, e_date, s_bank_no, s_rack_no)
    raw_data = raw_data.dropna(axis=0) #NA Omit

    df_pie = raw_data[['cyc_date','soh','q_u','cur_avg','n','u_vol','o_vol','gap']].groupby(['cyc_date'],as_index=False).mean()
    df_pie['cls']=''
    date_df = pd.DataFrame()
   
    for item in data_cuts.iterrows():
        add_day = int(item[1][0])
        tmp_date = (datetime.strptime("1970-01-01", "%Y-%m-%d") + timedelta(days=add_day))
        temp_row = {'no':item[1][0] ,'cyc_date':tmp_date}
        date_df = date_df.append(temp_row, ignore_index=True)
    
    date_df = date_df.sort_values(by=['no'])    
    date_df['cyc_date'].apply(str)
    cnt = 0
    df_pie['cyc_date'] = pd.to_datetime(df_pie['cyc_date'], format='%Y%m%d')

    for item in date_df.iterrows():
        cnt = cnt + 1
        df_pie.loc[ ((df_pie.cyc_date<item[1][1]) & (df_pie.cls == '')),"cls" ] = cnt
    
    df_pie.loc[ (df_pie.cls == ''),"cls" ] = cnt+1
    df_pie = df_pie[['cls','soh','q_u','cur_avg','n','u_vol','o_vol','gap']].groupby(['cls'], as_index=False).mean()

    pie_data = {'q_u':uf_scale_mm_calc(df_pie.loc[:,"q_u"]),
                'cur_avg':uf_scale_mm_calc(df_pie.loc[:,"cur_avg"]),
                'n':uf_scale_mm_calc(df_pie.loc[:,"n"]),
                'u_vol':uf_scale_mm_calc(df_pie.loc[:,"u_vol"]),
                'o_vol':uf_scale_mm_calc(df_pie.loc[:,"o_vol"]),
                'gap':uf_scale_mm_calc(df_pie.loc[:,"gap"])}
    df_pie = pd.DataFrame(pie_data)
    df_pie.index = df_pie.index+1

    df_pie = df_pie.transpose()

    # rowname = pd.DataFrame({'item_name': df_pie.index.values.tolist()})
    df_pie.insert(len(df_pie.columns), "item_name",df_pie.index.values.tolist())

    return df.to_json(date_format='iso',orient='split') , df_pie.to_json(date_format='iso',orient='split') ,''



 


######################################################################################
## Render Plot 1
######################################################################################
@app.callback(Output('mars_plot_1' , 'figure'   ),
              Output("mars_plot_2" , "figure"   ) ,
            #   Output("mars_plot_3" , "figure"   ) ,
            #   Output("mars_plot_4" , "figure"   ) ,
            #   Output("mars_plot_5" , "figure"   ) ,
            #   Output("mars_plot_6" , "figure"   ) ,
              Input('ds_mars_df'   , 'modified_timestamp'),
              State('ds_mars_df'   , 'data'     ),
              State('ds_mars_pie'  , 'data'     )
              )
def cb_mars_plot1_render( ts, data, pie_data):
    if ts is None or data is None:
        raise PreventUpdate


    data = pd.read_json(data, orient='split')
    data = data.dropna(axis=0)
    
    pie_df = pd.read_json(pie_data, orient='split')
    pie_df = pie_df.dropna(axis=0)

    pio.templates.default = "plotly_white"
    plot_template = ('plotly','ggplot2', 'seaborn', 'simple_white', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff','ygridoff', 'gridon', 'none')

    if data is None or len(data)<1:
        fig =  blank_fig()
        return fig , fig  

    data['cyc_date'] = pd.to_datetime(data['cyc_date'], format='%Y%m%d')

    data_cuts = (1,18500,18619,18717,18815)
    # data_cuts = (18619,18619,18815,18500,18717)

    fig1 = px.scatter(data, 
                      x="cyc_date", 
                      y="soh", 
                      title='Divide SOH Trend' )
    
    fig1.update_traces(mode='lines+markers')
    
    fig1.update_layout(hovermode="closest")
    fig1.update_layout(showlegend=False)

    date_cnt = 0
    for i in data_cuts:
        date_cnt = date_cnt + 1
        if date_cnt == 1 :
            t_date = data.loc[0,'cyc_date']
        else:
            t_date = datetime.strptime("1970-01-01", "%Y-%m-%d") + timedelta(days=i)

        ann_text = "Class" + str(date_cnt)

        fig1.add_vline(x=t_date, 
                       line_width=2, 
                       line_dash="dash", 
                       line_color="green" )

        fig1.add_annotation(
            x=t_date + timedelta(days=20) ,
            y=max(data.soh.values),
            text= ann_text ,
            font=dict(size=24,color="#ffffff"),
            align="right",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
            )

    # fig1.update_layout(annotations=[{**a, **{"y":.5}}  for a in fig.to_dict()["layout"]["annotations"]])    
    
    # fig1.update_layout(yaxis_range=[3,7])
    fig1.update_layout(height=680)

    labels =np.array(pie_df.item_name.values).tolist()

    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'},{}]]
    fig2 = make_subplots(rows=2, cols=3, specs=specs)
    fig2.add_trace(go.Pie(labels=labels, values=np.array(pie_df.iloc[:,0].values).tolist(), name="Class 1"), 1, 1)
    fig2.add_trace(go.Pie(labels=labels, values=np.array(pie_df.iloc[:,1].values).tolist(), name="Class 2"), 1, 2)
    fig2.add_trace(go.Pie(labels=labels, values=np.array(pie_df.iloc[:,2].values).tolist(), name="Class 3"), 1, 3)
    fig2.add_trace(go.Pie(labels=labels, values=np.array(pie_df.iloc[:,3].values).tolist(), name="Class 4"), 2, 1)
    fig2.add_trace(go.Pie(labels=labels, values=np.array(pie_df.iloc[:,4].values).tolist(), name="Class 5"), 2, 2)


    # Use `hole` to create a donut-like pie chart
    fig2.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig2.update_layout(
        title_text="Detail Variable",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Class1', x=0.12, y=0.82, font_size=18, showarrow=False),
                     dict(text='Class2', x=0.50, y=0.82, font_size=18, showarrow=False),
                     dict(text='Class3', x=0.88, y=0.82, font_size=18, showarrow=False),
                     dict(text='Class4', x=0.12, y=0.18, font_size=18, showarrow=False),
                     dict(text='Class5', x=0.50, y=0.18, font_size=18, showarrow=False)
                    ])


    # fig2 = px.pie(pie_df, values=1, names='item_name', title='1')
    # fig2.update_layout(hovermode="closest")
    # fig2.update_layout(showlegend=False)

    # fig3 = px.pie(pie_df, values=2, names='item_name', title='2')
    # fig3.update_layout(hovermode="closest")
    # fig3.update_layout(showlegend=False)

    # fig4 = px.pie(pie_df, values=3, names='item_name', title='3')
    # fig4.update_layout(hovermode="closest")
    # fig4.update_layout(showlegend=False)

    # fig5 = px.pie(pie_df, values=4, names='item_name', title='4')
    # fig5.update_layout(hovermode="closest")
    # fig5.update_layout(showlegend=False)

    # fig6 = px.pie(pie_df, values=5, names='item_name', title='5')
    # fig6.update_layout(hovermode="closest")
    # fig6.update_layout(showlegend=False)

    return fig1 , fig2 


 

 



#======================================================================================================================
#---------------- R Source ---------------------------------------------
#======================================================================================================================
# #- m3 (Apply Mars!!!) -Added 2020.04.04

# library(earth) 
# s1 <-filter(T_soh,rack_no == 8)

# s11 <-slice(s1,-which(is.na(s1$soh))) # na 
# s11$cyc_date<-ymd(s11$cyc_date) # change data type 
# range(s11$cyc_date)

# par(mfrow=c(1,1)) #<- Poltting Selected 

# plot(s11$cyc_date, s11$soh,pch=16, main="Original of Rack #8") 
# grid()

# t_s11<-reshape2::dcast(s11 cell_no-cyc_date, value.var = "soh", mean) #<- mean of soh
# train<-data.frame(cyc_date=names(t_$11)[-1] %>% ymd,soh=day_avg<-apply(t_s11(-1),2,mean))
# m3 <-earth(soh-cyc_date,train) # make mars Modol 

# summary(m3) 
# m3$cuts 
# p_mar<-predict( m3, train) # same(=Model Train) data predicr

# plot(train$cyc_date,p_mar) 
# grid()
# abline(v=m3$cuts,Ity=3,col=3)

# aggr_s11<-aggregate(cbind(soh,q_u,cur_avg, n, u_vol,o_vol,gap) ~ cyc_date, data = $11, mean) 
# c_t<-as.integer(m3$cuts[,1])(-1) %>% sort() %>% unique()

# class<-rep(5.dim(aggr_s11)[1])
# for(i in c(4:1)){
#     class[1:which(aggr_s11$cyc_date == c_t[i])]<-i
# }

# table(class) 
# aggr_s11<-mutate(aggr_s11.class=class)

# aggr_by_class<-lapply(group_split(aggr_s11.class), function(L){ 
#     data.frame(class=L$class[1],
#                q_u=mean(L$q_u),
#                cur_avg=mean(L$cur_avg),
#                n=mean(L$n),
#                u_vol=mean(L$u_vol), 
#                o_vol=mean($o_vol),
#                gap=mean($gap)) 
# }) %>% rbindlist()

# scale_mm<-function(x){ (x-min(x))/(max(x)-min(x))  }

# a21<-apply(aggr_by_class[,-1],2,scale_mm) %>% as.data.frame()

# par(mfrow=c(3,2)) 
# lapply(c(1:5), function(x){ 
#     pie(as.numeric(a21[x,]) ,
#     labels = names(a21), 
#     edges = 2000,
#     radius = 1.0
#     main=x)
# })

# names(a21)
#======================================================================================================================