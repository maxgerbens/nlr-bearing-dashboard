"""
Alle toegang tot bestanden op één plek.

De schermen weten niets van mappen of CSV-paden; ze vragen hier de gegevens op.
De resultaten worden in het geheugen bewaard (st.cache_data), zodat een lager
dat al eens is opgevraagd direct opnieuw verschijnt (NFE-1: trend < 2 seconden).
"""

import numpy as np
import pandas as pd
import streamlit as st

from src import config


@st.cache_data
def load_features() -> pd.DataFrame:
    """Leest de vooraf berekende kenmerken uit features.csv.

    Voegt twee handige kolommen toe die we uit config halen: het leesbare
    conditie-label en het faulttype van het lager.
    """
    table = pd.read_csv(config.FEATURES_FILE)
    table["condition_label"] = table["condition"].map(config.CONDITIONS)
    table["fault_type"] = table["bearing"].map(config.FAULT_TYPES)
    return table


def bearings_in_condition(features: pd.DataFrame, condition: str) -> list[str]:
    """Geeft de lagernamen die bij één belastingsconditie horen (FE-7)."""
    rows = features[features["condition"] == condition]
    return sorted(rows["bearing"].unique())


def measurements_of_bearing(features: pd.DataFrame, bearing: str) -> pd.DataFrame:
    """Geeft alle meetmomenten van één lager, op volgorde van minuut (FE-2)."""
    rows = features[features["bearing"] == bearing]
    return rows.sort_values("minute")


def failure_minute(features: pd.DataFrame, bearing: str) -> int:
    """Geeft de minuut van het falenmoment: het laatste meetmoment van het lager.

    De dataset is run-to-failure, dus de laatste meting is het moment van falen
    (FE-3).
    """
    return int(measurements_of_bearing(features, bearing)["minute"].max())


@st.cache_data
def load_raw_signal(condition: str, bearing: str, minute: int) -> np.ndarray:
    """Leest het ruwe trillingssignaal van één meetmoment (FE-4).

    Een meetbestand heet "<minuut>.csv" en bevat 32.768 metingen. We geven de
    horizontale as terug als reeks getallen.
    """
    file_path = config.DATA_DIR / condition / bearing / f"{minute}.csv"
    measurement = pd.read_csv(file_path)
    return measurement[config.SIGNAL_COLUMN].to_numpy()
