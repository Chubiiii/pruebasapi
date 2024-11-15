# Home.py
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Inicio", page_icon="🏠", layout="centered")

# Agregar una imagen
image = Image.open("imagen.png")
st.image(image, use_column_width=True)

# Título de bienvenida
st.title("¡Bienvenido a Nuestra Aplicación!")

# Descripción o mensaje
st.write("""
    Esta es la página de inicio de tu aplicación. Haz clic en el botón de abajo para iniciar sesión y acceder a todas las funcionalidades.
""")

# Botón de bienvenida
if st.button("Iniciar Sesión"):
    js = "window.location.href = '/Login'"
    html = f"<script>{js}</script>"
    st.markdown(html, unsafe_allow_html=True)
