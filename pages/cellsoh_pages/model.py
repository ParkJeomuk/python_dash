
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd
from utils.functions import *
 



def cellsoh_data_load(sStartDate, sEndDate, sBankNo, sRackNo, sModuleNo, sCellNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date'] = data['cyc_date'].apply(str)
    data['bank_no'] = data['bank_no'].apply(int)
    data['rack_no'] = data['rack_no'].apply(int)
    data['module_no'] = data['module_no'].apply(int)
    data['cell_no'] = data['cell_no'].apply(int)
    
    data = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] >= sStartDate.replace('-','')) & (data["cyc_date"] <= sEndDate.replace('-','')) ]

    if uf_is_empty(sRackNo) == False :
            if type(sRackNo) == str:
                data = data[(data["rack_no"]==int(sRackNo))]
            else:
                data = data[data.rack_no.isin(sRackNo)]
            
    if uf_is_empty(sModuleNo) == False :
            if type(sModuleNo) == str:
                data = data[(data["module_no"]==int(sModuleNo))]
            else:
                data = data[data.module_no.isin(sModuleNo)]
            
    if uf_is_empty(sCellNo) == False :
            if type(sCellNo) == str:
                data = data[(data["cell_no"]==int(sCellNo))]
            else:
                data = data[data.cell_no.isin(sCellNo)]

    return data
    

