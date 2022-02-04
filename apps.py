import dash
import dash_bootstrap_components as dbc
# import uvicorn as uvicorn
# from fastapi import FastAPI

from utils.external_assets import ROOT, EXTERNAL_STYLESHEETS, FONT_AWSOME

#-------- Flask --------------------------------------------
import flask
# from flask_caching import Cache

#-------- FastAPI ------------------------------------------
# from fastapi import FastAPI
# from starlette.middleware.wsgi import WSGIMiddleware



from ui.main import layout
# =============================================================================
# Dash App and Flask Server
# =============================================================================



server = flask.Flask(__name__)

# server = FastAPI()


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

# server.mount("/dash", WSGIMiddleware(app.server))
# uvicorn.run(server)

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

