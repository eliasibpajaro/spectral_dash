"""
model/train_model.py
--------------------
Entrena múltiples modelos para predecir Sa(T=0.01 s, RotD50)
y guarda:
- el mejor pipeline en model.pkl (para la pestaña de predicción),
- el resumen completo de comparación en meta.pkl.

Modelos incluidos:
- Regresión lineal
- XGBoost
- Random Forest
- SVR con kernel RBF
- MLP
"""

import os
import sys
import copy
import joblib
import numpy as np
import pandas as pd

from xgboost import XGBRegressor

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from utils.data_utils import SOIL_CLASS_LABELS, load_wide_dataset

MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
META_PATH = os.path.join(BASE_DIR, "model", "meta.pkl")

TARGET = "T_0.01_RotD50"
TARGET_PERIOD = 0.01
MASK_COL = "Tmax"
RANDOM_STATE = 42
TEST_SIZE = 0.2

NUMERIC_FEATURES = [
    "Magnitude",
    "Rrup_OpenQuake",
    "Hypocenter Depth (km)",
    "log_Rrup",
    "Mag_logRrup",
    "Mag2",
    "log_Depth",
]
CATEGORICAL_FEATURES = ["Soil_Class"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Soil_Class"] = df["Soil_Class"].astype(str)
    df["log_Rrup"] = np.log(df["Rrup_OpenQuake"].clip(lower=1e-6))
    df["Mag_logRrup"] = df["Magnitude"] - df["log_Rrup"]
    df["Mag2"] = df["Magnitude"] ** 2
    df["log_Depth"] = np.log(df["Hypocenter Depth (km)"].clip(lower=1))

    return df


def build_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)

    if scale_numeric:
        num_transformer = Pipeline([
            ("scaler", StandardScaler())
        ])
    else:
        num_transformer = "passthrough"

    return ColumnTransformer(
        transformers=[
            ("num", num_transformer, NUMERIC_FEATURES),
            ("cat", ohe, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def get_model_specs():
    return {
        "linear_regression": {
            "display_name": "Regresión lineal",
            "scale_numeric": True,
            "estimator": LinearRegression(),
        },
        "xgboost": {
            "display_name": "XGBoost",
            "scale_numeric": False,
            "estimator": XGBRegressor(
                objective="reg:squarederror",
                eval_metric="rmse",
                n_estimators=500,
                learning_rate=0.04,
                max_depth=4,
                min_child_weight=3,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.0,
                reg_lambda=1.0,
                tree_method="hist",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        },
        "random_forest": {
            "display_name": "Random Forest",
            "scale_numeric": False,
            "estimator": RandomForestRegressor(
                n_estimators=400,
                max_depth=None,
                min_samples_leaf=2,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        },
        "svr_rbf": {
            "display_name": "SVR (RBF)",
            "scale_numeric": True,
            "estimator": SVR(
                kernel="rbf",
                C=10.0,
                epsilon=0.05,
                gamma="scale",
            ),
        },
        "mlp": {
            "display_name": "MLP",
            "scale_numeric": True,
            "estimator": MLPRegressor(
                hidden_layer_sizes=(64, 32),
                activation="relu",
                solver="adam",
                alpha=1e-3,
                learning_rate_init=1e-3,
                max_iter=1200,
                early_stopping=True,
                random_state=RANDOM_STATE,
            ),
        },
    }


def build_pipeline(model_key: str) -> Pipeline:
    spec = get_model_specs()[model_key]
    return Pipeline([
        ("prep", build_preprocessor(scale_numeric=spec["scale_numeric"])),
        ("model", clone(spec["estimator"])),
    ])


def load_and_prepare():
    df = load_wide_dataset(BASE_DIR)

    mask_valid = df[MASK_COL] >= TARGET_PERIOD
    df_valid = df.loc[mask_valid].copy()

    print(f"  Registros totales : {len(df)}")
    print(f"  Registros válidos : {len(df_valid)}  ({MASK_COL} >= {TARGET_PERIOD} s)")

    df_valid = engineer_features(df_valid)
    df_clean = df_valid.dropna(subset=ALL_FEATURES + [TARGET]).copy()

    print(f"  Registros limpios : {len(df_clean)}")

    X = df_clean[ALL_FEATURES].copy()
    y = np.log(df_clean[TARGET].astype(float))

    return X, y, df_clean


def extract_feature_scores(pipeline: Pipeline):
    prep = pipeline.named_steps["prep"]
    model = pipeline.named_steps["model"]

    try:
        feature_names = prep.get_feature_names_out().tolist()
    except Exception:
        return {}, None

    if hasattr(model, "feature_importances_"):
        scores = np.asarray(model.feature_importances_, dtype=float)
        total = scores.sum()
        if total > 0:
            scores = scores / total
        return dict(zip(feature_names, scores.tolist())), "importance"

    if hasattr(model, "coef_"):
        coef = np.asarray(model.coef_, dtype=float).ravel()
        scores = np.abs(coef)
        total = scores.sum()
        if total > 0:
            scores = scores / total
        return dict(zip(feature_names, scores.tolist())), "coef_abs"

    return {}, None


def train_all_models(X: pd.DataFrame, y: pd.Series):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    fitted_pipelines = {}
    models_meta = {}

    specs = get_model_specs()

    for model_key, spec in specs.items():
        print(f"\n  → Entrenando {spec['display_name']}...")

        pipeline = build_pipeline(model_key)
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        cv_r2 = cross_val_score(pipeline, X, y, cv=cv, scoring="r2").mean()

        feature_scores, feature_score_kind = extract_feature_scores(pipeline)

        models_meta[model_key] = {
            "display_name": spec["display_name"],
            "metrics": {
                "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
                "mae": float(mean_absolute_error(y_test, y_pred)),
                "r2": float(r2_score(y_test, y_pred)),
                "r2_cv5": float(cv_r2),
            },
            "y_test": y_test.tolist(),
            "y_pred": y_pred.tolist(),
            "n_test": int(len(y_test)),
            "feature_scores": feature_scores,
            "feature_score_kind": feature_score_kind,
        }

        fitted_pipelines[model_key] = pipeline

    return fitted_pipelines, models_meta, X_train, X_test


def build_comparison(models_meta: dict) -> pd.DataFrame:
    rows = []
    for model_key, info in models_meta.items():
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

    df["rank_rmse"] = df["rmse"].rank(method="min", ascending=True)
    df["rank_mae"] = df["mae"].rank(method="min", ascending=True)
    df["rank_r2"] = df["r2"].rank(method="min", ascending=False)
    df["rank_r2_cv5"] = df["r2_cv5"].rank(method="min", ascending=False)

    df["rank_mean"] = df[["rank_rmse", "rank_mae", "rank_r2", "rank_r2_cv5"]].mean(axis=1)

    df = df.sort_values(
        by=["rank_mean", "rank_rmse", "rank_mae", "r2"],
        ascending=[True, True, True, False]
    ).reset_index(drop=True)

    df["overall_position"] = np.arange(1, len(df) + 1)
    return df


def main():
    print("=" * 72)
    print(" Entrenamiento comparativo — Sa(T=0.01 s)")
    print(" Modelos: LR | XGBoost | RF | SVR-RBF | MLP")
    print("=" * 72)

    print("\n[1/3] Cargando y preparando datos...")
    X, y, _ = load_and_prepare()

    print("\n[2/3] Entrenando modelos...")
    fitted_pipelines, models_meta, X_train, X_test = train_all_models(X, y)

    comparison_df = build_comparison(models_meta)
    best_row = comparison_df.iloc[0]
    best_model_key = best_row["model_key"]
    best_model_name = best_row["display_name"]

    print("\n[3/3] Guardando modelo ganador y metadatos...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    meta = {
        "features": ALL_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "target": TARGET,
        "target_period": TARGET_PERIOD,
        "mask_column": MASK_COL,
        "log_transform": True,
        "comparison_metric": "average_rank",
        "best_model_key": best_model_key,
        "best_model_name": best_model_name,
        "soil_class_mapping": SOIL_CLASS_LABELS,
        "models": models_meta,
        "comparison": comparison_df.to_dict(orient="records"),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }

    joblib.dump(fitted_pipelines[best_model_key], MODEL_PATH)
    joblib.dump(meta, META_PATH)

    print(f"  Mejor modelo → {best_model_name}")
    print(f"  Pipeline para predicción → {MODEL_PATH}")
    print(f"  Metadatos comparativos → {META_PATH}")

    print("\nResumen comparativo:")
    print(
        comparison_df[
            ["overall_position", "display_name", "rmse", "mae", "r2", "r2_cv5", "rank_mean"]
        ].to_string(index=False)
    )

    print("\n✓ Listo.")


if __name__ == "__main__":
    main()