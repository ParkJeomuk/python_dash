
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT
import pandas as pd

 



def dataset_load_data(sDataType, sDate, eDate, sBankNo, sRackNo, sModuleNo, sCellNo):   
    if sDataType == 'C':
        data = pd.read_csv('./data/soh_data.csv')
        data["cyc_date"]  = data["cyc_date"].apply(str)
        data["bank_no"]   = data["bank_no"].apply(str)
        data["rack_no"]   = data["rack_no"].apply(str)
        data["cell_no"]   = data["cell_no"].apply(str)
    else:
        data = ''


    data = data[((data["cyc_date"] >= sDate.replace('-','')) & (data["cyc_date"] <= eDate.replace('-',''))  ) &
                (data["bank_no"] == str(sBankNo)) & 
                (data["rack_no"] == str(sRackNo)) & 
                (data["cell_no"] == str(sCellNo)) ]

    return data

