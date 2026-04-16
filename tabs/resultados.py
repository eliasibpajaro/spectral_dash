"""
tabs/resultados.py
------------------
EDA completo, comparación de modelos, evaluación interactiva
y resumen final del mejor modelo.
"""

import os
import joblib
import pandas as pd
import numpy as np
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.data_utils import SOIL_CLASS_LABELS, load_wide_dataset

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_META_PATH = os.path.join(_BASE, "model", "meta.pkl")

_PERIODS = [0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2,
            0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0,
            3.0, 4.0, 5.0, 6.0, 7.5, 10.0]
_SPEC_COLS = [f"T_{p}_RotD50" for p in _PERIODS]

_META_CACHE = None
_DF_CACHE = None


def _get_meta():
    global _META_CACHE
    if _META_CACHE is None:
        _META_CACHE = joblib.load(_META_PATH)
    return _META_CACHE


def _get_df():
    global _DF_CACHE
    if _DF_CACHE is None:
        _DF_CACHE = load_wide_dataset(_BASE)
    return _DF_CACHE


def _models_dict(meta):
    return meta.get("models", {})


def _comparison_df(meta):
    comp = meta.get("comparison", [])
    if comp:
        return pd.DataFrame(comp)

    rows = []
    for model_key, info in _models_dict(meta).items():
        m = info["metrics"]
        rows.append({
            "model_key": model_key,
            "display_name": info["display_name"],
            "rmse": m["rmse"],
            "mae": m["mae"],
            "r2": m["r2"],
            "r2_cv5": m["r2_cv5"],
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["rank_rmse"] = df["rmse"].rank(method="min", ascending=True)
    df["rank_mae"] = df["mae"].rank(method="min", ascending=True)
    df["rank_r2"] = df["r2"].rank(method="min", ascending=False)
    df["rank_r2_cv5"] = df["r2_cv5"].rank(method="min", ascending=False)
    df["rank_mean"] = df[["rank_rmse", "rank_mae", "rank_r2", "rank_r2_cv5"]].mean(axis=1)
    df = df.sort_values("rank_mean", ascending=True).reset_index(drop=True)
    df["overall_position"] = np.arange(1, len(df) + 1)
    return df


def _pretty_feature_name(feat):
    feat = str(feat)

    if feat.startswith("num__"):
        feat = feat.replace("num__", "", 1)
    if feat.startswith("cat__"):
        feat = feat.replace("cat__", "", 1)

    mapping = {
        "Magnitude": "Magnitud Mw",
        "Rrup_OpenQuake": "Rrup [km]",
        "Hypocenter Depth (km)": "Profundidad hipocentral [km]",
        "log_Rrup": "log(Rrup)",
        "Mag_logRrup": "Mag − log(Rrup)",
        "Mag2": "Magnitud²",
        "log_Depth": "log(Profundidad)",
        "Soil_Class_1": "Soil_Class: Roca dura",
        "Soil_Class_2": "Soil_Class: Roca blanda",
        "Soil_Class_3": "Soil_Class: Suelo denso",
        "Soil_Class_4": "Soil_Class: Suelo blando",
        "Soil_Class_5": "Soil_Class: Suelo muy blando",
    }
    return mapping.get(feat, feat)


def _feature_color(feat):
    feat = str(feat)
    if feat.startswith("num__"):
        feat = feat.replace("num__", "", 1)
    if feat.startswith("cat__"):
        feat = feat.replace("cat__", "", 1)

    if feat in {"Magnitude", "Mag2", "Mag_logRrup"}:
        return "#6c8ebf"
    if feat in {"Rrup_OpenQuake", "log_Rrup"}:
        return "#6c8ebf"
    if feat in {"Hypocenter Depth (km)", "log_Depth"}:
        return "#6c8ebf"
    if feat.startswith("Soil_Class_"):
        return "#6c8ebf"
    return "#6c8ebf"


def _build_metrics_cards(model_info):
    metrics = model_info["metrics"]
    n_test = model_info.get("n_test", len(model_info.get("y_test", [])))

    return dbc.Row([
        dbc.Col(_metric_kpi("RMSE", f"{metrics['rmse']:.4f}", "Escala log(Sa)", "#edf6ff"), md=3, className="mb-3"),
        dbc.Col(_metric_kpi("MAE",  f"{metrics['mae']:.4f}",  "Escala log(Sa)", "#edf6ff"), md=3, className="mb-3"),
        dbc.Col(_metric_kpi("R²",   f"{metrics['r2']:.4f}",   "Test set", "#edf6ff"), md=3, className="mb-3"),
        dbc.Col(_metric_kpi("R² CV5", f"{metrics['r2_cv5']:.4f}", f"{n_test} reg. en test", "#edf6ff"), md=3, className="mb-3"),
    ], className="g-3")


def _build_rvp_fig(model_info, model_name):
    y_test = np.array(model_info["y_test"], dtype=float)
    y_pred = np.array(model_info["y_pred"], dtype=float)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_test,
        y=y_pred,
        mode="markers",
        marker=dict(color="#6c8ebf", opacity=0.65, size=7),
        name="Predicciones"
    ))

    lims = [
        min(y_test.min(), y_pred.min()) - 0.1,
        max(y_test.max(), y_pred.max()) + 0.1
    ]

    fig.add_trace(go.Scatter(
        x=lims,
        y=lims,
        mode="lines",
        line=dict(color="#ae4132", dash="dash", width=2),
        name="Predicción perfecta"
    ))

    fig.update_layout(
        title=f"Reales vs predichos — {model_name}",
        xaxis_title="log(Sa) real",
        yaxis_title="log(Sa) predicho",
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="white",
        height=360
    )
    return fig


