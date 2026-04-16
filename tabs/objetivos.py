"""
tabs/objetivos.py
-----------------
Pestaña de objetivos y justificación del proyecto.
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

        dbc.Row(dbc.Col([
            html.H2("Objetivos del Proyecto",
                    className="fw-bold mt-4 mb-1", style={"color": "#2c3e50"}),
            html.P("Metas y justificación del análisis de aceleraciones espectrales",
                   className="text-muted lead mb-4"),
            html.Hr(),
        ])),

        dbc.Accordion([
            dbc.AccordionItem([
                html.P(
                    "Desarrollar y evaluar un conjunto comparativo de modelos de aprendizaje automático "
                    "para la predicción de aceleraciones espectrales en el primer período "
                    "(Sa en T=0.01 s, RotD50) a partir de parámetros sísmicos de registros "
                    "colombianos, integrando los resultados en un dashboard analítico interactivo.",
                    className="text-secondary fs-5 mb-0"
                )
            ], title="Objetivo general"),

            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        _obj_item("1", "Exploración del Dataset",
                                  "Realizar un análisis exploratorio (EDA) completo del dataset "
                                  "de registros sísmicos colombianos, identificando distribuciones, "
                                  "correlaciones y calidad de los datos mediante Tmax.",
                                  "#d6eaf8"),
                        _obj_item("2", "Preprocesamiento",
                                  "Aplicar la máscara Tmax para invalidar períodos no confiables, "
                                  "transformar la variable objetivo al espacio logarítmico y preparar "
                                  "las variables de entrada para el entrenamiento.",
                                  "#d6eaf8"),
                    ], width=6),
                    dbc.Col([
                        _obj_item("3", "Entrenamiento del Modelo",
                                  "Entrenar y comparar modelos de regresión lineal, Random Forest, SVR con kernel RBF, MLP y XGBoost para predecir Sa(T=0.01 s), "
                                  "separar correctamente conjuntos de entrenamiento y prueba, "
                                  "y guardar el modelo serializado para su uso en producción.",
                                  "#d6eaf8"),
                        _obj_item("4", "Evaluación y Dashboard",
                                  "Evaluar comparativamente los modelos con métricas RMSE, MAE, R² y R² CV5, visualizar "
                                  "residuos y aceleraciones reales vs predichas, y exponer "
                                  "un formulario de predicción interactiva en tiempo real.",
                                  "#d6eaf8"),
                    ], width=6),
                ])
            ], title="Objetivos específicos"),

            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col(_just_card(
                        "Necesidad Local",
                        "Colombia carece de un GMPE calibrado específicamente con registros "
                        "instrumentales propios. Los modelos globales no capturan "
                        "adecuadamente las particularidades tectónicas de la región Andina.",
                        "#f8f9fa"
                    ), width=4),
                    dbc.Col(_just_card(
                        "Valor Científico",
                        "El uso de Machine Learning como complemento a los GMPE empíricos "
                        "permite explorar relaciones no lineales y capturar efectos locales "
                        "de sitio de manera flexible y escalable.",
                        "#f8f9fa"
                    ), width=4),
                    dbc.Col(_just_card(
                        "Aplicación Práctica",
                        "Un predictor rápido de Sa facilita evaluaciones de amenaza sísmica "
                        "preliminares, análisis de riesgo en infraestructura crítica y la "
                        "toma de decisiones en planificación urbana.",
                        "#f8f9fa"
                    ), width=4),
                ], className="g-3")
            ], title="Justificación"),
        ],
        start_collapsed=True,
        always_open=True,
        className="mb-5")

    ], fluid=True)

def _obj_item(num, title, desc, bg):
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div(
                        num,
                        className="fw-bold text-center",
                        style={"fontSize": "2rem", "color": "#355c7d"}
                    ),
                    width=2
                ),
                dbc.Col([
                    html.H6(title, className="fw-bold mb-1", style={"color": "#243b55"}),
                    html.P(desc, className="small mb-0", style={"color": "#64748b"}),
                ], width=10),
            ], align="center")
        ])
    ], style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": bg,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    }, className="mb-3")


def _just_card(title, desc, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="fw-bold", style={"color": "#243b55"}),
            html.P(desc, className="small mb-0", style={"color": "#64748b"}),
        ])
    ], style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": bg,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    }, className="h-100")
