
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from pyparsing import null_debug_action
from utils.constants import TIMEOUT
import pandas as pd

 



def dataset_load_data(sDataType, sDate, eDate, sBankNo, sRackNo, sModuleNo, sCellNo):   
    
    data = pd.read_csv('./data/soh_data.csv')

    if len(data)>0 :
        data["cyc_date"]  = data["cyc_date"].apply(str)
        data["bank_no"]   = data["bank_no"].apply(str)
        data["rack_no"]   = data["rack_no"].apply(str)
        data["module_no"] = data["module_no"].apply(str)
        data["cell_no"]   = data["cell_no"].apply(str)

        data = data[((data["cyc_date"] >= sDate.replace('-','')) & (data["cyc_date"] <= eDate.replace('-',''))  ) ]

        if sBankNo is not None and sBankNo != '' :
            data = data[(data["bank_no"] == str(sBankNo))]

        if sRackNo is not None and sRackNo != '' :
            data = data[(data["rack_no"] == str(sRackNo))]

        if sModuleNo is not None and sModuleNo != '':
            data = data[(data["module_no"] == str(sModuleNo))]

        if sCellNo is not None and sCellNo != '' :
            data = data[(data["cell_no"] == str(sCellNo))]
    else:
        data = ''
    
    return data

