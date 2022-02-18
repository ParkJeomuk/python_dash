import dash
import dash_bootstrap_components as dbc

from utils.external_assets import ROOT, EXTERNAL_STYLESHEETS, FONT_AWSOME

#-------- Flask --------------------------------------------
import flask

from ui.main import layout
# =============================================================================
# Dash App and Flask Server
# =============================================================================
server = flask.Flask(__name__)




app = dash.Dash(
    name= __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    requests_pathname_prefix="/dash/",
    assets_folder = ROOT+"/assets/", 
    title = "BECOM",
    suppress_callback_exceptions=True, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP  , 
        FONT_AWSOME,
        #EXTERNAL_STYLESHEETS
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)


# cfg = {
#     'DEBUG' : True,
#     'CACHE_TYPE': 'filesystem',
#     'CACHE_DIR': 'cache-directory',
#     'CACHE_DEFAULT_TIMEOUT': 666
# }
# cache = Cache(app.server, config=cfg)

server = app.server 
# =============================================================================
# Dash Admin Components
# =============================================================================
app.layout = layout

