"""
tabs/mapa.py
------------
Mapa interactivo de estaciones y sismos con filtros múltiples.
"""

import os
import numpy as np
import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from utils.data_utils import (
    EVENT_LAT_COL,
    EVENT_LON_COL,
    STATION_LAT_COL,
    STATION_LON_COL,
    SOIL_CLASS_LABELS,
    load_wide_dataset,
)

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DF_CACHE = None

_BASEMAP_OPTIONS = [
    {"label": "OpenStreetMap", "value": "open-street-map"},
    {"label": "Claro (Carto Positron)", "value": "carto-positron"},
    {"label": "Oscuro (Carto Darkmatter)", "value": "carto-darkmatter"},
    {"label": "Topográfico / relieve (USGS)", "value": "usgs-topo"},
]

_LAYER_OPTIONS = [
    {"label": "Estaciones", "value": "stations"},
    {"label": "Sismos", "value": "events"},
    {"label": "Conexiones", "value": "links"},
]


def _get_map_df():
    global _DF_CACHE
    if _DF_CACHE is None:
        df = load_wide_dataset(_BASE).copy()

        # Estandarización defensiva
        if "EQID_Code" in df.columns:
            df["EQID_Code"] = df["EQID_Code"].astype(str)
        if "Station Code" in df.columns:
            df["Station Code"] = df["Station Code"].astype(str)
        if "Soil_Class" in df.columns:
            df["Soil_Class"] = df["Soil_Class"].astype(str)

        for col in ["Magnitude", "Hypocenter Depth (km)", "Rrup_OpenQuake", "Tmax"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        _DF_CACHE = df

    return _DF_CACHE


def _range_bounds(series, pad_frac=0.0):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return 0.0, 1.0

    mn = float(s.min())
    mx = float(s.max())

    if mn == mx:
        return mn - 1.0, mx + 1.0

    pad = (mx - mn) * pad_frac
    return mn - pad, mx + pad


def _range_marks(min_val, max_val, n=5):
    vals = np.linspace(min_val, max_val, n)
    marks = {}

    for v in vals:
        if abs(v) >= 100:
            label = f"{v:.0f}"
        elif abs(v) >= 10:
            label = f"{v:.1f}"
        else:
            label = f"{v:.2f}"
        marks[float(v)] = label

    return marks


def _apply_basemap(fig, basemap):
    if basemap == "usgs-topo":
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": "traces",
                    "sourcetype": "raster",
                    "sourceattribution": "U.S. Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}"
                    ],
                }
            ],
        )
    else:
        fig.update_layout(mapbox_style=basemap, mapbox_layers=[])


def _filter_df(
    df,
    mag_range,
    depth_range,
    rrup_range,
    tmax_range,
    soil_classes,
    eqid_codes,
    station_codes,
):
    mask = pd.Series(True, index=df.index)

    if mag_range:
        mask &= df["Magnitude"].between(mag_range[0], mag_range[1], inclusive="both").fillna(False)

    if depth_range:
        mask &= df["Hypocenter Depth (km)"].between(depth_range[0], depth_range[1], inclusive="both").fillna(False)

    if rrup_range:
        mask &= df["Rrup_OpenQuake"].between(rrup_range[0], rrup_range[1], inclusive="both").fillna(False)

    if tmax_range:
        mask &= df["Tmax"].between(tmax_range[0], tmax_range[1], inclusive="both").fillna(False)

    if soil_classes:
        mask &= df["Soil_Class"].astype(str).isin([str(x) for x in soil_classes])

    if eqid_codes:
        mask &= df["EQID_Code"].astype(str).isin([str(x) for x in eqid_codes])

    if station_codes:
        mask &= df["Station Code"].astype(str).isin([str(x) for x in station_codes])

    return df.loc[mask].copy()


