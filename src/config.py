from pathlib import Path

# Hoofdmap van het project (de map waarin dit project staat).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Map met de ruwe XJTU-SY meetbestanden (de CSV's per lager).
DATA_DIR = PROJECT_ROOT / "data"

# Bestand met de vooraf berekende kenmerken. Wordt gemaakt door build_features.py
# en ingelezen door het dashboard. Klein bestand -> snel laden (NFE-1).
FEATURES_FILE = PROJECT_ROOT / "features.csv"

# We berekenen de kenmerken op de horizontale trillingsas. Dit is in de XJTU-SY
# literatuur de meest gebruikte as om degradatie te volgen.
SIGNAL_COLUMN = "Horizontal_vibration_signals"

# Bemonsteringsfrequentie van de sensor: 25.600 metingen per seconde.
SAMPLING_RATE_HZ = 25_600

# Een ruw meetbestand bevat 32.768 metingen (1,28 seconde). Dat is te veel om
# leesbaar te tonen, dus laten we het eerste deel zien (hier: 0,1 seconde).
RAW_SIGNAL_PREVIEW_SAMPLES = 2_560

# De drie belastingscondities. De sleutel is de mapnaam in data/, de waarde is
# het label dat de monteur op het scherm ziet.
CONDITIONS = {
    "35Hz12kN": "35 Hz / 12 kN",
    "37.5Hz11kN": "37,5 Hz / 11 kN",
    "40Hz10kN": "40 Hz / 10 kN",
}

# Het faulttype per lager, overgenomen uit Tabel 2 van de dataset-documentatie.
# Dit is bekende, vaste informatie en hoort daarom hier thuis (FE-6).
FAULT_TYPES = {
    "Bearing1_1": "Outer race",
    "Bearing1_2": "Outer race",
    "Bearing1_3": "Outer race",
    "Bearing1_4": "Cage",
    "Bearing1_5": "Inner race + outer race",
    "Bearing2_1": "Inner race",
    "Bearing2_2": "Outer race",
    "Bearing2_3": "Cage",
    "Bearing2_4": "Outer race",
    "Bearing2_5": "Outer race",
    "Bearing3_1": "Outer race",
    "Bearing3_2": "Inner race + ball + cage + outer race",
    "Bearing3_3": "Inner race",
    "Bearing3_4": "Inner race",
    "Bearing3_5": "Outer race",
}

# De drie kenmerken die we tonen. De sleutel is de kolomnaam in features.csv,
# de waarde is een korte Nederlandse uitleg onder de grafiek (NFE-3).
FEATURE_LABELS = {
    "rms": "RMS — het gemiddelde trillingsniveau. Loopt op naarmate het lager slijt.",
    "kurtosis": "Kurtosis — meet pieken in het signaal. Stijgt bij beginnende schade.",
    "crest_factor": "Crest factor — verhouding piek/RMS. Wijst op losse, schokkende trillingen.",
}
