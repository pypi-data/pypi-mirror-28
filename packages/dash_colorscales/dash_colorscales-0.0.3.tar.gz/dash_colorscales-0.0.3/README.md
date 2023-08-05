# dash-colorscales

Colorscale picker UI for your Dash apps

## Dash

Go to this link to learn about [Dash](https://plot.ly/dash/).

## Getting started

```sh
pip install dash_colorscales
```

## Basic Dash App using the colorscale picker

```
import dash_colorscales
import dash
import dash_html_components as html
import json

app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
    dash_colorscales.DashColorscales(
        id='colorscale-picker',
        nSwatches=7,
        fixSwatches=True
    ),
    html.P(id='output', children='')
])

@app.callback(
        dash.dependencies.Output('output', 'children'),
        [dash.dependencies.Input('colorscale-picker', 'colorscale')])
def display_output(colorscale):
    return json.dumps(colorscale)

if __name__ == '__main__':
    app.run_server(debug=True)
```