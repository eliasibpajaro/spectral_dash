"""
tabs/problema.py
----------------
Planteamiento del problema de investigación.
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
                    "Problema de investigación",
                    className="fw-bold mt-2 mb-1",
                    style={"color": "#2c3e50"}
                ),
                html.P(
                    "Predicción de la aceleración espectral Sa(T=0.01 s) a partir de variables sismológicas y de sitio.",
                    className="lead mb-4",
                    style=SUBTLE_TEXT
                ),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ])),

            dbc.Accordion([

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Contexto del problema", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            html.P(
                                "La estimación del movimiento del suelo es un componente central en ingeniería sísmica, "
                                "porque de ella dependen análisis de amenaza, diseño estructural y evaluación del riesgo. "
                                "En contextos regionales como el colombiano, la disponibilidad de registros sigue siendo "
                                "más limitada que en bases internacionales, lo que dificulta construir modelos con cobertura homogénea.",
                                style=SUBTLE_TEXT
                            ),
                            html.P(
                                "En particular, la aceleración espectral en períodos cortos como Sa(T=0.01 s) depende de manera "
                                "no lineal de la magnitud, la distancia a la ruptura, la profundidad hipocentral y la condición local del sitio.",
                                className="mb-0",
                                style=SUBTLE_TEXT
                            )
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Contexto del problema"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H5(
                                    "Dificultad principal",
                                    className="fw-semibold mb-3",
                                    style={"color": "#243b55"}
                                ),
                                html.P(
                                    "El conjunto de datos no cubre de manera homogénea todas las combinaciones posibles de magnitud, "
                                    "distancia, profundidad y clase de suelo. Además, no todas las observaciones son igualmente confiables "
                                    "en todo el rango espectral, por lo que debe usarse Tmax como criterio de validez.",
                                    className="mb-0",
                                    style=SUBTLE_TEXT
                                )
                            ])
                        ], style=CARD_STYLE, className="h-100"), md=6, className="mb-3"),

                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H5(
                                    "Necesidad de modelación",
                                    className="fw-semibold mb-3",
                                    style={"color": "#243b55"}
                                ),
                                html.P(
                                    "Se requiere un modelo supervisado que permita predecir Sa(T=0.01 s) "
                                    "preservando una representación coherente del efecto del sitio y evitando "
                                    "tratar Soil_Class como si fuera una escala numérica ordinal.",
                                    className="mb-0",
                                    style=SUBTLE_TEXT
                                )
                            ])
                        ], style=CARD_STYLE, className="h-100"), md=6, className="mb-3"),
                    ], className="mb-1")
                ], title="Dificultad y necesidad de modelación"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(
                                "Pregunta de investigación",
                                className="fw-semibold mb-3",
                                style={"color": "#243b55"}
                            ),
                            html.Div([
                                html.Strong("Pregunta central: "),
                                html.Span(
                                    "¿Es posible predecir de forma consistente la aceleración espectral Sa(T=0.01 s) "
                                    "usando Magnitude, Rrup_OpenQuake, Hypocenter Depth (km) y Soil_Class, "
                                    "tratando Soil_Class correctamente como una variable categórica?",
                                    style=SUBTLE_TEXT
                                )
                            ], style={
                                "backgroundColor": "#f8fafc",
                                "border": "1px solid #e6edf5",
                                "borderRadius": "14px",
                                "padding": "14px 16px"
                            })
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Pregunta de investigación"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5("Enfoque adoptado", className="mb-0 fw-semibold"),
                            style=HEADER_STYLE
                        ),
                        dbc.CardBody([
                            html.P(
                                "Para abordar este problema se plantea un flujo de modelación en el que Sa(T=0.01 s) "
                                "se predice a partir de variables sismológicas y geotécnicas seleccionadas. "
                                "Soil_Class se trata como categoría, el EDA se analiza por separado en la pestaña de resultados "
                                "y el desempeño se estudia mediante comparación entre varios modelos supervisados.",
                                className="mb-0",
                                style=SUBTLE_TEXT
                            )
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Enfoque adoptado"),

            ],
            start_collapsed=True,
            always_open=True,
            className="mb-5")

        ], style=PAGE_STYLE)

    ], fluid=True)