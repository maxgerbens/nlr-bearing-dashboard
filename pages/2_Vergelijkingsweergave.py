"""
Scherm 2 — Vergelijkingsweergave.

De monteur kiest een belastingsconditie en meerdere lagers, en ziet per kenmerk
alle gekozen lagers in één grafiek (US-2). Zo valt afwijkend gedrag op. Het
faulttype staat per lager in de legenda (FE-6).
"""

import streamlit as st

from src import charts, config, data

st.title("Vergelijkingsweergave")
st.write("Vergelijk meerdere lagers onder dezelfde belastingsconditie om afwijkend gedrag te herkennen.")

features = data.load_features()

# Stap 1: filter op conditie en kies de lagers die je wilt vergelijken (FE-7, FE-5).
condition = st.selectbox("Belastingsconditie", options=list(config.CONDITIONS), format_func=config.CONDITIONS.get)
available = data.bearings_in_condition(features, condition)
selected = st.multiselect("Lagers om te vergelijken", options=available, default=available[:2])

if len(selected) < 2:
    st.warning("Kies minstens twee lagers om te vergelijken.")
    st.stop()

# Stap 2: per kenmerk één grafiek met alle gekozen lagers (FE-5, NFE-3).
comparison = features[features["bearing"].isin(selected)]
for feature, explanation in config.FEATURE_LABELS.items():
    st.header(feature)
    st.plotly_chart(charts.comparison_chart(comparison, feature), use_container_width=True)
    st.caption(explanation)
