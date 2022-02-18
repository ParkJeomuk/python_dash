
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
