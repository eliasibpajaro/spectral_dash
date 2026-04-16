"""
tabs/prediccion.py
------------------
Formulario interactivo para predicción en tiempo real de Sa(T=0.01 s).
Usa el mismo esquema de variables que el pipeline entrenado con XGBoost.
"""

import os
import joblib
import numpy as np
import pandas as pd
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from tabs.resultados import _META_PATH
from utils.data_utils import SOIL_CLASS_LABELS, load_wide_dataset

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODEL_PATH = os.path.join(_BASE, "model", "model.pkl")

_SOIL_OPTIONS = [
    {"label": f"{k} — {v}", "value": k}
    for k, v in SOIL_CLASS_LABELS.items()
]

_pipeline_cache = None
_context_df_cache = None
_meta_cache = None

def _get_pipeline():
    global _pipeline_cache
    if _pipeline_cache is None:
        _pipeline_cache = joblib.load(_MODEL_PATH)
    return _pipeline_cache

def _get_meta():
    global _meta_cache
    if _meta_cache is None:
        _meta_cache = joblib.load(_META_PATH)
    return _meta_cache

def _get_context_df():
    global _context_df_cache
    if _context_df_cache is None:
        _context_df_cache = load_wide_dataset(_BASE)
    return _context_df_cache


def _engineer(mag, rrup, depth, soil_class):
    mag = float(mag)
    rrup = float(rrup)
    depth = float(depth)
    soil_class = str(soil_class)

    log_rrup = np.log(max(rrup, 1e-6))

    return pd.DataFrame({
        "Magnitude": [mag],
        "Rrup_OpenQuake": [rrup],
        "Hypocenter Depth (km)": [depth],
        "log_Rrup": [log_rrup],
        "Mag_logRrup": [mag - log_rrup],
        "Mag2": [mag ** 2],
        "log_Depth": [np.log(max(depth, 1.0))],
        "Soil_Class": pd.Categorical([soil_class], categories=list(SOIL_CLASS_LABELS.keys())),
    })


def layout():
    meta = _get_meta()
    best_model_name = meta.get("best_model_name", "No disponible")

    return dbc.Container([

        dbc.Row(dbc.Col([
            html.H2("Predicción interactiva",
                    className="fw-bold mt-4 mb-1", style={"color": "#2c3e50"}),
            html.P("Ingrese los parámetros sísmicos para predecir Sa(T=0.01 s) en tiempo real",
                className="text-muted lead mb-3"),
            dbc.Alert([
                html.Strong("Modelo activo de predicción: "),
                best_model_name
            ], color="info", className="py-2 mb-3"),
            html.Hr(),
        ])),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("Parámetros de entrada",
                                       className="mb-0 fw-semibold")),
                dbc.CardBody([
                    html.Label("Magnitud Momento (Mw)", className="fw-semibold mb-1"),
                    dcc.Slider(
                        id="pred-magnitude", min=4.5, max=7.0, step=0.05, value=5.5,
                        marks={v: str(v) for v in [4.5, 5.0, 5.5, 6.0, 6.5, 7.0]},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="mb-4"
                    ),

                    html.Label("Distancia a ruptura — Rrup (km)", className="fw-semibold mb-1"),
                    dcc.Slider(
                        id="pred-rrup", min=10, max=360, step=5, value=100,
                        marks={v: str(v) for v in [10, 50, 100, 150, 200, 300, 360]},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="mb-4"
                    ),

                    html.Label("Profundidad hipocentral (km)", className="fw-semibold mb-1"),
                    dcc.Slider(
                        id="pred-depth", min=2, max=60, step=1, value=20,
                        marks={v: str(v) for v in [2, 10, 20, 30, 40, 50, 60]},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="mb-4"
                    ),

                    html.Label("Soil_Class", className="fw-semibold mb-1"),
                    dcc.Dropdown(
                        id="pred-soil-class",
                        options=_SOIL_OPTIONS,
                        value="3",
                        clearable=False,
                        className="mb-4"
                    ),

                    dbc.Button(
                        "Predecir Sa(T=0.01 s)",
                        id="pred-btn",
                        color="primary",
                        className="w-100 fw-bold",
                        size="lg"
                    ),
                ])
            ], className="shadow-sm border-0 h-100"), md=5, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Resultado de la predicción",
                                           className="mb-0 fw-semibold")),
                    dbc.CardBody(
                        html.Div(
                            id="pred-output",
                            children=dbc.Alert(
                                "Ajusta los parámetros y haz clic en “Predecir Sa(T=0.01 s)”.",
                                color="light",
                                className="mb-0"
                            )
                        )
                    ),
                ], className="shadow-sm border-0 mb-4"),

                dbc.Card([
                    dbc.CardHeader(html.H5("Contexto en el dataset",
                                           className="mb-0 fw-semibold")),
                    dbc.CardBody(
                        dcc.Graph(
                            id="pred-context-plot",
                            config={"displayModeBar": False}
                        )
                    ),
                ], className="shadow-sm border-0"),
            ], md=7, className="mb-4"),
        ]),

    ], fluid=True)


