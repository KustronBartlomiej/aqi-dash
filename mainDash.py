import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ========== Load dataset ==========
df = pd.read_csv("D:\\VisualStudio\\GitHub\\Kaggle\\AQI_dataset.csv")
df["AQI Value"] = pd.to_numeric(df["AQI Value"], errors="coerce")

# ========== Create a quick-access dictionary keyed by city ==========
city_data = {row["City"]: row for _, row in df.iterrows()}

# ========== Calculate global statistics ==========
avg_aqi = df["AQI Value"].mean()
city_count = df["City"].nunique()

# ========== Generate interactive map using OpenStreetMap ==========
map_fig = px.scatter_map(
    df,
    lat="lat",
    lon="lng",
    color="AQI Category",
    hover_name="City",
    hover_data={"AQI Value": ':.0f'},
    zoom=1,
    height=600
)
map_fig.update_layout(map_style="open-street-map", margin={"r": 0, "t": 50, "l": 0, "b": 0})

# ========== Initialize Dash application ==========
app = dash.Dash(__name__)
app.title = "Global AQI Dashboard"

# ========== Define layout of the dashboard ==========
app.layout = html.Div([
    html.H1("Global Air Quality Index (AQI) Dashboard 🌍", style={"textAlign": "center"}),

    html.Div([

        # ========== Left panel: Map and basic statistics ==========
        html.Div([
            html.H3(f"Global average AQI: {avg_aqi:.1f}", style={
                "backgroundColor": "#f9c74f" if avg_aqi < 100 else "#f94144",
                "padding": "10px",
                "borderRadius": "10px",
                "textAlign": "center",
                "marginBottom": "10px"
            }),
            html.P(f"Number of cities in dataset: {city_count}"),
            dcc.Graph(id="aqi-map", figure=map_fig, style={"height": "600px", "width": "100%"})
        ], style={
            "flex": "2",
            "paddingRight": "20px",
            "boxSizing": "border-box"
        }),

        # ========== Right panel: AQI breakdown per component ==========
        html.Div([
            html.H2("AQI Components Breakdown", style={"textAlign": "center"}),
            dcc.Graph(id="aqi-details", style={"height": "400px", "width": "100%"})
        ], style={
            "flex": "1",
            "paddingLeft": "20px",
            "boxSizing": "border-box",
            "borderLeft": "1px solid #ccc"
        })

    ], style={
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "space-between",
        "alignItems": "flex-start",
        "width": "100%",
        "maxWidth": "100%",
        "flexWrap": "nowrap"
    })

], style={
    "padding": "20px",
    "width": "100%",
    "maxWidth": "100%",
    "boxSizing": "border-box"
})

# ========== Callback to update AQI component breakdown when a city is clicked ==========
@app.callback(
    Output("aqi-details", "figure"),
    Input("aqi-map", "clickData")
)
def update_details(clickData):
    if not clickData:
        return px.bar(title="Click a city on the map to see AQI breakdown")

    city = clickData["points"][0]["hovertext"]
    row = city_data.get(city)
    if row is None:
        return px.bar(title="No data available for this city")

    # ========== Extract AQI components for the selected city ==========
    components = {
        "PM2.5": float(row["PM2.5 AQI Value"]),
        "Ozone": float(row["Ozone AQI Value"]),
        "NO2": float(row["NO2 AQI Value"]),
        "CO": float(row["CO AQI Value"])
    }

    # ========== Create a bar chart for the AQI breakdown ==========
    fig = px.bar(
        x=list(components.keys()),
        y=list(components.values()),
        labels={"x": "Component", "y": "AQI Value"},
        title=f"AQI Breakdown for: {city}"
    )
    return fig

# ========== Run the Dash app ==========
if __name__ == "__main__":
    app.run(debug=True)
