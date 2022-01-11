from apps import app
from dash.dependencies      import Input, Output, State

from components.example_plots     import plot_scatter

# Update figure on slider change
@app.callback(
    Output('box-graph', 'figure'),
    [Input('controlbar-slider', 'value')] )
def update_box_graph(value):
    return plot_scatter(value)
