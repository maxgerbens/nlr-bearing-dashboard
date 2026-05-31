"""
Scherm 1 — Trendweergave.

De monteur kiest een belastingsconditie en een lager, en ziet het verloop van de
drie kenmerken over de hele levensduur (US-3), met het falenmoment erin (US-4).
Daaronder kan hij het ruwe signaal van één meetmoment bekijken (US-5).
"""

import streamlit as st

from src import charts, config, data

st.title("Trendweergave")
st.write("Bekijk hoe een lager slijt over zijn levensduur. Kies hieronder een conditie en een lager.")

features = data.load_features()

# Stap 1: filter op belastingsconditie en kies een lager (FE-7, FE-1).
condition = st.selectbox("Belastingsconditie", options=list(config.CONDITIONS), format_func=config.CONDITIONS.get)
bearing = st.selectbox("Lager", options=data.bearings_in_condition(features, condition))

# Toon het faulttype van dit lager (FE-6).
st.info(f"Faulttype van dit lager: **{config.FAULT_TYPES[bearing]}**")

measurements = data.measurements_of_bearing(features, bearing)
failure = data.failure_minute(features, bearing)

# Stap 2: één trendgrafiek per kenmerk, met het falenmoment en een uitleg (FE-2, FE-3, NFE-3).
st.header("Trendverloop")
for feature, explanation in config.FEATURE_LABELS.items():
    st.plotly_chart(charts.trend_chart(measurements, feature, failure), use_container_width=True)
    st.caption(explanation)

# Stap 3: ruw trillingssignaal van een gekozen meetmoment (FE-4, US-5).
st.header("Ruw trillingssignaal")
st.write("Kies een meetmoment om de onbewerkte meting op detailniveau te bekijken.")
minute = st.select_slider("Meetmoment (minuut)", options=list(measurements["minute"]))

signal = data.load_raw_signal(condition, bearing, minute)
st.plotly_chart(charts.raw_signal_chart(signal), use_container_width=True)
st.caption(
    f"Ruwe meting op minuut {minute}. Eerste {config.RAW_SIGNAL_PREVIEW_SAMPLES} metingen "
    f"(circa 0,1 s) van de horizontale as, bemonsterd op {config.SAMPLING_RATE_HZ:,} Hz."
)
