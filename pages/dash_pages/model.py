
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from utils.constants import TIMEOUT
import pandas as pd



    
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
    # data = pd.read_csv('./data/raw_data.csv')
    data = pd.read_csv('./data/big_data.csv')
    data = data.iloc[0:6000000, [3,4,5,6,7,15,21,30]]
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



def df_dash_data_box(): 
    data = dataTable_column = pd.DataFrame({
                                            'bank_no'       : [1,2,3] ,
                                            'voltage'       : [1075.1, 1065.3, 1074.3],
                                            'voltage_per'   : [90, 91.1, 92.2],
                                            'current_c'     : [17, 18, 17.5],
                                            'current_c_per' : [96, 97.1, 95.2],
                                            'current_d'     : [24.1, 23.5, 24.5],
                                            'current_d_per' : [96, 97.1, 95.2],
                                            'charge_q'      : [106.2, 105.4, 109.8],
                                            'charge_q_per'  : [93, 94.1, 95.3],
                                            'datacount'     : [43200,43201,43202],
                                            'datacount_per' : [100,99.8,100],
                                            'datafail'      : [0,0,0] ,
                                            'datafail_per'  : [0,0,0]
                                        })
    return data