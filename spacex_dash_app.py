# Import required libraries
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "site1", "value": "site1"},
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 100: "100"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    print(entered_site)

    if entered_site == "ALL":
        data = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(
            data, values="class", names="Launch Site", title="Successful launches"
        )
        return fig

    else:
        data = (
            spacex_df[spacex_df["Launch Site"] == entered_site]
            .groupby("Launch Site")["class"]
            .sum()
            .reset_index()
        )
        fig = px.pie(data, values="class", names="Launch Site", title="title")
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_payload_plot(entered_site, payload_mass):
    print(entered_site,payload_mass)
    payload_mass_ = payload_mass[0] if payload_mass else None

    if entered_site == "ALL":
        data = spacex_df[spacex_df["Payload Mass (kg)"] == payload_mass] if payload_mass_ else spacex_df
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", title="Scatter")
        return fig

    else:
        data = spacex_df[spacex_df["Launch Site"] == entered_site]
        data = data[data["Payload Mass (kg)"] == payload_mass] if payload_mass_ else data
        fig = px.scatter(data, x="Payload Mass (kg)", y="class", title="Scatter")
        return fig


# Run the app
if __name__ == "__main__":
    app.run()
