"""
De drie trillingskenmerken die het dashboard toont.

Dit bestand bevat alleen wiskunde: het kent geen bestanden, mappen of grafieken.
Elke functie krijgt een reeks meetwaarden (het trillingssignaal) en geeft één
getal terug. Zo zijn de kenmerken los te lezen en los te controleren.
"""

import numpy as np


def rms(signal: np.ndarray) -> float:
    """RMS (Root Mean Square): het effectieve trillingsniveau.

    Wortel van het gemiddelde van de gekwadrateerde waarden. Hoe meer een lager
    trilt, hoe hoger de RMS.
    """
    return float(np.sqrt(np.mean(signal**2)))


def kurtosis(signal: np.ndarray) -> float:
    """Kurtosis: hoe "piekerig" het signaal is.

    Een gaaf lager trilt gelijkmatig (kurtosis rond 3). Beginnende schade geeft
    korte, scherpe pieken, waardoor de kurtosis stijgt.
    """
    mean = np.mean(signal)
    standard_deviation = np.std(signal)
    return float(np.mean((signal - mean) ** 4) / standard_deviation**4)


def crest_factor(signal: np.ndarray) -> float:
    """Crest factor: de verhouding tussen de hoogste piek en het RMS-niveau.

    Een hoge crest factor betekent dat er losse, schokkende uitschieters zijn
    ten opzichte van het gemiddelde trillingsniveau.
    """
    peak = np.max(np.abs(signal))
    return float(peak / rms(signal))
