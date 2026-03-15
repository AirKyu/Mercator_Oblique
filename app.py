import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mercator Oblique V15", layout="wide")

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.title("🗺️ Simulateur de Projection Oblique")
st.write("Naviguez sur le globe ou utilisez les flèches. Les boutons ↺ et ↻ font pivoter la Terre sur l'axe de la vue.")

components.html(html_code, height=950, scrolling=True)
