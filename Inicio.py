#PIL = libreria para el manejo de imagenes, base64 = libreria para insertar imagenes con html
import streamlit as st
from PIL import Image
import base64

# Configuración de la página
st.set_page_config(page_title="Inicio", page_icon="🏠", layout="wide")

# Función para cargar la imagen y convertirla a base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

#Eliminar barra lateral, o bloquearla
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Ruta de la imagen
image_path = "imagen.png" 
image_base64 = get_image_as_base64(image_path)

# Código HTML y CSS
st.markdown(
    f"""
    <style>
    .background {{
        position: relative;
        text-align: center; /* alineado al centro del contenedor
    }}
    .background img {{
        width: 100%; 
        height: auto; /* se ajusta a su ancho maximo, y se ajusta la altura proporcionalmente */
    }}
    .button-overlay {{
        position: absolute;
        bottom: 50px; 
        left: 50%;
        transform: translateX(-50%); /* ajustes varios de posicion para el contenedor del boton */
    }}
    .button-overlay button {{
        padding: 15px 32px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease; /* ajustes varios para el estilo del boton */
    }}
    .button-overlay button:hover {{
        background-color: #45a049; /* efecto al pasar cursor */
    }}
    </style>

    /* clase fondo, aca se aplican los estilos css, se carga la imagen en una version apta para la pagina, y se referencia el boton continuar a la pagina login */
    <div class="background">
        <img src="data:image/png;base64,{image_base64}" alt="Background">
        <div class="button-overlay">
            <a href="/Login" target="_self">
                <button>Continuar</button>
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
