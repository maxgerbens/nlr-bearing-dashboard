import streamlit as st

pages = [
    st.Page("pages/1_Trendweergave.py", title="Trendweergave"),
    st.Page("pages/2_Vergelijkingsweergave.py", title="Vergelijkingsweergave"),
]

pg = st.navigation(pages)
pg.run()