def _build_res_fig(model_info, model_name):
    y_test = np.array(model_info["y_test"], dtype=float)
    y_pred = np.array(model_info["y_pred"], dtype=float)
    residuals = y_test - y_pred

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Histograma de residuos", "Residuos vs predichos"]
    )

    fig.add_trace(
        go.Histogram(
            x=residuals,
            nbinsx=30,
            marker_color="#6c8ebf",
            name="Residuos"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=y_pred,
            y=residuals,
            mode="markers",
            marker=dict(color="#6c8ebf", opacity=0.6, size=6),
            name="Residuos"
        ),
        row=1, col=2
    )

    fig.add_hline(y=0, line_dash="dash", line_color="#ae4132", row=1, col=2)

    fig.update_xaxes(title_text="log(Sa) predicho", row=1, col=2)
    fig.update_yaxes(title_text="Residuo", row=1, col=1)
    fig.update_yaxes(title_text="Residuo", row=1, col=2)
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="white",
        showlegend=False,
        title_text=f"Análisis de residuos — {model_name}",
        height=380
    )
    return fig


def _build_feature_plot(model_info, model_name):
    scores = model_info.get("feature_scores", {})
    score_kind = model_info.get("feature_score_kind")

    if not scores:
        return dbc.Alert(
            f"{model_name} no expone una medida directa de relevancia de variables en esta implementación.",
            color="light",
            className="mb-0"
        )

    df_imp = pd.DataFrame({
        "Feature_raw": list(scores.keys()),
        "Score": list(scores.values()),
    })

    df_imp["Feature"] = df_imp["Feature_raw"].apply(_pretty_feature_name)
    df_imp["Color"] = df_imp["Feature_raw"].apply(_feature_color)

    df_imp = (
        df_imp.groupby(["Feature", "Color"], as_index=False)["Score"]
        .sum()
        .sort_values("Score", ascending=True)
    )

    if score_kind == "coef_abs":
        title_suffix = "Relevancia aproximada (|coef| normalizado)"
    else:
        title_suffix = "Importancia relativa"

    fig = go.Figure(go.Bar(
        x=df_imp["Score"],
        y=df_imp["Feature"],
        orientation="h",
        marker_color=df_imp["Color"].tolist(),
        text=[f"{v:.1%}" for v in df_imp["Score"]],
        textposition="outside",
    ))

    fig.update_layout(
        title=f"{title_suffix} — {model_name}",
        xaxis_title="Peso relativo",
        xaxis_tickformat=".0%",
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=240),
        height=380,
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def _build_model_summary(model_key, meta):
    models = _models_dict(meta)
    comparison = _comparison_df(meta)
    model_info = models[model_key]
    model_name = model_info["display_name"]

    row = comparison.loc[comparison["model_key"] == model_key].iloc[0]
    best_key = meta.get("best_model_key", comparison.iloc[0]["model_key"])
    is_best = model_key == best_key

    metrics = model_info["metrics"]

    text = (
        f"{model_name} ocupa la posición #{int(row['overall_position'])} "
        f"en la comparación global. "
        f"Sus métricas son RMSE={metrics['rmse']:.4f}, "
        f"MAE={metrics['mae']:.4f}, R²={metrics['r2']:.4f} y "
        f"R² CV5={metrics['r2_cv5']:.4f}."
    )

    if is_best:
        color = "success"
        title = f"{model_name} es el mejor modelo según el resumen comparativo."
    else:
        best_name = meta.get("best_model_name", comparison.iloc[0]["display_name"])
        color = "secondary"
        title = f"{model_name} no es el modelo líder; el mejor es {best_name}."

    return dbc.Alert([
        html.H6(title, className="alert-heading mb-2"),
        html.P(text, className="mb-0")
    ], color=color, className="mb-4")


