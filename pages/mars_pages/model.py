
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd
from utils.functions import *

def mars_data_load(sDate1, sDate2, sBankNo, sRackNo): 

    data = pd.read_csv('./data/mars_soh.csv')

    # data = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] >= sDate1.replace('-','')) & (data["cyc_date"] <= sDate2.replace('-','')) ]

    return data

 


def mars_raw_data_load(sDate,eDate, sBankNo, sRackNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date']  = data['cyc_date'].apply(str)
    data['bank_no']   = data['bank_no'].apply(int)
    data['rack_no']   = data['rack_no'].apply(int)
    
    data = data[(data["bank_no"]==int(sBankNo)) & (data["rack_no"]==int(sRackNo)) & (data["cyc_date"] >= sDate.replace('-',''))& (data["cyc_date"] <= eDate.replace('-',''))  ]

    return data
