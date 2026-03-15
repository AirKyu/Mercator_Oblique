import streamlit as st
import streamlit.components.v1 as components

# Interface Streamlit
st.set_page_config(page_title="Mercator Oblique Explorer", layout="wide")

# On charge le fichier HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# On affiche le composant dans Streamlit
st.title("🗺️ Projection Mercator Oblique Interactive")
st.markdown("Utilisez les flèches du clavier ou le globe en bas à droite pour naviguer.")

components.html(html_code, height=900, scrolling=True)