def _build_best_model_summary(meta):
    comparison = _comparison_df(meta)
    if comparison.empty:
        return dbc.Alert("No hay resultados comparativos guardados.", color="light")

    best_row = comparison.iloc[0]
    best_name = best_row["display_name"]

    text = (
        f"El mejor modelo según el promedio de rangos entre RMSE, MAE, R² y R² CV5 es "
        f"{best_name}. "
        f"Obtuvo RMSE={best_row['rmse']:.4f}, MAE={best_row['mae']:.4f}, "
        f"R²={best_row['r2']:.4f} y R² CV5={best_row['r2_cv5']:.4f}. "
        f"El criterio usado favorece simultáneamente errores bajos y capacidad explicativa alta."
    )

    return dbc.Card([
        dbc.CardBody([
            html.H5("Mejor modelo global", className="fw-bold mb-3"),
            html.P(text, className="mb-0")
        ])
    ], className="shadow-sm border-0")


def _build_comparison_rank_fig(comparison):
    if comparison.empty:
        return go.Figure()

    df_plot = comparison.sort_values("rank_mean", ascending=False)

    fig = px.bar(
        df_plot,
        x="rank_mean",
        y="display_name",
        orientation="h",
        title="Comparación global por promedio de rangos (menor es mejor)",
        labels={"rank_mean": "Promedio de rangos", "display_name": "Modelo"},
        color="rank_mean",
        color_continuous_scale=["#6c8ebf","#6c8ebf"]
    )
    fig.update_layout(
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="white",
        height=360,
        coloraxis_showscale=False
    )
    return fig


