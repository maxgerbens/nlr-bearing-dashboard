"""
De grafieken van het dashboard, los van de schermen.

Elke functie krijgt kant-en-klare gegevens en geeft een grafiek terug. Zo blijven
de schermen kort en leesbaar, en staat alle teken-logica op één plek.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src import config


def trend_chart(measurements: pd.DataFrame, feature: str, failure_minute: int) -> go.Figure:
    """Trend van één kenmerk over de levensduur, met het falenmoment erin (FE-2, FE-3).

    De x-as is de tijd in minuten, de y-as het kenmerk. Een rode stippellijn
    markeert het moment van falen.
    """
    figure = px.line(measurements, x="minute", y=feature, labels={"minute": "Tijd (minuten)", feature: feature})
    figure.add_vline(
        x=failure_minute,
        line_dash="dash",
        line_color="red",
        annotation_text="Falenmoment (laatste meting)",
        annotation_hovertext=(
            "Het laatste meetmoment van dit lager. De dataset is run-to-failure, "
            "dus hier is het lager bezweken."
        ),
    )
    return figure


def comparison_chart(measurements: pd.DataFrame, feature: str) -> go.Figure:
    """Eén kenmerk voor meerdere lagers in dezelfde grafiek (FE-5, FE-6).

    Elk lager krijgt een eigen kleur. De legenda toont per lager het faulttype,
    zodat afwijkend gedrag te koppelen is aan een soort schade.
    """
    measurements = measurements.copy()
    measurements["Lager (faulttype)"] = measurements["bearing"] + " (" + measurements["fault_type"] + ")"
    figure = px.line(
        measurements,
        x="minute",
        y=feature,
        color="Lager (faulttype)",
        labels={"minute": "Tijd (minuten)", feature: feature},
    )

    # Faalmarkering per lager (Scherm 2): een verticale lijn op het laatste
    # meetmoment van elk lager, in dezelfde kleur als zijn lijn. Zo ziet de
    # monteur in één oogopslag welk lager eerder faalt.
    failure_minutes = measurements.groupby("Lager (faulttype)")["minute"].max()
    for trace in figure.data:
        figure.add_vline(
            x=failure_minutes[trace.name],
            line_dash="dash",
            line_color=trace.line.color,
        )
    return figure


def raw_signal_chart(signal: np.ndarray) -> go.Figure:
    """Het ruwe trillingssignaal van één meetmoment (FE-4).

    We tonen het eerste deel van de meting (zie config) en zetten de x-as om naar
    seconden, zodat de monteur de meeteenheid herkent.
    """
    preview = signal[: config.RAW_SIGNAL_PREVIEW_SAMPLES]
    seconds = np.arange(len(preview)) / config.SAMPLING_RATE_HZ
    return px.line(
        x=seconds,
        y=preview,
        labels={"x": "Tijd (seconden)", "y": "Trilling (g)"},
    )