def _build_map(df_filtered, basemap, layers_on):
    links_plot = df_filtered.dropna(
        subset=[EVENT_LAT_COL, EVENT_LON_COL, STATION_LAT_COL, STATION_LON_COL]
    ).copy()

    events_plot = (
        df_filtered[
            ["EQID_Code", "EQID", "Magnitude", "Hypocenter Depth (km)", EVENT_LAT_COL, EVENT_LON_COL]
        ]
        .dropna(subset=[EVENT_LAT_COL, EVENT_LON_COL])
        .drop_duplicates(subset=["EQID_Code", EVENT_LAT_COL, EVENT_LON_COL])
        .copy()
    )

    stations_plot = (
        df_filtered[
            ["Station Code", "Station ID", "Soil_Class", "Soil_Class_label", STATION_LAT_COL, STATION_LON_COL]
        ]
        .dropna(subset=[STATION_LAT_COL, STATION_LON_COL])
        .drop_duplicates(subset=["Station Code", STATION_LAT_COL, STATION_LON_COL])
        .copy()
    )

    fig = go.Figure()

    if "links" in layers_on and not links_plot.empty:
        line_lats = []
        line_lons = []

        for _, row in links_plot.iterrows():
            line_lats.extend([row[EVENT_LAT_COL], row[STATION_LAT_COL], None])
            line_lons.extend([row[EVENT_LON_COL], row[STATION_LON_COL], None])

        fig.add_trace(go.Scattermapbox(
            lat=line_lats,
            lon=line_lons,
            mode="lines",
            name="Conexiones",
            hoverinfo="skip",
            line=dict(color="rgba(120,120,120,0.30)", width=0.6),
        ))

    if "events" in layers_on and not events_plot.empty:
        fig.add_trace(go.Scattermapbox(
            lat=events_plot[EVENT_LAT_COL],
            lon=events_plot[EVENT_LON_COL],
            mode="markers",
            name="Sismos",
            marker=dict(
                size=np.clip(events_plot["Magnitude"].fillna(0) * 3.2, 8, 24),
                color="#e74c3c",
                opacity=0.85,
            ),
            text=events_plot["EQID_Code"].astype(str),
            customdata=np.stack([
                events_plot["Magnitude"].astype(float).fillna(np.nan),
                events_plot["Hypocenter Depth (km)"].astype(float).fillna(np.nan),
            ], axis=-1),
            hovertemplate=(
                "<b>Sismo</b><br>"
                "EQID_Code: %{text}<br>"
                "Magnitud: %{customdata[0]:.2f}<br>"
                "Profundidad: %{customdata[1]:.1f} km"
                "<extra></extra>"
            ),
        ))

    if "stations" in layers_on and not stations_plot.empty:
        fig.add_trace(go.Scattermapbox(
            lat=stations_plot[STATION_LAT_COL],
            lon=stations_plot[STATION_LON_COL],
            mode="markers",
            name="Estaciones",
            marker=dict(size=9, color="#2980b9", opacity=0.9),
            text=stations_plot["Station Code"].astype(str),
            customdata=np.stack([
                stations_plot["Soil_Class"].astype(str),
                stations_plot["Soil_Class_label"].fillna("-").astype(str),
            ], axis=-1),
            hovertemplate=(
                "<b>Estación</b><br>"
                "Código: %{text}<br>"
                "Soil_Class: %{customdata[0]}<br>"
                "Clase: %{customdata[1]}"
                "<extra></extra>"
            ),
        ))

    all_lats = list(events_plot[EVENT_LAT_COL].dropna()) + list(stations_plot[STATION_LAT_COL].dropna())
    all_lons = list(events_plot[EVENT_LON_COL].dropna()) + list(stations_plot[STATION_LON_COL].dropna())

    center_lat = float(np.mean(all_lats)) if all_lats else 4.5
    center_lon = float(np.mean(all_lons)) if all_lons else -74.5

    _apply_basemap(fig, basemap)
    fig.update_layout(
        mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=4.25),
        template="plotly_white",
        height=720,
        margin=dict(l=0, r=0, t=60, b=70),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.85)"
        ),
        title=dict(
            text="Mapa dinámico de estaciones y sismos",
            x=0.5,
            xanchor="center"
        ),
    )

    return fig


