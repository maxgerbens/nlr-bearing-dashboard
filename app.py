"""
Startpagina van het NLR Bearing Dashboard.

Dit is het beginscherm dat de monteur als eerste ziet. Het legt kort uit wat het
dashboard doet en welke twee schermen er zijn. De schermen zelf staan in de map
'pages' en verschijnen automatisch in het menu links.

Starten met:   streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="NLR Bearing Dashboard", layout="wide")

st.title("NLR Bearing Dashboard")
st.write(
    "Dit dashboard maakt het slijtageverloop van lagers zichtbaar op basis van "
    "trillingsmetingen uit de XJTU-SY dataset. Het toont gegevens; het geeft geen "
    "voorspelling en geen vervangingsadvies. De interpretatie blijft bij de monteur."
)

st.header("De twee schermen")
st.markdown(
    "- **Trendweergave** — bekijk het verloop van één lager over zijn levensduur, "
    "met het falenmoment en het ruwe signaal.\n"
    "- **Vergelijkingsweergave** — zet meerdere lagers onder dezelfde conditie naast "
    "elkaar om afwijkend gedrag te herkennen."
)
st.info("Kies links in het menu een scherm om te beginnen.")

st.header("Wat betekenen de kenmerken?")
st.markdown(
    "- **RMS** — het gemiddelde trillingsniveau; loopt op bij slijtage.\n"
    "- **Kurtosis** — meet pieken in het signaal; stijgt bij beginnende schade.\n"
    "- **Crest factor** — verhouding piek/RMS; wijst op losse, schokkende trillingen."
)
