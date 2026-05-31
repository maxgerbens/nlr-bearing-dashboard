"""
Stap 1 (eenmalig uitvoeren): bereken de kenmerken en sla ze op.

Sommige lagers hebben duizenden meetbestanden van elk 32.768 metingen. Die elke
keer opnieuw inlezen zou het dashboard traag maken. Daarom rekenen we hier
eenmalig per meetmoment de drie kenmerken uit en schrijven we het resultaat naar
een klein bestand: features.csv. Het dashboard leest daarna alleen dat bestand.

Draai dit script één keer met:   python build_features.py
"""

import pandas as pd

from src import config, features


def measurement_files_in_order(bearing_dir):
    """Geeft de meetbestanden van een lager op volgorde van minuut.

    De bestanden heten "1.csv", "2.csv", ... waarbij het nummer de minuut is.
    We sorteren op dat nummer, niet op tekst (anders komt "10" vóór "2").
    """
    files = bearing_dir.glob("*.csv")
    return sorted(files, key=lambda path: int(path.stem))


def compute_rows_for_bearing(condition: str, bearing_dir) -> list[dict]:
    """Berekent voor elk meetmoment van één lager de drie kenmerken."""
    rows = []
    for measurement_file in measurement_files_in_order(bearing_dir):
        minute = int(measurement_file.stem)
        measurement = pd.read_csv(measurement_file)
        signal = measurement[config.SIGNAL_COLUMN].to_numpy()
        rows.append(
            {
                "condition": condition,
                "bearing": bearing_dir.name,
                "minute": minute,
                "rms": features.rms(signal),
                "kurtosis": features.kurtosis(signal),
                "crest_factor": features.crest_factor(signal),
            }
        )
    return rows


def build_features_table() -> pd.DataFrame:
    """Loopt over alle condities en lagers en verzamelt alle kenmerk-regels."""
    all_rows = []
    for condition in config.CONDITIONS:
        condition_dir = config.DATA_DIR / condition
        for bearing_dir in sorted(condition_dir.iterdir()):
            if not bearing_dir.is_dir():
                continue
            print(f"Bezig met {condition} / {bearing_dir.name} ...")
            all_rows.extend(compute_rows_for_bearing(condition, bearing_dir))
    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    table = build_features_table()
    table.to_csv(config.FEATURES_FILE, index=False)
    print(f"Klaar: {len(table)} meetmomenten opgeslagen in {config.FEATURES_FILE}")
