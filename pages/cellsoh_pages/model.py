
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd

 



def cellsoh_data_load(sStartDate, sEndDate, sBankNo, sRackNo, sModuleNo, sCellNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date'] = data['cyc_date'].apply(str)
    data['bank_no'] = data['bank_no'].apply(str)
    data['rack_no'] = data['rack_no'].apply(str)
    data['module_no'] = data['module_no'].apply(str)
    data['cell_no'] = data['cell_no'].apply(str)
    
    data = data[(data["bank_no"]==sBankNo) & (data["cyc_date"] >= sStartDate.replace('-','')) & (data["cyc_date"] <= sEndDate.replace('-','')) ]

    if sRackNo is not None and sRackNo != "" :
            data = data[(data["rack_no"] == str(sRackNo))]
            
    if sModuleNo is not None and sModuleNo != "" :
            data = data[(data["module_no"] == str(sModuleNo))]
            
    if sCellNo is not None and sCellNo != "" :
            data = data[(data["cell_no"] == str(sCellNo))]
            
    return data
    