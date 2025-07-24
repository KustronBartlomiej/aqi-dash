import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import os

# ========== Load dataset ==========
df = pd.read_csv("AQI_dataset.csv")
df["AQI Value"] = pd.to_numeric(df["AQI Value"], errors="coerce")

# ========== Create quick-access lookup ==========
city_data = {row["City"]: row for _, row in df.iterrows()}

# ========== Compute basic stats ==========
avg_aqi = df["AQI Value"].mean()
city_count = df["City"].nunique()

# ========== Create map ==========
map_fig = px.scatter_map(
    df,
    lat="lat",
    lon="lng",
    color="AQI Category",
    hover_name="City",
    hover_data={"AQI Value": ':.0f'},
    zoom=1,
    height=500
)

map_fig.update_layout(
    map_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    font=dict(color="white"),
    legend=dict(
        title="AQI Category",
        x=0.01,
        y=0.99,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(40,40,40,0.7)",
        bordercolor="gray",
        borderwidth=1,
        font=dict(color="white", size=10),
        orientation="v"
    )
)

# ========== Initialize Dash app ==========
app = dash.Dash(__name__)

# Add dark background for full body
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body {
                margin: 0;
                padding: 0;
                background-color: #1e1e1e;
                color: white;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.title = "Global AQI Dashboard"

# ========== Define layout ==========
app.layout = html.Div([
    html.H1("Global AQI Dashboard 🌍", style={
        "textAlign": "center",
        "fontSize": "26px",
        "paddingBottom": "10px"
    }),

    html.Div([
        # === Left: Map & stats ===
        html.Div([
            html.H3(f"Global average AQI: {avg_aqi:.1f}", style={
                "backgroundColor": "#333" if avg_aqi < 100 else "#600",
                "color": "#f1f1f1",
                "padding": "10px",
                "borderRadius": "10px",
                "textAlign": "center",
                "marginBottom": "10px",
                "border": "1px solid #666"
            }),
            html.P(f"Number of cities in dataset: {city_count}", style={"textAlign": "center"}),
            dcc.Graph(id="aqi-map", figure=map_fig, style={"height": "500px", "width": "100%"})
        ], style={
            "flex": "1",
            "minWidth": "300px",
            "padding": "10px",
            "boxSizing": "border-box"
        }),

        # === Right: AQI breakdown ===
        html.Div([
            html.H2("AQI Components Breakdown", style={
                "textAlign": "center",
                "fontSize": "20px"
            }),
            dcc.Graph(id="aqi-details", style={"height": "400px", "width": "100%"})
        ], style={
            "flex": "1",
            "minWidth": "300px",
            "padding": "10px",
            "boxSizing": "border-box"
        }),
    ], style={
        "display": "flex",
        "flexDirection": "row",
        "flexWrap": "wrap",
        "justifyContent": "center",
        "alignItems": "stretch",
        "width": "100%",
        "boxSizing": "border-box"
    })

], style={
    "padding": "10px",
    "maxWidth": "1200px",
    "margin": "auto",
    "boxSizing": "border-box",
    "backgroundColor": "#1e1e1e",
    "color": "#f1f1f1",
    "minHeight": "100vh"
})

# ========== Callback for AQI details ==========
@app.callback(
    Output("aqi-details", "figure"),
    Input("aqi-map", "clickData")
)
def update_details(clickData):
    # Jeśli nic nie kliknięto, pokaż dane dla Warsaw
    if not clickData:
        city = "Warsaw"
    else:
        city = clickData["points"][0]["hovertext"]

    row = city_data.get(city)
    if row is None:
        return px.bar(title=f"No data available for {city}")

    components = {
        "PM2.5": float(row["PM2.5 AQI Value"]),
        "Ozone": float(row["Ozone AQI Value"]),
        "NO2": float(row["NO2 AQI Value"]),
        "CO": float(row["CO AQI Value"])
    }

    fig = px.bar(
        x=list(components.keys()),
        y=list(components.values()),
        labels={"x": "Component", "y": "AQI Value"},
        title=f"AQI Breakdown for: {city}"
    )

    fig.update_layout(
        margin={"l": 40, "r": 20, "t": 50, "b": 30},
        font={"size": 14, "color": "white"},
        height=400,
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e"
    )

    return fig

# ========== Run locally or via Render ==========
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
