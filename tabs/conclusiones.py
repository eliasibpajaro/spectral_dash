"""
tabs/conclusiones.py
--------------------
Conclusiones del proyecto.
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
                html.H2("Conclusiones",
                        className="fw-bold mt-2 mb-1", style={"color": "#2c3e50"}),
                html.P("Síntesis de hallazgos, aportes y perspectivas futuras.",
                       className="lead mb-4", style={"color": "#64748b"}),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ])),

            dbc.Accordion([
                dbc.AccordionItem([
                    _conc_card(
                        "1",
                        "Factibilidad del modelo",
                        "El framework comparativo muestra que las variables sísmicas disponibles "
                        "(Mw, Rrup, profundidad y Soil_Class) contienen información suficiente "
                        "para estimar de forma razonable Sa(T=0.01 s). La comparación entre regresión lineal, "
                        "Random Forest, SVR, MLP y XGBoost permite identificar el mejor equilibrio entre error y capacidad explicativa.",
                        "#eaf4fb", "#2980b9"
                    )
                ], title="Conclusión 1"),

                dbc.AccordionItem([
                    _conc_card(
                        "2",
                        "Importancia de Rrup y magnitud",
                        "El análisis de relevancia de variables muestra que Rrup y Magnitude son determinantes "
                        "para Sa en períodos cortos, en línea con la física de propagación de ondas sísmicas. "
                        "Soil_Class también aporta información relevante, aunque su efecto sigue siendo discreto "
                        "y simplificado frente a variables continuas como Vs30.",
                        "#eaf4fb", "#2980b9"
                    )
                ], title="Conclusión 2"),

                dbc.AccordionItem([
                    _conc_card(
                        "3",
                        "Transformación logarítmica",
                        "El uso de ln(Sa) fue importante para estabilizar la varianza y mejorar el desempeño del modelo. "
                        "La respuesta espectral presenta un comportamiento compatible con una distribución lognormal.",
                        "#eaf4fb", "#2980b9"
                    )
                ], title="Conclusión 3"),

                dbc.AccordionItem([
                    _conc_card(
                        "4",
                        "Valor del dashboard",
                        "La integración en un dashboard interactivo permite explorar el dataset, comparar modelos "
                        "y ejecutar predicciones en tiempo real sin depender de código, acercando los resultados "
                        "a un uso más aplicado en ingeniería sísmica.",
                        "#eaf4fb", "#2980b9"
                    )
                ], title="Conclusión 4"),
            ],
            start_collapsed=True,
            always_open=True,
            className="mb-4"),

            dbc.Card([
                dbc.CardHeader(
                    html.H5("Trabajo futuro y extensiones", className="mb-0 fw-semibold"),
                    style=HEADER_STYLE
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Extensiones del modelo", className="fw-semibold", style={"color": "#243b55"}),
                            html.Ul([
                                html.Li("Entrenar modelos para los 22 períodos del espectro completo."),
                                html.Li("Incorporar Vs30 como variable continua de sitio."),
                                html.Li("Ampliar la comparación hacia otros modelos como LightGBM, CatBoost o arquitecturas secuenciales."),
                                html.Li("Añadir incertidumbre mediante enfoques probabilísticos."),
                            ], style={"color": "#64748b"})
                        ], md=6),

                        dbc.Col([
                            html.H6("Mejoras al dashboard", className="fw-semibold", style={"color": "#243b55"}),
                            html.Ul([
                                html.Li("Visualización del espectro completo predicho."),
                                html.Li("Mapa interactivo de sismos y estaciones con fondos configurables."),
                                html.Li("Comparación automática con GMPE de referencia."),
                                html.Li("Exportación de reportes desde la aplicación."),
                            ], style={"color": "#64748b"})
                        ], md=6),
                    ])
                ])
            ], style=CARD_STYLE, className="mb-4"),

            dbc.Card([
                dbc.CardBody([
                    html.Blockquote([
                        html.P(
                            "\"El aprendizaje automático no reemplaza el conocimiento físico en sismología, "
                            "pero ofrece una herramienta complementaria poderosa para capturar patrones "
                            "complejos en datos instrumentales y acelerar la toma de decisiones en "
                            "ingeniería sísmica aplicada.\"",
                            className="fst-italic fs-5 mb-0",
                            style={"color": "#5c6b7a"}
                        ),
                    ], className="blockquote text-center py-2 mb-0")
                ])
            ], style={
                "border": "none",
                "borderRadius": "18px",
                "backgroundColor": "#f0f4f8",
                "boxShadow": "0 8px 24px rgba(44, 62, 80, 0.08)"
            }, className="mb-5"),

        ], style=PAGE_STYLE)

    ], fluid=True)


def _conc_card(num, title, desc, bg, color):
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div(num, className="fw-bold text-center",
                             style={"fontSize": "2.2rem", "color": color}),
                    width=2
                ),
                dbc.Col([
                    html.H5(title, className="fw-bold", style={"color": "#243b55"}),
                    html.P(desc, className="small mb-0", style={"color": "#64748b"}),
                ], width=10),
            ], align="start")
        ])
    ], style={
        "border": "none",
        "borderRadius": "18px",
        "backgroundColor": bg,
        "boxShadow": "0 8px 22px rgba(44, 62, 80, 0.07)"
    }, className="h-100")