def layout():
    df = _get_df()
    meta = _get_meta()
    models = _models_dict(meta)
    comparison = _comparison_df(meta)

    default_model_key = meta.get("best_model_key")
    if default_model_key is None and models:
        default_model_key = next(iter(models.keys()))

    # =========================================================================
    # 1) EDA
    # =========================================================================
    target = df["T_0.01_RotD50"].astype(float)

    stats = {
        "Media": f"{target.mean():.5f} g",
        "Mediana": f"{target.median():.5f} g",
        "Desv. Est.": f"{target.std():.5f} g",
        "Mín": f"{target.min():.5f} g",
        "Máx": f"{target.max():.5f} g",
        "Coef. Var.": f"{(target.std()/target.mean()*100):.1f} %",
    }

    fig_hist = px.histogram(
        df, x="T_0.01_RotD50", nbins=50,
        title="Distribución de Sa(T=0.01 s) [g]",
        labels={"T_0.01_RotD50": "Sa(T=0.01 s) [g]"},
        color_discrete_sequence=["#6c8ebf"]
    )
    fig_hist.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white")

    fig_log = px.histogram(
        x=np.log(target), nbins=50,
        title="Distribución de log[Sa(T=0.01 s)]",
        labels={"x": "log(Sa) [log g]"},
        color_discrete_sequence=["#6c8ebf"]
    )
    fig_log.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white")

    fig_mag = px.scatter(
        df, x="Magnitude", y="T_0.01_RotD50", color="Soil_Class_label",
        opacity=0.65, title="Sa(T=0.01 s) vs Magnitud",
        labels={"Magnitude": "Magnitud Mw", "T_0.01_RotD50": "Sa [g]", "Soil_Class_label": "Tipo de sitio"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_mag.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white")

    fig_rrup = px.scatter(
        df, x="Rrup_OpenQuake", y="T_0.01_RotD50", color="Soil_Class_label",
        opacity=0.65, log_y=True, log_x=True,
        title="Sa(T=0.01 s) vs Rrup (log-log)",
        labels={"Rrup_OpenQuake": "Rrup [km]", "T_0.01_RotD50": "Sa [g]", "Soil_Class_label": "Tipo de sitio"},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_rrup.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white")

    fig_box = px.box(
        df, x="Soil_Class_label", y="T_0.01_RotD50", color="Soil_Class_label",
        log_y=True, title="Sa(T=0.01 s) por categoría de sitio",
        labels={"Soil_Class_label": "Categoría", "T_0.01_RotD50": "Sa [g]"},
        color_discrete_sequence=["#6c8ebf"],
        category_orders={"Soil_Class_label": list(SOIL_CLASS_LABELS.values())}
    )
    fig_box.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white", showlegend=False)

    df_soil_count = (
        df["Soil_Class_label"]
        .value_counts(dropna=False)
        .rename_axis("Soil_Class_label")
        .reset_index(name="count")
    )

    fig_soil_count = px.bar(
        df_soil_count, x="Soil_Class_label", y="count",
        title="Número de registros por categoría de sitio",
        labels={"Soil_Class_label": "Categoría de sitio", "count": "Número de registros"},
        color="Soil_Class_label",
        color_discrete_sequence=["#6c8ebf"],
        category_orders={"Soil_Class_label": list(SOIL_CLASS_LABELS.values())}
    )
    fig_soil_count.update_layout(template="plotly_white", plot_bgcolor="#f8f9fa", paper_bgcolor="white", showlegend=False)

    # =========================================================================
    # 2) RESULTADOS ESTÁTICOS DEL CONJUNTO
    # =========================================================================
    corr_cols = ["Magnitude", "Rrup_OpenQuake", "Hypocenter Depth (km)", "T_0.01_RotD50"]
    corr = df[corr_cols].corr(method="spearman")

    fig_corr = px.imshow(
        corr, text_auto=".2f", color_continuous_scale="Blues",
        zmin=-1, zmax=1,
        title="Correlación (Spearman) entre variables numéricas y Sa(T=0.01 s)",
        labels=dict(color="r")
    )
    fig_corr.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="#f8f9fa")

    df_spec = df.copy()
    for p, col in zip(_PERIODS, _SPEC_COLS):
        df_spec.loc[df_spec["Tmax"] < p, col] = np.nan

    median_spectra = {}
    for soil_class, label in SOIL_CLASS_LABELS.items():
        subset = df_spec[df_spec["Soil_Class"] == soil_class][_SPEC_COLS]
        median_spectra[label] = subset.median()

    fig_spec = go.Figure()
    colors = ["#3498db", "#2ecc71", "#e67e22", "#e74c3c", "#9b59b6"]
    for (label, vals), color in zip(median_spectra.items(), colors):
        fig_spec.add_trace(go.Scatter(
            x=_PERIODS,
            y=vals.values,
            mode="lines+markers",
            name=label,
            line=dict(color=color, width=2),
            marker=dict(size=5)
        ))

    fig_spec.update_layout(
        title="Espectros medianos de respuesta por tipo de sitio",
        xaxis_title="Período T [s]",
        yaxis_title="Sa [g]",
        xaxis_type="log",
        yaxis_type="log",
        template="plotly_white",
        plot_bgcolor="#f8f9fa",
        legend=dict(title="Tipo de sitio"),
        paper_bgcolor="white"
    )

    rank_fig = _build_comparison_rank_fig(comparison)

    model_options = [
        {"label": info["display_name"], "value": model_key}
        for model_key, info in models.items()
    ]

    comparison_show = comparison.copy()
    if not comparison_show.empty:
        comparison_show = comparison_show[
            ["overall_position", "display_name", "rmse", "mae", "r2", "r2_cv5", "rank_mean"]
        ].copy()
        comparison_show.columns = ["Posición", "Modelo", "RMSE", "MAE", "R²", "R² CV5", "Rank promedio"]

        for col in ["RMSE", "MAE", "R²", "R² CV5", "Rank promedio"]:
            comparison_show[col] = comparison_show[col].map(lambda x: f"{x:.4f}")

    return dbc.Container([

        dbc.Row(dbc.Col([
            html.H2("Resultados", className="fw-bold mt-4 mb-1", style={"color": "#2c3e50"}),
            html.P(
                "Análisis exploratorio de datos, comparación de modelos y evaluación del modelo seleccionado.",
                className="text-muted lead mb-4"
            ),
            html.Hr(),
        ])),

        dbc.Card([
            dbc.CardBody([
                html.H4("Análisis Exploratorio de Datos (EDA)", className="fw-bold mb-3"),
                html.P(
                    "Se analiza el comportamiento de la variable objetivo Sa(T=0.01 s), "
                    "su distribución en escala original y logarítmica, su relación con las "
                    "variables numéricas y las diferencias entre categorías de sitio.",
                    className="mb-0"
                )
            ])
        ], className="shadow-sm border-0 mb-4"),

        dbc.Row([
            dbc.Col(_metric_kpi(k, v, "", "#f0f4f8"), width=2, className="mb-3")
            for k, v in stats.items()
        ], className="g-2 mb-3"),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(figure=fig_hist, config={"displayModeBar": False}))],
                             className="shadow-sm border-0"), md=6, className="mb-4"),
            dbc.Col(dbc.Card([dbc.CardBody([
                dcc.Graph(figure=fig_log, config={"displayModeBar": False}),
                html.Small(
                    "La transformación logarítmica estabiliza la varianza y aproxima la distribución de Sa a un comportamiento lognormal.",
                    className="text-muted ms-3"
                )
            ])], className="shadow-sm border-0"), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(figure=fig_mag, config={"displayModeBar": False}))],
                             className="shadow-sm border-0"), md=6, className="mb-4"),
            dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(figure=fig_rrup, config={"displayModeBar": False}))],
                             className="shadow-sm border-0"), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(figure=fig_box, config={"displayModeBar": False}))],
                             className="shadow-sm border-0"), md=7, className="mb-4"),
            dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(figure=fig_soil_count, config={"displayModeBar": False}))],
                             className="shadow-sm border-0"), md=5, className="mb-4"),
        ]),

        dbc.Card([
            dbc.CardBody([
                html.H4("Evaluación interactiva del modelo", className="fw-bold mb-3"),
                html.P(
                    "Selecciona un modelo para ver su resumen singular, sus métricas y sus gráficos de evaluación.",
                    className="mb-3"
                ),
                dcc.Dropdown(
                    id="eval-model-selector",
                    options=model_options,
                    value=default_model_key,
                    clearable=False
                ),
            ])
        ], className="shadow-sm border-0 mb-4"),

        html.Div(id="eval-model-summary"),

        html.Div(id="eval-model-metrics"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(id="eval-rvp", config={"displayModeBar": False}))
            ], className="shadow-sm border-0"), md=6, className="mb-4"),

            dbc.Col(dbc.Card([
                dbc.CardBody(html.Div(id="eval-importance-container"))
            ], className="shadow-sm border-0"), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(id="eval-res", config={"displayModeBar": False}))
            ], className="shadow-sm border-0"), md=12, className="mb-4"),
        ]),

        dbc.Card([
            dbc.CardBody([
                html.H4("Información complementaria del conjunto", className="fw-bold mb-3"),
                html.P(
                    "Estos resultados no dependen del modelo seleccionado y ayudan a contextualizar la respuesta espectral del conjunto.",
                    className="mb-0"
                )
            ])
        ], className="shadow-sm border-0 mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=fig_corr, config={"displayModeBar": False}))
            ], className="shadow-sm border-0"), md=5, className="mb-4"),

            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=fig_spec, config={"displayModeBar": False}))
            ], className="shadow-sm border-0"), md=7, className="mb-4"),
        ]),

        dbc.Card([
            dbc.CardBody([
                html.H4("Resumen comparativo final", className="fw-bold mb-3"),
                html.P(
                    "Se comparan todos los modelos con base en RMSE, MAE, R² y R² CV5. "
                    "El mejor modelo se define usando el promedio de rangos entre esas métricas.",
                    className="mb-0"
                )
            ])
        ], className="shadow-sm border-0 mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody(
                    dbc.Table.from_dataframe(
                        comparison_show,
                        striped=True,
                        bordered=True,
                        hover=True,
                        responsive=True,
                        size="sm"
                    ) if not comparison_show.empty else dbc.Alert("No hay comparación disponible.", color="light")
                )
            ], className="shadow-sm border-0"), md=7, className="mb-4"),

            dbc.Col(dbc.Card([
                dbc.CardBody(dcc.Graph(figure=rank_fig, config={"displayModeBar": False}))
            ], className="shadow-sm border-0"), md=5, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(_build_best_model_summary(meta), md=12, className="mb-5")
        ]),

    ], fluid=True)


