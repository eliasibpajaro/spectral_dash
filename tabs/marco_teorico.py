"""
tabs/marco_teorico.py
---------------------
Marco teórico con fórmulas renderizadas en LaTeX y secciones desplegables.
"""

from dash import html, dcc
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

SECTION_TITLE_STYLE = {
    "color": "#1f3b5b",
    "fontWeight": "700",
    "letterSpacing": "0.2px",
}

SUBTLE_TEXT = {
    "color": "#5c6b7a"
}

FORMULA_BOX_STYLE = {
    "backgroundColor": "#f8fafc",
    "border": "1px solid #e6edf5",
    "borderRadius": "14px",
    "padding": "10px 14px",
}

TABLE_HEADER_STYLE = {
    "background": "linear-gradient(90deg, #243b55 0%, #355c7d 100%)",
    "color": "white"
}


def layout():
    return dbc.Container([

        html.Div([

            dbc.Row(dbc.Col([
                html.H2(
                    "Marco teórico",
                    className="fw-bold mt-2 mb-1",
                    style={"color": "#2c3e50"}
                ),
                html.P(
                    "Fundamentos físicos, espectrales y estadísticos del modelo de predicción.",
                    className="lead mb-4",
                    style={"color": "#64748b"}
                ),
                html.Hr(style={"borderTop": "1px solid #d9e3ef"}),
            ])),

            dbc.Accordion([

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(
                                "Fundamento dinámico",
                                className="fw-bold mb-3",
                                style=SECTION_TITLE_STYLE
                            ),
                            html.P(
                                "El movimiento estructural se idealiza mediante un sistema de un grado de libertad "
                                "(SDOF) sometido a aceleración de base. La ecuación de movimiento puede escribirse como:",
                                className="mb-3",
                                style=SUBTLE_TEXT
                            ),
                            html.Div(
                                dcc.Markdown(
                                    r"""
$$
\ddot{x}(t) + 2\zeta \omega_n \dot{x}(t) + \omega_n^2 x(t) = -\ddot{x}_g(t)
$$
""",
                                    mathjax=True,
                                    className="mb-0"
                                ),
                                style=FORMULA_BOX_STYLE
                            ),
                            html.Div(style={"height": "10px"}),
                            dcc.Markdown(
                                r"""
donde $x(t)$ es el desplazamiento relativo, $\zeta$ es la razón de amortiguamiento,
$\omega_n$ es la frecuencia natural circular y $\ddot{x}_g(t)$ es la aceleración del suelo.
""",
                                mathjax=True,
                                className="mb-0",
                                style=SUBTLE_TEXT
                            ),
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Fundamento dinámico"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(_concept_card(
                            "Espectro de respuesta",
                            r"Describe la respuesta máxima de un oscilador SDOF para distintos períodos estructurales.",
                            r"""
La ordenada espectral de aceleración se interpreta como:

$$
S_a(T,\zeta)=\max_t \left| \ddot{x}(t)+\ddot{x}_g(t) \right|
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_concept_card(
                            "RotD50",
                            r"Se usa para representar una medida robusta de la respuesta espectral horizontal independiente de la orientación.",
                            r"""
RotD50 corresponde al percentil 50 de las ordenadas espectrales obtenidas al rotar los dos componentes horizontales.

$$
\mathrm{RotD50}(T)=P_{50}\left(S_a^{(\theta)}(T)\right)
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_concept_card(
                            "Transformación logarítmica",
                            r"La modelación en escala logarítmica es estándar porque las aceleraciones espectrales suelen exhibir comportamiento aproximadamente lognormal.",
                            r"""
Se modela:

$$
y = \ln\left(S_a(T=0.01\,s)\right)
$$

y luego se recupera la escala original con:

$$
S_a = e^y
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),
                    ], className="mb-1")
                ], title="Conceptos espectrales y estadísticos"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(_concept_card(
                            "Máscara de confiabilidad espectral",
                            r"La columna $T_{\max}$ indica hasta qué período el espectro del registro se considera confiable.",
                            r"""
Para un período objetivo $T$, el registro se usa solo si:

$$
T \leq T_{\max}
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_concept_card(
                            "Soil_Class como variable categórica",
                            r"La clase de suelo no debe tratarse como variable ordinal numérica, sino como categoría.",
                            r"""
En el preproceso, $\mathrm{Soil\_Class}$ se codifica mediante one-hot encoding:

$$
\mathrm{Soil\_Class} \rightarrow \{I(1), I(2), I(3), I(4), I(5)\}
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_concept_card(
                            "Modelos supervisados de regresión",
                            r"El problema puede abordarse con distintos modelos supervisados, desde regresión lineal hasta modelos no lineales como Random Forest, SVR, MLP y XGBoost.",
                            r"""
La relación de predicción puede expresarse en forma general como:

$$
\hat{y}=f(x)
$$
""",
                            "#edf6ff"
                        ), md=4, className="mb-3"),
                    ], className="mb-1")
                ], title="Supuestos y modelación"),

                dbc.AccordionItem([
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5(
                                "Variables del modelo",
                                className="mb-0 fw-semibold",
                                style={"color": "white"}
                            ),
                            style=TABLE_HEADER_STYLE
                        ),
                        dbc.CardBody([
                            dbc.Table([
                                html.Thead(html.Tr([
                                    html.Th("Variable", style={"width": "20%"}),
                                    html.Th("Símbolo"),
                                    html.Th("Tipo"),
                                    html.Th("Unidad"),
                                    html.Th("Rol"),
                                    html.Th("Descripción"),
                                ]), style={"backgroundColor": "#eef3f9"}),
                                html.Tbody([
                                    _op_row(
                                        "Magnitud momento", "M_w", "Continua",
                                        "Adimensional", "Entrada",
                                        "Magnitud del evento sísmico."
                                    ),
                                    _op_row(
                                        "Distancia a ruptura", "R_{rup}", "Continua",
                                        "km", "Entrada",
                                        "Distancia más corta a la ruptura."
                                    ),
                                    _op_row(
                                        "Profundidad hipocentral", "h", "Continua",
                                        "km", "Entrada",
                                        "Profundidad del hipocentro."
                                    ),
                                    _op_row(
                                        "Clase de suelo", r"\mathrm{Soil\_Class}", "Categórica",
                                        "—", "Entrada",
                                        "Clasificación del sitio tratada como categoría."
                                    ),
                                    _op_row(
                                        "Período máximo confiable", r"T_{\max}", "Continua",
                                        "s", "Máscara",
                                        "Límite hasta el cual el espectro se considera confiable."
                                    ),
                                    _op_row(
                                        "Aceleración espectral objetivo", r"S_a(T=0.01\,s)", "Continua",
                                        "g", "Salida",
                                        "Ordenada espectral RotD50 en el período objetivo."
                                    ),
                                ])
                            ], bordered=True, hover=True, responsive=True, size="sm", className="align-middle"),
                        ])
                    ], style=CARD_STYLE, className="mb-2")
                ], title="Variables del modelo"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(_formula_card(
                            "Transformación de distancia",
                            r"""
$$
\log(R_{rup})
$$
""",
                            "Captura la atenuación geométrica de manera no lineal.",
                            "#f8fafc"
                        ), md=6, className="mb-3"),

                        dbc.Col(_formula_card(
                            "Interacción magnitud-distancia",
                            r"""
$$
M_w - \log(R_{rup})
$$
""",
                            "Actúa como proxy simple de intensidad neta.",
                            "#f8fafc"
                        ), md=6, className="mb-3"),

                        dbc.Col(_formula_card(
                            "Término cuadrático de magnitud",
                            r"""
$$
M_w^2
$$
""",
                            "Permite capturar posibles no linealidades con la magnitud.",
                            "#f8fafc"
                        ), md=6, className="mb-3"),

                        dbc.Col(_formula_card(
                            "Transformación de profundidad",
                            r"""
$$
\log(h)
$$
""",
                            "Introduce una escala más estable para la profundidad hipocentral.",
                            "#f8fafc"
                        ), md=6, className="mb-3"),
                    ])
                ], title="Variables derivadas"),

                dbc.AccordionItem([
                    dbc.Row([
                        dbc.Col(_metric_def(
                            "RMSE",
                            "Root Mean Squared Error",
                            r"""
$$
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
$$
""",
                            "Penaliza con mayor fuerza los errores grandes.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_metric_def(
                            "MAE",
                            "Mean Absolute Error",
                            r"""
$$
\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}\left|y_i-\hat{y}_i\right|
$$
""",
                            "Mide el error absoluto promedio del modelo.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),

                        dbc.Col(_metric_def(
                            "R²",
                            "Coeficiente de determinación",
                            r"""
$$
R^2 = 1-\frac{\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}{\sum_{i=1}^{n}(y_i-\bar{y})^2}
$$
""",
                            "Indica la proporción de varianza explicada.",
                            "#edf6ff"
                        ), md=4, className="mb-3"),
                    ])
                ], title="Métricas de evaluación"),

            ],
            start_collapsed=True,
            always_open=True,
            className="mb-5")

        ], style=PAGE_STYLE)

    ], fluid=True)


def _concept_card(title, desc_md, formula_md, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="fw-bold", style={"color": "#243b55"}),
            dcc.Markdown(desc_md, mathjax=True, className="small mb-2", style={"color": "#5c6b7a"}),
            html.Div(
                dcc.Markdown(formula_md, mathjax=True, className="small mb-0"),
                style=FORMULA_BOX_STYLE
            ),
        ])
    ], className="h-100", style={
        "border": "none",
        "borderRadius": "18px",
        "backgroundColor": bg,
        "boxShadow": "0 8px 22px rgba(44, 62, 80, 0.07)"
    })


def _formula_card(title, formula_md, desc, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, className="fw-bold", style={"color": "#243b55"}),
            html.Div(
                dcc.Markdown(formula_md, mathjax=True, className="mb-0"),
                style=FORMULA_BOX_STYLE
            ),
            html.Hr(className="my-3"),
            html.P(desc, className="small mb-0", style={"color": "#5c6b7a"}),
        ])
    ], className="h-100", style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": bg,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    })


def _op_row(var, sym, tipo, unit, rol, desc):
    rol_color = {"Entrada": "primary", "Máscara": "warning", "Salida": "danger"}
    return html.Tr([
        html.Td(var),
        html.Td(dcc.Markdown(rf"${sym}$", mathjax=True, className="mb-0")),
        html.Td(tipo),
        html.Td(unit),
        html.Td(dbc.Badge(rol, color=rol_color.get(rol, "secondary"))),
        html.Td(html.Small(desc, className="text-muted")),
    ], style={"backgroundColor": "white"})


def _metric_def(abbr, name, formula_md, desc, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H4(abbr, className="fw-bold", style={"color": "#2c3e50"}),
            html.P(name, className="small mb-2", style={"color": "#64748b"}),
            html.Div(
                dcc.Markdown(formula_md, mathjax=True, className="mb-0"),
                style=FORMULA_BOX_STYLE
            ),
            html.Hr(className="my-3"),
            html.P(desc, className="small mb-0", style={"color": "#5c6b7a"}),
        ])
    ], className="h-100", style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": bg,
        "boxShadow": "0 6px 18px rgba(44, 62, 80, 0.06)"
    })