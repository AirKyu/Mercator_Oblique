import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page pour qu'elle prenne tout l'espace
st.set_page_config(page_title="Mercator Oblique", layout="wide")

# Lecture du fichier HTML
with open("index.html", 'r', encoding='utf-8') as f:
    html_data = f.read()

# Affichage du composant HTML
# Note : 'height' définit la hauteur de la fenêtre de la carte
components.html(html_data, height=800, scrolling=True)
