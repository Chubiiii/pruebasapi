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
ruta_imagen = "imagen.png"  # Asegúrate de que esta ruta sea correcta

# Cargar la imagen
imagen_fondo = cargar_imagen(ruta_imagen)

# -------------------- Contenedor Principal --------------------
if imagen_fondo:
    with st.container():
        # Mostrar la imagen
        st.image(imagen_fondo, use_column_width=True)
        
        # Espacio flexible reducido
        for _ in range(15):  # Menos iteraciones para subir el botón
            st.write("")
        
        # Crear columnas para centrar el botón
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Continuar"):
                # Acción al hacer clic en el botón
                st.experimental_set_query_params(page="Login")
                st.experimental_rerun()
