"""
tabs/contexto.py
----------------
Pestaña de contexto: impacto e importancia en ingeniería sísmica.
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
    "padding": "14px",
}

SUBTLE_TEXT = {"color": "#64748b"}


def layout():
    return dbc.Container([

        dbc.Row(dbc.Col([
            html.H2("Contexto e Importancia en Ingeniería Sísmica",
                    className="fw-bold mt-4 mb-1", style={"color": "#2c3e50"}),
            html.P("Por qué predecir aceleraciones espectrales es crítico para el diseño estructural",
                   className="text-muted lead mb-4"),
            html.Hr(),
        ])),

        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col(_impact_card(
                        "Diseño sismo-resistente",
                        "Las aceleraciones espectrales son la entrada fundamental de los códigos de diseño "
                        "(NSR-10 en Colombia, ASCE 7 en EE.UU.). Determinar Sa(T) con precisión permite "
                        "dimensionar correctamente vigas, columnas y sistemas de disipación.",
                        "#d0e8f1"
                    ), width=4, className="mb-3"),
                    dbc.Col(_impact_card(
                        "Evaluación de amenaza sísmica",
                        "Los análisis probabilísticos de amenaza sísmica (PSHA) utilizan modelos de "
                        "predicción del movimiento del suelo (GMM/GMPE) para estimar la probabilidad "
                        "de excedencia de Sa en un sitio dado.",
                        "#d0e8f1"
                    ), width=4, className="mb-3"),
                    dbc.Col(_impact_card(
                        "Machine Learning en sismología",
                        "Los enfoques de aprendizaje automático permiten capturar relaciones no lineales "
                        "complejas entre parámetros sísmicos y respuesta espectral, complementando los "
                        "modelos físicos tradicionales.",
                        "#d0e8f1"
                    ), width=4, className="mb-3"),
                ])
            ], title="Áreas de impacto"),

            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.P(
                            "Colombia está ubicada en una de las zonas de mayor actividad sísmica del "
                            "mundo, en la intersección de las placas Nazca, Caribe y Sudamericana. "
                            "Esta configuración tectónica genera sismos frecuentes con magnitudes "
                            "que pueden superar M 7.0.",
                            className="text-secondary"
                        ),
                        html.P(
                            "La Reglamentación Colombiana de Construcción Sismo-Resistente (NSR-10) "
                            "establece los espectros de diseño para diferentes zonas del país, pero "
                            "la base de datos instrumental sigue siendo limitada comparada con "
                            "regiones como Japón o California, lo que hace valioso el desarrollo "
                            "de modelos de predicción locales.",
                            className="text-secondary"
                        ),
                    ], width=8),
                    dbc.Col([
                        _stat_card("M máx registrada", "6.78", "#3498db"),
                        _stat_card("Rrup mínima", "12.5 km", "#3498db"),
                        _stat_card("Profundidades", "2 – 58.7 km", "#3498db"),
                        _stat_card("Registros disponibles", "709", "#3498db"),
                    ], width=4),
                ])
            ], title="Colombia en el contexto sísmico regional"),

            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.P(
                            "Las ecuaciones de predicción del movimiento del suelo (GMPE) son relaciones empíricas "
                            "que predicen Sa en función de parámetros de la fuente, trayectoria y sitio.",
                            className="text-secondary"
                        ),
                        dbc.Table([
                            html.Thead(html.Tr([
                                html.Th("Familia GMPE"), html.Th("Región"), html.Th("Período máx.")
                            ])),
                            html.Tbody([
                                html.Tr([html.Td("NGA-West2 (ASK14, BSSA14, CB14, CY14)"),
                                         html.Td("Global"), html.Td("10 s")]),
                                html.Tr([html.Td("García et al. (2005)"),
                                         html.Td("México"), html.Td("4 s")]),
                                html.Tr([html.Td("Zhao et al. (2006)"),
                                         html.Td("Japón"), html.Td("5 s")]),
                                html.Tr([html.Td("Framework comparativo (LR, RF, SVR, MLP, XGBoost)"),
                                         html.Td("Colombia"), html.Td("0.01 s (T₁)")]),
                            ])
                        ], bordered=True, hover=True, responsive=True, size="sm",
                           className="mt-2"),
                    ], width=7),
                    dbc.Col([
                        _feature_row("M — Magnitud", "Energía liberada por el sismo", "#e8f4f8"),
                        _feature_row("Rrup — Distancia ruptura", "Distancia más corta a la falla", "#e8f4f8"),
                        _feature_row("Prof. hipocentral", "Profundidad del foco sísmico (km)", "#e8f4f8"),
                        _feature_row("Soil_Class — Clase de sitio", "Tipo de suelo (1-5, NSR-10)", "#e8f4f8"),
                    ], width=5),
                ])
            ], title="GMPE y variables predictoras"),
        ],
        start_collapsed=True,
        always_open=True,
        className="mb-5")

    ], fluid=True)


def _impact_card(title, body, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="fw-bold text-center"),
            html.P(body, className="text-secondary small text-center mb-0"),
        ])
    ], className="border-0 h-100", style={"backgroundColor": bg})


def _stat_card(label, value, color):
    return html.Div([
        html.Div(value, className="fw-bold", style={"color": color, "fontSize": "1.4rem"}),
        html.Div(label, className="small", style={"color": "#64748b"})
    ], style={
        "backgroundColor": "#f8fafc",
        "border": "1px solid #e6edf5",
        "borderRadius": "14px",
        "padding": "12px 14px",
        "marginBottom": "10px"
    })


def _feature_row(name, desc, bg):
    return html.Div([
        html.Div([
            html.Strong(name, style={"fontSize": "0.92rem", "color": "#243b55"}),
            html.P(desc, className="small mb-0", style={"color": "#64748b"}),
        ], className="p-3", style={
            "backgroundColor": bg,
            "borderRadius": "14px",
            "border": "1px solid rgba(36,59,85,0.05)"
        })
    ], className="mb-3")