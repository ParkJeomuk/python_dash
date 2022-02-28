
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd

 



def automl_load_train_data(sFilePath):   
    if sFilePath is None:
        raise PreventUpdate

    data = pd.read_pickle(sFilePath)

    return data

def automl_load_test_data(sFilePath):   
    if sFilePath is None:
        raise PreventUpdate

    data = pd.read_pickle(sFilePath)
    
    return data



def automl_load_predict_data(sFilePath):   
    if sFilePath is None:
        raise PreventUpdate

    data = pd.read_csv(sFilePath)
    
    return data

