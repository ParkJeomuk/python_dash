
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd

 



def cellsoh_data_load(sStartDate, sEndDate, sBankNo, sRackNo, sModuleNo, sCellNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date'] = data['cyc_date'].apply(str)
    data['bank_no'] = data['bank_no'].apply(int)
    data['rack_no'] = data['rack_no'].apply(int)
    data['module_no'] = data['module_no'].apply(int)
    data['cell_no'] = data['cell_no'].apply(int)
    
    data = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] >= sStartDate.replace('-','')) & (data["cyc_date"] <= sEndDate.replace('-','')) ]

    if sRackNo is not None and sRackNo != "" :
            if type(sRackNo) == str:
                data = data[(data["rack_no"]==int(sRackNo))]
            else:
                data = data[data.rack_no.isin(sRackNo)]
            
    if sModuleNo is not None and sModuleNo != "" :
            if type(sModuleNo) == str:
                data = data[(data["module_no"]==int(sModuleNo))]
            else:
                data = data[data.module_no.isin(sModuleNo)]
            
    if sCellNo is not None and sCellNo != "" :
            if type(sCellNo) == str:
                data = data[(data["cell_no"]==int(sCellNo))]
            else:
                data = data[data.cell_no.isin(sCellNo)]

    return data
    