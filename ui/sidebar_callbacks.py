from dash.dependencies import Input, Output, State
from apps import app
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash import html
from utils.constants import MENU_ITEMS
import datetime
import pandas as pd


# =============================================================================
# Callbacks
# =============================================================================

def activate(input_id, 
             dash_pages, 
             dataset_pages, 
             linermd_pages, 
             automl_pages , 
             cellsoh_pages,
             tab_cards, 
             basic_boxes, 
             value_boxes, 
             gallery_1, 
             tab_gallery_2
             ):
    menu_n = len(MENU_ITEMS)
    menu_status = [ False for i in range(menu_n)]
    try:    
        menu_idx = MENU_ITEMS.index(input_id.split( '_', maxsplit=1)[1])    
        menu_status[menu_idx]=True
    except:
        pass
    return menu_status

@app.callback(
    [Output(f"content_{menu}", "active") for menu in MENU_ITEMS],
    [ Input(f'menu_{menu}', 'n_clicks')  for menu in MENU_ITEMS] )
def activate_page_content(dash_pages, 
                          dataset_pages,
                          linermd_pages,
                          automl_pages, 
                          cellsoh_pages,
                          tab_cards, 
                          basic_boxes,
                          value_boxes, 
                          gallery_1, 
                          tab_gallery_2):
    ctx = dash.callback_context # Callback context to recognize which input has been triggered
    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return activate(input_id, 
                    dash_pages, dataset_pages, linermd_pages, automl_pages, cellsoh_pages, tab_cards, basic_boxes, value_boxes, gallery_1, tab_gallery_2)

@app.callback(
    Output('mybread', 'text'),
    [ Input(f"menu_{menu}", "n_clicks") for menu in MENU_ITEMS],
    [ State(f"menu_{menu}", "label")    for menu in MENU_ITEMS] )
def update_breadcrumbs( nClick1, nClick2, nClick3, nClick4, nClick5, nClick6, nClick7, nClick8, nClick9, nClick10,
    dash_pages, dataset_pages, linermd_pages, automl_pages, cellsoh_pages, tab_cards, basic_boxes, value_boxes, gallery_1, gallery_2): 
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0].split('_', maxsplit=1)[1]
    return eval(input_id)


@app.callback(Output("common_modal_popup", "children"),
              Output("common_modal_popup", "is_open" ),
              Input("ds_modal_data"      , "modified_timestamp"),
              State("ds_modal_data"      , "data"))
def uf_show_modal(ts, data):
    if ts is None:
        raise PreventUpdate 
    if data is None:
        raise PreventUpdate     
        
    data = pd.read_json(data, orient='split')
    sTitle   = data['title'] 
    sContent = data['content']
    md = [dbc.ModalHeader(dbc.ModalTitle(sTitle), close_button=True),
          dbc.ModalBody(html.P(sContent, id="common_p", style={'textAlign': 'center', 'padding': 10})),
          dbc.ModalFooter(dbc.Button("Close",id="close-centered",className="ms-auto",n_clicks=0))
         ]

    return md

# @app.callback(Output("ds_modal_data"      , "data"))
def uf_set_modal(sTitle, sContent):
    
    d = {'title':  [sTitle], 'content':  [sContent ]}
    data = pd.DataFrame(data=d, index=[0])

    return data.to_json(date_format='iso' , orient='split')
