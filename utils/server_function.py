from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from utils.constants import TIMEOUT

import pandas as pd
import plotly.graph_objs as go


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def df_bank():   
    # assign data of lists.  
    lstBank = list(range(1,4))
    data = {'name': lstBank, 'code': lstBank}  
      # Create DataFrame  
    df = pd.DataFrame(data)   
    return df

def df_rack():   
    # assign data of lists.  
    lstRack = list(range(1,29))
    data = {'name': lstRack, 'code': lstRack}  
    # Create DataFrame  
    df = pd.DataFrame(data)   
    return df

def df_module():   
    # assign data of lists.  
    lstModule = list(range(1,7))
    data = {'name': lstModule, 'code': lstModule}  
    # Create DataFrame  
    df = pd.DataFrame(data)   
    return df

def df_cell():   
    # assign data of lists.  
    lstCell = list(range(1,277))
    data = {'name': lstCell, 'code': lstCell}  
      # Create DataFrame  
    df = pd.DataFrame(data)   
    return df


def uf_load_model_list():   
    data = pd.read_csv('./data/model_list.csv')
    data = data[['md_name','md_path','md_filename','md_x_var','md_y_var','md_mae','md_mse','md_rmse','md_desc']]
    return data    




def uf_save_model_list(dModel):   
    data = pd.read_csv('./data/model_list.csv')

    r = (data.md_name == dModel['md_name'])

    if isinstance(dModel['md_x_var'], list) :
        x_str = ','.join(map(str,dModel['md_x_var']))
    else:
        x_str = dModel['md_x_var']
    

    if(len(data.loc[r,:]) < 1) : 
        a_df = pd.DataFrame({'md_name':[dModel['md_name']], 
                             'md_path':[dModel['md_path']],
                             'md_filename':[dModel['md_filename']],
                             'md_x_var':[x_str],
                             'md_y_var':[dModel['md_y_var']],
                             'md_mae'  :[dModel['md_mae']],
                             'md_mse'  :[dModel['md_mse']],
                             'md_rmse' :[dModel['md_rmse']],
                             'md_desc' :[dModel['md_desc']]
                             })
        data = pd.concat([pd.DataFrame(data[['md_name','md_path','md_filename','md_x_var','md_y_var','md_mae','md_mse','md_rmse','md_desc']]) ,
                          pd.DataFrame(a_df)], axis=0)
    else:
        data.loc[r,['md_path','md_filename','md_x_var','md_y_var','md_mae','md_mse','md_rmse','md_desc']]=[dModel['md_path'],dModel['md_filename'],x_str,dModel['md_y_var'],dModel['md_mae'],dModel['md_mse'],dModel['md_rmse'],dModel['md_desc']]

    data = pd.DataFrame(data[['md_name','md_path','md_filename','md_x_var','md_y_var','md_mae','md_mse','md_rmse','md_desc']])

    data.to_csv('./data/model_list.csv')
    return True



