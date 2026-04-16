"""
tabs/limitaciones.py
--------------------
Limitaciones del estudio y del modelo.
"""

from dash import html
import dash_bootstrap_components as dbc


PAGE_STYLE = {
    "background": "linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%)",
    "padding": "18px",
    "borderRadius": "18px",
}

CARD_STYLE = {
    "border": "none",
    "borderRadius": "18px",
    "boxShadow": "0 8px 24px rgba(44, 62, 80, 0.08)",
    "backgroundColor": "white",
}

HEADER_STYLE = {
    "background": "linear-gradient(90deg, #243b55 0%, #355c7d 100%)",
    "color": "white",
    "borderTopLeftRadius": "18px",
    "borderTopRightRadius": "18px",
    "borderBottom": "none",
}


def layout():
    return dbc.Container([

        html.Div([

            dbc.Row(dbc.Col([
                html.H2("Limitaciones del estudio",
                        className="fw-bold mt-2 mb-1", style={"color": "#2c3e50"}),
                html.P("Restricciones metodológicas, del dataset y del modelo.",
                       className="lead mb-4", style={"color": "#64748b"}),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ])),

            dbc.Accordion([
                dbc.AccordionItem([
                    _lim_card(
                        "Datos",
                        [
                            "Dataset limitado a 709 registros colombianos.",
                            "Rango de magnitudes relativamente estrecho (4.5–6.78 Mw).",
                            "Alta concentración de registros con Rrup > 100 km, subrepresentando campo cercano.",
                            "Soil_Class es una variable discreta y no captura variabilidad continua del suelo como Vs30.",
                        ],
                        "#eef7fb"
                    )
                ], title="Datos"),

                dbc.AccordionItem([
                    _lim_card(
                        "Modelo",
                        [
                            "Entrenado únicamente para el período T=0.01 s.",
                            "No incorpora efectos explícitos de directividad ni geometría de ruptura.",
                            "Los modelos basados en datos no extrapolan bien fuera del rango de entrenamiento.",
                            "No se realizó una búsqueda exhaustiva de hiperparámetros para todos los candidatos.",
                            "Aún existe variabilidad no explicada asociada a propagación y efectos de sitio.",
                        ],
                        "#eef7fb"
                    )
                ], title="Modelo"),

                dbc.AccordionItem([
                    _lim_card(
                        "Metodológicas",
                        [
                            "No se realiza validación cruzada espacial estricta por estación.",
                            "Soil_Class es una simplificación; idealmente se preferiría Vs30 continuo.",
                            "No se modela explícitamente la variabilidad inter-evento e intra-evento como en GMPE clásicos.",
                            "La interpretación física de resultados en escala logarítmica requiere cuidado.",
                        ],
                        "#eef7fb"
                    )
                ], title="Metodológicas"),
            ],
            start_collapsed=True,
            always_open=True,
            className="mb-4"),

            dbc.Card([
                dbc.CardHeader(
                    html.H5("Resumen de limitaciones y posibles mejoras", className="mb-0 fw-semibold"),
                    style=HEADER_STYLE
                ),
                dbc.CardBody([
                    dbc.Table([
                        html.Thead(html.Tr([
                            html.Th("Limitación"),
                            html.Th("Impacto estimado"),
                            html.Th("Posible mejora"),
                        ]), style={"backgroundColor": "#eef3f9"}),
                        html.Tbody([
                            html.Tr([
                                html.Td("Tamaño del dataset"),
                                html.Td(dbc.Badge("Alto", color="danger")),
                                html.Td("Incorporar registros de países vecinos o ampliar la red")
                            ]),
                            html.Tr([
                                html.Td("Falta de Vs30"),
                                html.Td(dbc.Badge("Medio", color="warning", text_color="dark")),
                                html.Td("Reemplazar Soil_Class por Vs30 continuo o proxy geológico")
                            ]),
                            html.Tr([
                                html.Td("Solo T=0.01 s"),
                                html.Td(dbc.Badge("Medio", color="warning", text_color="dark")),
                                html.Td("Entrenar modelos separados por período o usar enfoques vectoriales")
                            ]),
                            html.Tr([
                                html.Td("No validación cruzada espacial"),
                                html.Td(dbc.Badge("Medio", color="warning", text_color="dark")),
                                html.Td("Usar LeaveOneGroupOut por estación para evaluación más realista")
                            ]),
                            html.Tr([
                                html.Td("Sin optimización de hiperparámetros"),
                                html.Td(dbc.Badge("Bajo", color="success")),
                                html.Td("Aplicar Optuna o RandomizedSearchCV")
                            ]),
                        ])
                    ], bordered=True, hover=True, responsive=True, size="sm")
                ])
            ], style=CARD_STYLE, className="mb-5"),

        ], style=PAGE_STYLE)

    ], fluid=True)


def _lim_card(title, items, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H5(title, className="fw-bold mb-3", style={"color": "#243b55"}),
            html.Ul([
                html.Li(item, className="mb-2", style={"color": "#5c6b7a"})
                for item in items
            ], className="ps-3 mb-0"),
        ])
    ], style={
        "border": "none",
        "borderRadius": "18px",
        "backgroundColor": bg,
        "boxShadow": "0 8px 22px rgba(44, 62, 80, 0.07)"
    }, className="h-100")