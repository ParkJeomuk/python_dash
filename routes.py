from ui.sidebar_callbacks import update_breadcrumbs, activate_page_content

from pages.basic_boxes.callbacks import update_box_graph
from pages.tab_cards.callbacks   import display_tabbox1

from pages.gallery_1.callbacks import make_graph
from pages.gallery_2.callbacks import update_figure




# Dash Page --------------------------------------------------------------------------------
from pages.dash_pages.callbacks    import *
from pages.dataset_pages.callbacks import *
from pages.linermd_pages.callbacks import *
from pages.automl_pages.callbacks  import *
from pages.cellsoh_pages.callbacks import *
from pages.aging_pages.callbacks   import *
from pages.trend_pages.callbacks   import *
from pages.mars_pages.callbacks    import *

# @app.callback(
#     Output("page-content", "children"),
#     [Input("url", "pathname")] )  
#     #[( f"/{menu}", "pathname") for menu in MENU_ITEMS] )
# def render_page_content(pathname):
#     if pathname == menus[MENU_ITEMS.index("home")][1]:
#         return home.layout
#     # elif pathname == gdp_page_location:
#     #     return gdp.layout
#     # elif pathname == iris_page_location:
#     #     return iris.layout
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )