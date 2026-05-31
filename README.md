# NLR Bearing Dashboard

Een dashboard dat het slijtageverloop van lagers zichtbaar maakt op basis van
trillingsmetingen uit de XJTU-SY dataset. Het toont gegevens en geeft geen
voorspelling of vervangingsadvies; de interpretatie blijft bij de monteur.

## Wat het dashboard doet

- **Trendweergave** — het verloop van RMS, kurtosis en crest factor van één lager
  over zijn levensduur, met het falenmoment en het ruwe signaal.
- **Vergelijkingsweergave** — meerdere lagers onder dezelfde belastingsconditie
  naast elkaar, om afwijkend gedrag te herkennen.

## Installatie

Je hebt Python 3.9 of nieuwer nodig.

```bash
pip install -r requirements.txt
```

## Gebruik

Stap 1 — bereken eenmalig de kenmerken (maakt `features.csv` aan):

```bash
python build_features.py
```

Stap 2 — start het dashboard:

```bash
streamlit run app.py
```

Het dashboard opent in de browser. Kies links in het menu een scherm.

## Opbouw van de code

De code is opgesplitst zodat elk bestand één taak heeft:

| Bestand | Taak |
|---------|------|
| `build_features.py` | Berekent eenmalig de kenmerken naar `features.csv`. |
| `src/config.py` | Instellingen: paden, condities, faulttypes. Eén bron van waarheid. |
| `src/features.py` | De berekeningen: RMS, kurtosis, crest factor. |
| `src/data.py` | Inlezen van `features.csv` en van ruwe meetbestanden. |
| `src/charts.py` | De grafieken. |
| `app.py` | Startpagina. |
| `pages/` | De twee schermen. |

## Databron

XJTU-SY Bearing Dataset (Wang et al., 2018, DOI: 10.1109/TR.2018.2882682):
run-to-failure trillingsdata van 15 lagers onder 3 belastingscondities. Elke CSV
is één meetmoment van 1 minuut (32.768 metingen op 25,6 kHz). Het laatste
meetbestand van een lager is het moment van falen.