@callback(
    Output("pred-output", "children"),
    Output("pred-context-plot", "figure"),
    Input("pred-btn", "n_clicks"),
    State("pred-magnitude", "value"),
    State("pred-rrup", "value"),
    State("pred-depth", "value"),
    State("pred-soil-class", "value"),
    prevent_initial_call=True,
)
def predict(n_clicks, mag, rrup, depth, soil_class):
    pipeline = _get_pipeline()
    df = _get_context_df()

    soil_class = str(soil_class)
    soil_name = SOIL_CLASS_LABELS.get(soil_class, "-")

    X = _engineer(mag, rrup, depth, soil_class)
    log_sa = float(pipeline.predict(X)[0])
    sa = float(np.exp(log_sa))

    result_panel = [
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.P("Sa(T=0.01 s) predicho",
                           className="text-muted small mb-1"),
                    html.H2(f"{sa:.5f} g", className="fw-bold mb-0",
                            style={"color": "#2980b9"}),
                ])
            ], className="border-0", style={"backgroundColor": "#eaf4fb"})),
        ], className="mb-3"),
        dbc.Table([
            html.Tbody([
                html.Tr([html.Th("Magnitud"), html.Td(f"{mag} Mw")]),
                html.Tr([html.Th("Rrup"), html.Td(f"{rrup} km")]),
                html.Tr([html.Th("Profundidad"), html.Td(f"{depth} km")]),
                html.Tr([html.Th("Soil_Class"), html.Td(f"{soil_class} — {soil_name}")]),
                html.Tr([html.Th("log(Sa)"), html.Td(f"{log_sa:.4f}")]),
            ])
        ], bordered=True, size="sm"),
        dbc.Alert([
            html.Strong("Nota: "),
            "La predicción se hace en log(Sa) y luego se transforma a g usando exp(log_sa)."
        ], color="light", className="mt-2 small")
    ]

    colors_soil = {
        "1": "#3498db",
        "2": "#2ecc71",
        "3": "#e67e22",
        "4": "#e74c3c",
        "5": "#9b59b6"
    }

    fig_ctx = go.Figure()
    for soil_value, label in SOIL_CLASS_LABELS.items():
        sub = df[df["Soil_Class"] == soil_value]
        fig_ctx.add_trace(go.Scatter(
            x=sub["Rrup_OpenQuake"],
            y=sub["T_0.01_RotD50"],
            mode="markers",
            name=label,
            opacity=0.5,
            marker=dict(color=colors_soil[soil_value], size=5)
        ))

    fig_ctx.add_trace(go.Scatter(
        x=[rrup],
        y=[sa],
        mode="markers",
        marker=dict(color="black", size=16, symbol="star"),
        name="Tu predicción"
    ))


    fig_ctx.update_layout(
        title=dict(
            text="Predicción en contexto del dataset",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Rrup [km]",
        yaxis_title="Sa(T=0.01 s) [g]",
        xaxis_type="log",
        yaxis_type="log",
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="white",
        height=380,
        margin=dict(l=40, r=20, t=70, b=85),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.85)",
            font=dict(size=10)
        )
    )

    return result_panel, fig_ctx