@callback(
    Output("eval-model-summary", "children"),
    Output("eval-model-metrics", "children"),
    Output("eval-rvp", "figure"),
    Output("eval-res", "figure"),
    Output("eval-importance-container", "children"),
    Input("eval-model-selector", "value"),
)
def update_model_evaluation(model_key):
    meta = _get_meta()
    models = _models_dict(meta)

    if not model_key or model_key not in models:
        return (
            dbc.Alert("Modelo no disponible.", color="warning"),
            html.Div(),
            go.Figure(),
            go.Figure(),
            dbc.Alert("Sin información de variables.", color="light")
        )

    model_info = models[model_key]
    model_name = model_info["display_name"]

    summary = _build_model_summary(model_key, meta)
    metrics_cards = _build_metrics_cards(model_info)
    fig_rvp = _build_rvp_fig(model_info, model_name)
    fig_res = _build_res_fig(model_info, model_name)
    importance = _build_feature_plot(model_info, model_name)

    return summary, metrics_cards, fig_rvp, fig_res, importance


def _metric_kpi(label, value, sub, bg):
    return dbc.Card([
        dbc.CardBody([
            html.H3(value, className="fw-bold mb-0", style={"color": "#2c3e50"}),
            html.H6(label, className="fw-semibold text-muted mb-1"),
            html.Small(sub, className="text-muted"),
        ], className="p-3 text-center")
    ], className="border-0 shadow-sm", style={"backgroundColor": bg})