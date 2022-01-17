
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from utils.constants import TIMEOUT
import pandas as pd


def df_bank():   
    # assign data of lists.  
    data = {'name': ['1', '2', '3'], 'code': [1, 2, 3]}  
      # Create DataFrame  
    df = pd.DataFrame(data)   
    return df


def df_dash_data():   
    data = pd.read_csv('./apps/sample_data/ppp.csv')
    return data.to_json(date_format='iso' , orient='split')