def layout():
    df = _get_map_df()

    mag_min, mag_max = _range_bounds(df["Magnitude"])
    dep_min, dep_max = _range_bounds(df["Hypocenter Depth (km)"])
    rrup_min, rrup_max = _range_bounds(df["Rrup_OpenQuake"])
    tmax_min, tmax_max = _range_bounds(df["Tmax"])

    eqid_df = (
        df[["EQID_Code", "EQID"]]
        .dropna(subset=["EQID_Code"])
        .drop_duplicates()
        .sort_values("EQID_Code")
    )

    eqid_options = []
    for _, row in eqid_df.iterrows():
        eqid_code = str(row["EQID_Code"])
        eqid_val = row["EQID"] if "EQID" in row.index else None
        label = eqid_code if pd.isna(eqid_val) else f"{eqid_code} | EQID={eqid_val}"
        eqid_options.append({"label": label, "value": eqid_code})

    station_options = [
        {"label": str(x), "value": str(x)}
        for x in sorted(df["Station Code"].dropna().astype(str).unique())
    ]

    soil_options = [
        {"label": f"{k} — {v}", "value": k}
        for k, v in SOIL_CLASS_LABELS.items()
    ]

    return dbc.Container([
        dbc.Row(dbc.Col([
            html.H2("Mapa interactivo", className="fw-bold mt-4 mb-1", style={"color": "#2c3e50"}),
            html.P(
                "Visualización espacial de estaciones, epicentros y sus conexiones, con filtros dinámicos por variables numéricas y categóricas.",
                className="text-muted lead mb-4"
            ),
            html.Hr(),
        ])),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Controles del mapa", className="mb-0 fw-semibold")),
                dbc.CardBody([
                    html.Label("Fondo cartográfico", className="fw-semibold mb-1"),
                    dcc.Dropdown(
                        id="map-basemap",
                        options=_BASEMAP_OPTIONS,
                        value="open-street-map",
                        clearable=False,
                        className="mb-4"
                    ),

                    html.Label("Capas visibles", className="fw-semibold mb-1"),
                    dcc.Checklist(
                        id="map-layers",
                        options=_LAYER_OPTIONS,
                        value=["stations", "events", "links"],
                        inline=False,
                        className="mb-4"
                    ),

                    html.Label("Magnitud", className="fw-semibold mb-1"),
                    dcc.RangeSlider(
                        id="map-mag-range",
                        min=mag_min,
                        max=mag_max,
                        step=0.1,
                        value=[mag_min, mag_max],
                        marks=_range_marks(mag_min, mag_max),
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="mb-4"
                    ),

                    html.Label("Profundidad hipocentral (km)", className="fw-semibold mb-1"),
                    dcc.RangeSlider(
                        id="map-depth-range",
                        min=dep_min,
                        max=dep_max,
                        step=0.5,
                        value=[dep_min, dep_max],
                        marks=_range_marks(dep_min, dep_max),
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="mb-4"
                    ),

                    html.Label("Rrup (km)", className="fw-semibold mb-1"),
                    dcc.RangeSlider(
                        id="map-rrup-range",
                        min=rrup_min,
                        max=rrup_max,
                        step=1.0,
                        value=[rrup_min, rrup_max],
                        marks=_range_marks(rrup_min, rrup_max),
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="mb-4"
                    ),

                    html.Label("Tmax (s)", className="fw-semibold mb-1"),
                    dcc.RangeSlider(
                        id="map-tmax-range",
                        min=tmax_min,
                        max=tmax_max,
                        step=0.05,
                        value=[tmax_min, tmax_max],
                        marks=_range_marks(tmax_min, tmax_max),
                        tooltip={"placement": "bottom", "always_visible": False},
                        className="mb-4"
                    ),

                    html.Label("Soil_Class", className="fw-semibold mb-1"),
                    dcc.Dropdown(
                        id="map-soil-class",
                        options=soil_options,
                        value=[],
                        multi=True,
                        placeholder="Filtrar por clase de suelo",
                        className="mb-4"
                    ),

                    html.Label("EQID_Code", className="fw-semibold mb-1"),
                    dcc.Dropdown(
                        id="map-eqid",
                        options=eqid_options,
                        value=[],
                        multi=True,
                        placeholder="Filtrar por EQID_Code",
                        className="mb-4"
                    ),

                    html.Label("Station Code", className="fw-semibold mb-1"),
                    dcc.Dropdown(
                        id="map-station-code",
                        options=station_options,
                        value=[],
                        multi=True,
                        placeholder="Filtrar por Station Code",
                        className="mb-0"
                    ),
                ])
            ], className="shadow-sm border-0 h-100"), md=4, className="mb-4"),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Visualización", className="mb-0 fw-semibold")),
                dbc.CardBody(
                    dcc.Graph(id="stations-events-map", config={"displayModeBar": False})
                )
            ], className="shadow-sm border-0"), md=8, className="mb-4"),
        ]),
    ], fluid=True)


@callback(
    Output("stations-events-map", "figure"),
    Input("map-basemap", "value"),
    Input("map-layers", "value"),
    Input("map-mag-range", "value"),
    Input("map-depth-range", "value"),
    Input("map-rrup-range", "value"),
    Input("map-tmax-range", "value"),
    Input("map-soil-class", "value"),
    Input("map-eqid", "value"),
    Input("map-station-code", "value"),
)
def update_map(
    basemap,
    layers_on,
    mag_range,
    depth_range,
    rrup_range,
    tmax_range,
    soil_classes,
    eqid_codes,
    station_codes,
):
    df = _get_map_df()

    df_filtered = _filter_df(
        df=df,
        mag_range=mag_range,
        depth_range=depth_range,
        rrup_range=rrup_range,
        tmax_range=tmax_range,
        soil_classes=soil_classes or [],
        eqid_codes=eqid_codes or [],
        station_codes=station_codes or [],
    )

    return _build_map(df_filtered, basemap, layers_on or [])