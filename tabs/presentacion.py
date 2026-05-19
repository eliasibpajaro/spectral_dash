from dash import html
import dash_bootstrap_components as dbc

PAGE_STYLE = {
    "background": "linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%)",
    "padding": "24px",
    "borderRadius": "18px",
}

CARD_STYLE = {
    "border": "none",
    "borderRadius": "18px",
    "boxShadow": "0 8px 24px rgba(44, 62, 80, 0.08)",
    "backgroundColor": "white",
}

def layout():
    return dbc.Container([
        html.Div([
            dbc.Row(dbc.Col([
                html.H1(
                    "PREDICCIÓN DE ACELERACIONES ESPECTRALES",
                    className="fw-bold text-center mt-4 mb-2",
                    style={"color": "#243B55"}
                ),
                html.H4(
                    "Framework de aprendizaje automático para la predicción de la aceleración picoefectiva en ingeniería sísmica",
                    className="text-center mb-4",
                    style={"color": "#64748B"}
                ),
            ])),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Estudiante 1", className="fw-bold"),
                        html.P("Nombre completo: Eliasib Pájaro"),
                        html.P("Programa: Ciencia de datos e ingeniería Civil"),
                        html.P("Correo: epjaro@uninorte.edu.co", className="mb-0"),
                    ])
                ], style=CARD_STYLE), className="mb-4"),

                ]),


            dbc.Row(dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Resumen de presentación", className="fw-bold"),
                    html.P(
                        "En esta presentación se introduce un framework de aprendizaje automático para la predicción de la aceleración picoefectiva en ingeniería sísmica. Se abordan los fundamentos teóricos, la metodología empleada, los resultados obtenidos y las conclusiones del estudio, destacando su relevancia para la ingeniería sísmica y su potencial impacto en la seguridad estructural. Asímismo se da una breve introducción a lo que es el espectro de respuesta sísmica y su importancia en la ingeniería sísmica.",
                        className="mb-0",
                        style={"color": "#64748B"}
                    )
                ])
            ], style=CARD_STYLE), className="mb-5")),
            html.P([
                "En este video se presenta una introducción al framework de aprendizaje automático para la predicción de la aceleración picoefectiva en ingeniería sísmica, destacando su relevancia y potencial impacto en la seguridad estructural. ",
                html.A(
                    "Ver video en YouTube",
                    href="https://youtu.be/rov29s6St3M",
                    target="_blank",
                    style={
                        "color": "#2563EB",
                        "fontWeight": "600",
                        "textDecoration": "none"
                    }
                )
            ],
    className="mb-0",
    style={"color": "#64748B"}
)

        ], style=PAGE_STYLE)
    ], fluid=True)