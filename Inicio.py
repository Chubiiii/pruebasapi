import streamlit as st

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Inicio", page_icon="🏠", layout="wide")

# -------------------- Crear un Contenedor de Pantalla Completa --------------------
with st.container():
    # Dividir la página en una sola columna
    col = st.columns(1)[0]
    
    # Mostrar la imagen en la columna
    col.image("imagen.png", use_column_width=True)
    
    # Espacio flexible para empujar el botón hacia abajo
    col.empty()
    
    # Crear un contenedor para el botón centrado
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
    
    with button_col2:
        if st.button("Continuar"):
            # Acción al hacer clic en el botón
            st.experimental_set_query_params(page="Login")
            st.experimental_rerun()
