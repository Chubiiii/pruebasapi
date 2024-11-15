import streamlit as st
from PIL import Image, UnidentifiedImageError

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Inicio", page_icon="🏠", layout="wide")

# -------------------- Función para Cargar la Imagen --------------------
def cargar_imagen(path):
    try:
        imagen = Image.open(path)
        return imagen
    except FileNotFoundError:
        st.error(f"No se encontró la imagen en la ruta especificada: {path}")
    except UnidentifiedImageError:
        st.error(f"No se pudo identificar la imagen. Asegúrate de que el archivo {path} sea una imagen válida.")
    except Exception as e:
        st.error(f"Ocurrió un error al cargar la imagen: {e}")

# Ruta de la imagen
ruta_imagen = "imagen.png"  # Reemplaza con la ruta correcta si está en una subcarpeta

# Cargar la imagen
imagen_fondo = cargar_imagen(ruta_imagen)

# -------------------- Mostrar la Imagen de Fondo --------------------
if imagen_fondo:
    st.image(imagen_fondo, use_column_width=True)

    # -------------------- Contenedor para el Botón --------------------
    button_container = st.empty()

    with button_container.container():
        # Crear tres columnas con proporciones [1, 2, 1] para centrar el botón
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("Continuar"):
                # Acción al hacer clic en el botón
                # Por ejemplo, cambiar los parámetros de consulta para navegar a la página de Login
                st.experimental_set_query_params(page="Login")
                st.experimental_rerun()
