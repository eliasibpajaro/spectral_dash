"""
app.py
------
Punto de entrada del dashboard de análisis y predicción de aceleraciones
espectrales sísmicas. Importa cada pestaña como módulo independiente.

Uso:
    python app.py
"""

import os
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

# ── Importar layouts de cada pestaña ─────────────────────────────────────────
from tabs import presentacion
from tabs import introduccion
from tabs import contexto
from tabs import problema
from tabs import objetivos
from tabs import marco_teorico
from tabs import metodologia
from tabs import resultados
from tabs import prediccion
from tabs import limitaciones
from tabs import conclusiones
from tabs import mapa

# ── Inicializar la app ───────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,          # Tema Bootstrap moderno
        dbc.icons.FONT_AWESOME,
    ],
    suppress_callback_exceptions=True,  # Necesario por layouts dinámicos
    title="Espectros Sísmicos — Colombia",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# ── Definición de pestañas ───────────────────────────────────────────────────
_TABS = [
    ("presentacion", " Presentación"),
    ("introduccion",  " Introducción"),
    ("contexto",      " Contexto"),
    ("problema",      " Problema"),
    ("objetivos",     " Objetivos"),
    ("marco_teorico", " Marco Teórico"),
    ("metodologia",   " Metodología"),
    ("resultados",    " Resultados"),
    ("mapa", " Mapa"),
    ("prediccion",    " Predicción"),
    ("limitaciones",  " Limitaciones"),
    ("conclusiones",  " Conclusiones"),
]

# ── Layout principal ─────────────────────────────────────────────────────────
app.layout = html.Div([

    # Navbar superior
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.I(className="fas fa-wave-square me-2",
                                   style={"color": "#3498db", "fontSize": "1.5rem"})),
                    dbc.Col(dbc.NavbarBrand(
                        "Aceleraciones Espectrales Sísmicas — Colombia",
                        className="ms-1 fw-bold",
                        style={"color": "#2c3e50"}
                    )),
                ], align="center"),
                href="#", style={"textDecoration": "none"}
            ),
            dbc.Badge("T = 0.01 s · RotD50 · LR · RF · SVR · MLP · XGBoost",
                color="primary", className="ms-auto d-none d-md-block"),
        ], fluid=True),
        color="white",
        className="shadow-sm border-bottom mb-0",
        sticky="top"
    ),

    # Tabs de navegación
    dbc.Container([
        dcc.Tabs(
            id="main-tabs",
            value="presentacion",
            children=[
                dcc.Tab(
                    label=label,
                    value=value,
                    style={
                        "padding": "10px 14px",
                        "fontSize": "0.82rem",
                        "fontWeight": "500",
                        "color": "#5d6d7e",
                        "borderTop": "3px solid transparent",
                    },
                    selected_style={
                        "padding": "10px 14px",
                        "fontSize": "0.82rem",
                        "fontWeight": "700",
                        "color": "#2980b9",
                        "borderTop": "3px solid #2980b9",
                        "backgroundColor": "#f0f7ff",
                    }
                )
                for value, label in _TABS
            ],
            className="mt-2",
        ),

        # Contenido dinámico de la pestaña seleccionada
        html.Div(id="tab-content", className="mt-0"),

    ], fluid=True, className="px-3"),

    # Footer
    html.Footer(
        dbc.Container(
            dbc.Row(dbc.Col(
                html.P(
                    "Dashboard de Aceleraciones Espectrales Sísmicas · "
                    "Desarrollado con Dash + Plotly + scikit-learn · "
                    "Dataset: Registros sísmicos colombianos",
                    className="text-center text-muted small py-3 mb-0"
                )
            )),
            fluid=True
        ),
        className="border-top mt-4",
        style={"backgroundColor": "#f8f9fa"}
    ),

], style={"backgroundColor": "#f5f6fa", "minHeight": "100vh"})


# ── Callback principal: renderizar pestaña activa ────────────────────────────
@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value")
)
def render_tab(tab):
    """Carga el layout de la pestaña seleccionada."""
    layouts = {
        "presentacion": presentacion.layout,
        "introduccion":  introduccion.layout,
        "contexto":      contexto.layout,
        "problema":      problema.layout,
        "objetivos":     objetivos.layout,
        "marco_teorico": marco_teorico.layout,
        "metodologia":   metodologia.layout,
        "resultados":    resultados.layout,
        "mapa": mapa.layout,
        "prediccion":    prediccion.layout,
        "limitaciones":  limitaciones.layout,
        "conclusiones":  conclusiones.layout,
    }
    fn = layouts.get(tab)
    if fn:
        return fn()
    return html.Div("Pestaña no encontrada.", className="p-4 text-muted")

server = app.server  # Para Google Cloud Run / App Engine


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)