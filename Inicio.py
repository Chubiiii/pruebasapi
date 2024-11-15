import streamlit as st

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Inicio", page_icon="🏠", layout="wide")

# -------------------- Mostrar Imagen de Fondo --------------------
image_path = Image.open("imagen.png")

try:
    st.image(image_path, use_column_width=True)
except FileNotFoundError:
    st.error(f"No se encontró la imagen en la ruta especificada: {image_path}")
except Exception as e:
    st.error(f"Error al cargar la imagen: {e}")

# -------------------- Contenedor para el Botón --------------------
button_container = st.empty()

# Crear tres columnas y colocar el botón en la columna central dentro del contenedor
with button_container.container():
    # Usar columnas para centrar el botón
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("Continuar"):
            # Acción al hacer clic en el botón, por ejemplo, redirigir a otra página
            st.experimental_set_query_params(page="Login")
            st.experimental_rerun()
