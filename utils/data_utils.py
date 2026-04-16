import os
import pandas as pd

RAW_TO_STD_COLS = {
    "Cat": "Soil_Class",
    "Tcorner": "Tmax",
}

SOIL_CLASS_LABELS = {
    "1": "Roca dura",
    "2": "Roca blanda",
    "3": "Suelo denso",
    "4": "Suelo blando",
    "5": "Suelo muy blando",
}

STATION_LAT_COL = "Station Latitude (deg positive N)"
STATION_LON_COL = "Station Longitude (deg positive E)"
EVENT_LAT_COL = "Epicenter Latitude (deg; positive N)"
EVENT_LON_COL = "Epicenter Longitude (deg; positive E)"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    rename_map = {
        old: new
        for old, new in RAW_TO_STD_COLS.items()
        if old in df.columns and new not in df.columns
    }
    df = df.rename(columns=rename_map)

    if "Soil_Class" in df.columns:
        df["Soil_Class"] = (
            df["Soil_Class"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
        )
        df["Soil_Class_label"] = df["Soil_Class"].map(SOIL_CLASS_LABELS)

    return df


def load_wide_dataset(base_dir: str) -> pd.DataFrame:
    path = os.path.join(base_dir, "espectros_Wide.csv")
    df = pd.read_csv(path)
    return normalize_columns(df)


def build_station_event_tables(df: pd.DataFrame):
    stations = (
        df[
            [
                "Station Code",
                "Station ID",
                STATION_LAT_COL,
                STATION_LON_COL,
                "Soil_Class",
                "Soil_Class_label",
            ]
        ]
        .dropna(subset=[STATION_LAT_COL, STATION_LON_COL])
        .drop_duplicates(subset=["Station Code", STATION_LAT_COL, STATION_LON_COL])
        .copy()
    )

    events = (
        df[
            [
                "EQID_Code",
                "EQID",
                EVENT_LAT_COL,
                EVENT_LON_COL,
                "Magnitude",
                "Hypocenter Depth (km)",
            ]
        ]
        .dropna(subset=[EVENT_LAT_COL, EVENT_LON_COL])
        .drop_duplicates(subset=["EQID_Code", EVENT_LAT_COL, EVENT_LON_COL])
        .copy()
    )

    links = (
        df[
            [
                "EQID_Code",
                "Station Code",
                "Magnitude",
                STATION_LAT_COL,
                STATION_LON_COL,
                EVENT_LAT_COL,
                EVENT_LON_COL,
            ]
        ]
        .dropna(subset=[STATION_LAT_COL, STATION_LON_COL, EVENT_LAT_COL, EVENT_LON_COL])
        .copy()
    )

    return stations, events, links