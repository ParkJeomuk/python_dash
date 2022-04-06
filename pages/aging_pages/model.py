
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT

import pandas as pd
from utils.functions import *

def aging_gap_data_load(sDate1, sDate2, sBankNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date']  = data['cyc_date'].apply(str)
    data['bank_no']   = data['bank_no'].apply(int)
    data['rack_no']   = data['rack_no'].apply(int)
    data['module_no'] = data['module_no'].apply(int)
    data['cell_no']   = data['cell_no'].apply(int)
    
    data1 = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] == sDate1.replace('-','')) ]
    data2 = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] == sDate2.replace('-','')) ]

    df = pd.merge(left= data1[['rack_no','module_no','cell_no','soh','q_a','q_u','cur_avg','n','u_vol','o_vol','gap']], 
                  right=data2[['rack_no','module_no','cell_no','soh','q_a','q_u','cur_avg','n','u_vol','o_vol','gap']], 
                  how="inner", 
                  on=["rack_no","module_no","cell_no"]
                 )

    return df


def aging_data_load(sDate, eDate, sDataType, sBankNo, sRackNo, sModuleNo, sCellNo): 

    data = pd.read_csv('./data/soh_cell.csv')

    data['cyc_date']  = data['cyc_date'].apply(str)
    data['bank_no']   = data['bank_no'].apply(int)
    data['rack_no']   = data['rack_no'].apply(int)
    data['module_no'] = data['module_no'].apply(int)
    data['cell_no']   = data['cell_no'].apply(int)
    
    data = data[(data["bank_no"]==int(sBankNo)) & (data["cyc_date"] >= sDate.replace('-','')) & (data["cyc_date"] <= eDate.replace('-','')) ]

    if sDataType == 'M':
        data = data[(data["rack_no"]==int(sRackNo)) & (data["module_no"]==int(sModuleNo)) ]
    elif sDataType == 'C':
        data = data[(data["rack_no"]==int(sRackNo)) & (data["cell_no"]==int(sCellNo)) ]

    return data