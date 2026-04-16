"""
tabs/metodologia.py
-------------------
Descripción metodológica del flujo de datos, preproceso y modelación.
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

SUBTLE_TEXT = {"color": "#64748b"}


def layout():
    return dbc.Container([

        html.Div([

            dbc.Row(dbc.Col([
                html.H2(
                    "Metodología",
                    className="fw-bold mt-2 mb-1",
                    style={"color": "#2c3e50"}
                ),
                html.P(
                    "Flujo metodológico para la predicción de Sa(T=0.01 s) usando un framework comparativo de modelos.",
                    className="lead mb-4",
                    style=SUBTLE_TEXT
                ),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ])),

            dbc.Accordion([

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Resumen del enfoque", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            html.P(
                                "Se plantea un esquema supervisado para predecir la aceleración espectral "
                                "Sa(T=0.01 s) a partir de variables sismológicas y de sitio. La variable objetivo "
                                "se modela en escala logarítmica y Soil_Class se trata como variable categórica "
                                "mediante codificación one-hot.",
                                className="mb-0",
                                style=SUBTLE_TEXT
                            )
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Resumen del enfoque"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(_step_card(
                            "1",
                            "Carga y estandarización",
                            "Se carga espectros_Wide.csv y se normalizan nombres de columnas: Cat → Soil_Class y Tcorner → Tmax.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_step_card(
                            "2",
                            "Filtrado por calidad",
                            "Se usa Tmax como máscara de confiabilidad espectral. Para T = 0.01 s solo se conservan registros con Tmax ≥ 0.01 s.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_step_card(
                            "3",
                            "Definición del target",
                            "La variable objetivo es T_0.01_RotD50 y el aprendizaje se realiza sobre log(Sa).",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_step_card(
                            "4",
                            "Variables predictoras",
                            "Se usan Magnitude, Rrup_OpenQuake, Hypocenter Depth (km) y Soil_Class, además de variables derivadas numéricas.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_step_card(
                            "5",
                            "Codificación de Soil_Class",
                            "Soil_Class no se trata como variable ordinal. Se codifica como variable categórica mediante OneHotEncoder.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_step_card(
                            "6",
                            "Entrenamiento y comparación",
                            "Se entrenan y comparan regresión lineal, Random Forest, SVR (RBF), MLP y XGBoost con train/test y validación cruzada.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),
                    ], className="mb-1")
                ], title="Flujo metodológico"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Variables del modelo", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(_feature_row(
                                    "Magnitude",
                                    "Magnitud momento del sismo.",
                                    "#edf6ff"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "Rrup_OpenQuake",
                                    "Distancia a ruptura en kilómetros.",
                                    "#edf6ff"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "Hypocenter Depth (km)",
                                    "Profundidad hipocentral en kilómetros.",
                                    "#edf6ff"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "Soil_Class",
                                    "Clase de sitio codificada como variable categórica.",
                                    "#edf6ff"
                                ), md=6, className="mb-3"),
                            ])
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Variables del modelo"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Variables derivadas", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(_feature_row(
                                    "log_Rrup",
                                    "Transformación logarítmica de la distancia para capturar atenuación geométrica.",
                                    "#f8fafc"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "Mag_logRrup",
                                    "Combinación Magnitude − log(Rrup) como proxy de intensidad neta.",
                                    "#f8fafc"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "Mag2",
                                    "Término cuadrático de magnitud para capturar no linealidad.",
                                    "#f8fafc"
                                ), md=6, className="mb-3"),

                                dbc.Col(_feature_row(
                                    "log_Depth",
                                    "Transformación logarítmica de la profundidad hipocentral.",
                                    "#f8fafc"
                                ), md=6, className="mb-3"),
                            ])
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Variables derivadas"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Esquema de modelación", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            html.Ul([
                                html.Li("Entrada: variables numéricas + Soil_Class categórica."),
                                html.Li("Preproceso: OneHotEncoder para Soil_Class."),
                                html.Li("Modelos comparados: Regresión lineal, Random Forest, SVR (RBF), MLP y XGBoost."),
                                html.Li("Salida del modelo: log[Sa(T=0.01 s)]."),
                                html.Li("Transformación final: Sa = exp(log(Sa))."),
                            ], className="mb-0", style={"color": "#64748b"})
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Esquema de modelación"),

            ],
            start_collapsed=True,
            always_open=True,
            className="mb-5")

        ], style=PAGE_STYLE)

    ], fluid=True)


def _step_card(num, title, text, color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(
                num,
                className="fw-bold mb-2",
                style={"fontSize": "1.9rem", "color": "#243b55"}
            ),
            html.H5(title, className="fw-semibold", style={"color": "#243b55"}),
            html.P(text, className="mb-0", style={"color": "#64748b"}),
        ])
    ], style={
        "border": "none",
        "borderRadius": "18px",
        "backgroundColor": color,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    }, className="h-100")


def _feature_row(name, desc, bg="#ffffff"):
    return dbc.Card([
        dbc.CardBody([
            html.H6(name, className="fw-semibold mb-1", style={"color": "#243b55"}),
            html.P(desc, className="mb-0", style={"color": "#64748b"}),
        ], className="p-3")
    ], style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": bg,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    }, className="h-100")