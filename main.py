import dash
import dash_bootstrap_components as dbc
from dash import html, Output, Input
from dash.exceptions import PreventUpdate

from utils import calc_elos

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])
server = app.server

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.B(""), className='col-md-1'),
                dbc.Col(html.B("Elo"), className='col-md-2'),
                dbc.Col(html.B("Broj odigranih meceva"), className='col-md-2'),
                dbc.Col(html.B("Set 1"), className='col-md-1'),
                dbc.Col(html.B("Set 2"), className='col-md-1'),
                dbc.Col(html.B("Set 3"), className='col-md-1'),
                dbc.Col(html.B("Novi Elo"), className='col-md-1'),
                dbc.Col(html.B("Razlika"), className='col-md-1'),
            ], className="mt-5 mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(html.B("Igrac 1"), className='col-md-1'),
                dbc.Col(dbc.Input(id="elo1", type="number", min=0, step=0.01, placeholder=1432.33),
                        className='col-md-2'),
                dbc.Col(dbc.Input(id="matches1", type="number", min=0, step=1, placeholder=66), className='col-md-2'),
                dbc.Col(dbc.Input(id="set11", type="number", min=0, max=7, step=1, placeholder=6),
                        className='col-md-1'),
                dbc.Col(dbc.Input(id="set12", type="number", min=0, max=7, step=1, placeholder=7),
                        className='col-md-1'),
                dbc.Col(dbc.Input(id="set13", type="number", min=0, max=10, step=1), className='col-md-1'),
                dbc.Col(html.H4(id="novi-elo1"), className='col-md-1', style={"color": "blue"}),
                dbc.Col(id="razlika1"),
            ], className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(html.B("Igrac 2"), className='col-md-1'),
                dbc.Col(dbc.Input(id="elo2", type="number", min=0, step=0.01, placeholder=1329.68),
                        className='col-md-2'),
                dbc.Col(dbc.Input(id="matches2", type="number", min=0, step=1, placeholder=18), className='col-md-2'),
                dbc.Col(dbc.Input(id="set21", type="number", min=0, max=7, step=1, placeholder=4),
                        className='col-md-1'),
                dbc.Col(dbc.Input(id="set22", type="number", min=0, max=7, step=1, placeholder=6),
                        className='col-md-1'),
                dbc.Col(dbc.Input(id="set23", type="number", min=0, max=10, step=1), className='col-md-1'),
                dbc.Col(html.H4(id="novi-elo2"), className='col-md-1', style={"color": "blue"}),
                dbc.Col(id="razlika2"),
            ]
        ),
    ]
)


@app.callback(
    Output(component_id='novi-elo1', component_property='children'),
    Output(component_id='novi-elo2', component_property='children'),
    Output(component_id='razlika1', component_property='children'),
    Output(component_id='razlika2', component_property='children'),
    Input(component_id='elo1', component_property='value'),
    Input(component_id='matches1', component_property='value'),
    Input(component_id='set11', component_property='value'),
    Input(component_id='set12', component_property='value'),
    Input(component_id='set13', component_property='value'),
    Input(component_id='elo2', component_property='value'),
    Input(component_id='matches2', component_property='value'),
    Input(component_id='set21', component_property='value'),
    Input(component_id='set22', component_property='value'),
    Input(component_id='set23', component_property='value'),
)
def update_output_div(elo1, matches1, set11, set12, set13,
                      elo2, matches2, set21, set22, set23):
    if not (elo1 and elo2 and matches1 and matches2 and set11 and set21 and set12 and set22):
        raise PreventUpdate

    match_result = [(set11, set21), (set12, set22)]
    if set13 and set23:
        match_result.append((set13, set23))

    a, b = calc_elos(elo1, matches1, elo2, matches2, match_result)

    if a > elo1:
        a_diff = get_diff_div(a - elo1, "green", "+")
    else:
        a_diff = get_diff_div(elo1 - a, "red", "-")

    if b > elo2:
        b_diff = get_diff_div(b - elo2, "green", "+")
    else:
        b_diff = get_diff_div(elo2 - b, "red", "-")

    return round(a, 0), round(b, 0), a_diff, b_diff


def get_diff_div(diff, color, sign):
    return dbc.Col(html.H4(f"{sign}{round(diff, 2)}"), className='col-md-1', style={"color": color})


if __name__ == "__main__":
    app.run_server()

if __name__ == '__main__':
    app.run_server(debug=True)
