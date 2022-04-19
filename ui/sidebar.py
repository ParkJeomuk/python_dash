import dash_bootstrap_components as dbc
from dash import dcc 
from dash import html
# https://docs-dash-admin-components.herokuapp.com/l/components/sidebar
import dash_admin_components as dac

from utils.constants import MENU_ITEMS 

# Sidebar
subitems = [
    dac.SidebarMenuSubItem(id='menu_gallery_1', 
        label='Gallery 1', 
        icon='arrow-circle-right', 
        badge_label='Soon',
        badge_color='success'
    ), 
    dac.SidebarMenuSubItem(id='menu_gallery_2', 
        label='Gallery 2', 
        icon='arrow-circle-right', 
        badge_label='Soon', 
        badge_color='success'
    )
]
sideMenu = 	dac.SidebarMenu(
    [
        dac.SidebarHeader(children="Data"),
        dac.SidebarMenuItem(id='menu_dash_pages'     ,label='Dash'            , icon='heartbeat'),
        dac.SidebarMenuItem(id='menu_dataset_pages'  ,label='Data Set'        , icon='box'),
        dac.SidebarMenuItem(id='menu_linermd_pages'  ,label='Liner Model'     , icon='chart-line'),
        dac.SidebarMenuItem(id='menu_automl_pages'   ,label='H2O'             , icon='coins'),
        dac.SidebarMenuItem(id='menu_cellsoh_pages'  ,label='SOH'             , icon='battery-half'),
        dac.SidebarMenuItem(id='menu_mars_pages'     ,label='AgingSpeed'      , icon='chart-bar'),
        dac.SidebarMenuItem(id='menu_aging_pages'    ,label='AgingGap'        , icon='bolt'),
        dac.SidebarMenuItem(id='menu_trend_pages'    ,label='AgingTrend'      , icon='chart-bar'),        
        dac.SidebarMenuItem(id='menu_tab_cards'      ,label='Tab cards'       , icon='image'),

        dac.SidebarHeader(children="Boxes"),
        dac.SidebarMenuItem(id='menu_basic_boxes', label='Basic boxes',      icon='desktop'),
        dac.SidebarMenuItem(id='menu_value_boxes', label='Value/Info boxes', icon='suitcase'),

        dac.SidebarHeader(children="Gallery"),
        dac.SidebarMenuItem(label='Galleries', icon='cubes', 
            children=subitems),
    ]
)
sidebar = dac.Sidebar(
    sideMenu,
    title='Becom',
	skin="dark",
    color="primary",
	brand_color="primary",
    url="http://127.0.0.1:8066/dash/",
    #src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    src="assets/logo1.png",
    elevation=0,
    opacity=1
)
