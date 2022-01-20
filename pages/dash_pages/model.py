
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

def df_data_type():   
    # assign data of lists.  
    data = {'name': ['Comparison', 'Period'], 'code': ['C','P']}  
      # Create DataFrame  
    df = pd.DataFrame(data)   
    return df

def df_dash_data():   
    data = pd.read_csv('./data/ppp.csv')
    # return data.to_json(date_format='iso' , orient='split')
    return data

def df_dash_raw_data():   
    data = pd.read_csv('./data/raw_data.csv')
    # return data.to_json(date_format='iso' , orient='split')
    return data

def df_dash_q_data():   
    data = pd.read_csv('./data/q_data.csv')
    # return data.to_json(date_format='iso' , orient='split')
    return data


def df_dash_polar_data():   
    data = pd.read_csv('./data/gradar.csv')
    return data


def df_dash_data_table_list():   
    data = pd.read_csv('./data/data_table.csv')
    return data
