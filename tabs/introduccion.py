"""
tabs/introduccion.py
--------------------
Pestaña de introducción: explica los espectros de respuesta y el problema.
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

SOFT_BOX = {
    "backgroundColor": "#f8fafc",
    "border": "1px solid #e6edf5",
    "borderRadius": "14px",
    "padding": "14px 12px",
    "height": "100%",
}

BADGE_PERIOD_STYLE = {
    "fontSize": "0.78rem",
    "padding": "0.45rem 0.65rem",
    "borderRadius": "999px",
}

TITLE_STYLE = {
    "color": "#2c3e50"
}

SUBTLE_TEXT = {
    "color": "#64748b"
}


def layout():
    return dbc.Container([

        html.Div([

            dbc.Row(dbc.Col(html.Div([
                html.H1(
                    "Análisis y predicción de Aceleraciones Espectrales",
                    className="display-5 fw-bold text-center mt-3",
                    style=TITLE_STYLE
                ),
                html.P(
                    "Dashboard analítico para ingeniería sísmica basado en registros colombianos.",
                    className="lead text-center mb-3",
                    style=SUBTLE_TEXT
                ),
                dbc.Alert([
                    html.Strong("Enfoque actual: "),
                    "comparación de modelos supervisados para predecir Sa(T=0.01 s) "
                    "usando variables sismológicas y de sitio."
                ], color="info", className="mb-4"),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ]))),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(
                        html.H5("¿Qué es un espectro de respuesta?", className="mb-0 fw-semibold"),
                        style=HEADER_STYLE
                    ),
                    dbc.CardBody([
                        html.P(
                            "Un espectro de respuesta es una curva que resume la respuesta máxima "
                            "de un oscilador de un grado de libertad (SDOF) ante una excitación sísmica, "
                            "en función de su período natural $T$.",
                            className="mb-3",
                            style=SUBTLE_TEXT
                        ),
                        html.P(
                            "Cada punto de la curva representa la aceleración espectral máxima "
                            "que experimentaría una estructura cuyo período natural es específico.",
                            className="mb-3",
                            style=SUBTLE_TEXT
                        ),
                        dbc.Row([
                            dbc.Col(html.Div([
                                html.Div("Sa(T)", className="fs-2 fw-bold text-center",
                                         style={"color": "#4f81bd"}),
                                html.P(
                                    "Aceleración espectral en función del período.",
                                    className="text-center small mb-0",
                                    style=SUBTLE_TEXT
                                ),
                            ], style=SOFT_BOX), md=4, className="mb-3"),
                            dbc.Col(html.Div([
                                html.Div("T [s]", className="fs-2 fw-bold text-center",
                                         style={"color": "#6aa84f"}),
                                html.P(
                                    "Período natural de vibración de la estructura.",
                                    className="text-center small mb-0",
                                    style=SUBTLE_TEXT
                                ),
                            ], style=SOFT_BOX), md=4, className="mb-3"),
                            dbc.Col(html.Div([
                                html.Div("RotD50", className="fs-2 fw-bold text-center",
                                         style={"color": "#c27c0e"}),
                                html.P(
                                    "Mediana de rotaciones horizontales, usada como medida robusta.",
                                    className="text-center small mb-0",
                                    style=SUBTLE_TEXT
                                ),
                            ], style=SOFT_BOX), md=4, className="mb-3"),
                        ], className="g-3"),
                    ])
                ], style=CARD_STYLE), md=6, className="mb-4"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader(
                        html.H5("Componente RotD50", className="mb-0 fw-semibold"),
                        style=HEADER_STYLE
                    ),
                    dbc.CardBody([
                        html.P(
                            "La métrica RotD50 es la mediana de las aceleraciones espectrales "
                            "obtenidas al rotar los dos componentes horizontales del movimiento "
                            "a todos los ángulos posibles.",
                            className="mb-3",
                            style=SUBTLE_TEXT
                        ),
                        html.P(
                            "Es ampliamente usada porque reduce la dependencia de la orientación "
                            "del instrumento y ofrece una representación estable de la demanda sísmica.",
                            className="mb-3",
                            style=SUBTLE_TEXT
                        ),
                        html.Div([
                            dbc.Badge("Percentil 50", color="primary", className="me-2 mb-2"),
                            dbc.Badge("Agnóstico a la orientación", color="success", className="me-2 mb-2"),
                            dbc.Badge("Uso extendido en ingeniería sísmica", color="warning", text_color="dark", className="mb-2"),
                        ], className="mb-3"),
                        html.Div([
                            html.Strong("Nota de calidad espectral. "),
                            html.Span(
                                "Los 22 períodos disponibles van desde T=0.01 s hasta T=10.0 s. "
                                "Registros de menor calidad se invalidan mediante la columna Tmax, "
                                "que indica el período máximo hasta donde el registro es confiable.",
                                style=SUBTLE_TEXT
                            )
                        ], style=SOFT_BOX)
                    ])
                ], style=CARD_STYLE), md=6, className="mb-4"),
            ]),

            dbc.Card([
                dbc.CardHeader(
                    html.H5("Períodos espectrales disponibles (22 períodos)", className="mb-0 fw-semibold"),
                    style=HEADER_STYLE
                ),
                dbc.CardBody([
                    html.Div([
                        dbc.Badge(
                            f"T={p}s",
                            color="secondary",
                            className="me-2 mb-2",
                            style=BADGE_PERIOD_STYLE
                        )
                        for p in [0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2,
                                  0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0,
                                  3.0, 4.0, 5.0, 6.0, 7.5, 10.0]
                    ]),
                    html.Hr(style={"borderTop": "1px solid #e6edf5"}),
                    html.Div([
                        html.Strong("Período de análisis en este proyecto: "),
                        dbc.Badge("T = 0.01 s", color="danger", className="fs-6 me-2"),
                        html.Span(
                            "primer período del espectro, asociado a aceleraciones de alta frecuencia.",
                            style=SUBTLE_TEXT
                        )
                    ])
                ])
            ], style=CARD_STYLE, className="mb-4"),

            dbc.Card([
                dbc.CardHeader(
                    html.H5("Flujo del proyecto", className="mb-0 fw-semibold"),
                    style=HEADER_STYLE
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(_step_card("1", "Dataset", "709 registros sísmicos colombianos", "#4f81bd"), md=2, className="mb-3"),
                        dbc.Col(_step_card("2", "EDA", "Análisis exploratorio y correlaciones", "#6aa84f"), md=2, className="mb-3"),
                        dbc.Col(_step_card("3", "Preproceso", "Tmax, log-transform y variables derivadas", "#c27c0e"), md=2, className="mb-3"),
                        dbc.Col(_step_card("4", "Modelos", "LR · RF · SVR · MLP · XGBoost", "#ae4132"), md=2, className="mb-3"),
                        dbc.Col(_step_card("5", "Evaluación", "Comparación de métricas entre modelos", "#7e57a0"), md=2, className="mb-3"),
                        dbc.Col(_step_card("6", "Predicción", "Formulario interactivo con modelo ganador", "#d79b00"), md=2, className="mb-3"),
                    ], className="g-3")
                ])
            ], style=CARD_STYLE, className="mb-5"),

        ], style=PAGE_STYLE)

    ], fluid=True)


def _step_card(num, title, desc, color):
    return dbc.Card([
        dbc.CardBody([
            html.Div(
                num,
                className="fw-bold text-center mb-2",
                style={
                    "fontSize": "2rem",
                    "color": color,
                    "lineHeight": "1"
                }
            ),
            html.H6(title, className="text-center fw-semibold mt-1", style={"color": "#243b55"}),
            html.P(desc, className="small text-center mb-0", style={"color": "#64748b"}),
        ])
    ], style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": "#f8fafc",
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)",
        "borderTop": f"4px solid {color}"
    }, className="h-100")
