"""
Script description: Optimized login script using Streamlit-Authenticator.

Libraries imported:
- yaml: For loading configuration files.
- streamlit: For building the web application.
- streamlit_authenticator: For handling authentication.
"""

import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import (
    CredentialsError,
    LoginError,
    RegisterError
)

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# -------------------- Cargar Configuración --------------------
@st.cache_resource
def load_config(config_path='config.yaml'):
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_config()

# -------------------- Crear Objeto Autenticador --------------------
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# -------------------- Widget de Inicio de Sesión --------------------
try:
    name, authentication_status, username = authenticator.login('Iniciar sesión', 'main')
except LoginError as e:
    st.error(e)

# -------------------- Post-Autenticación --------------------
if authentication_status:
    authenticator.logout('Cerrar sesión', 'sidebar')
    st.sidebar.write(f'Bienvenido/a *{name}*')
    st.title('Contenido de la Aplicación')
    st.write("Aquí va el contenido principal de tu aplicación.")

elif authentication_status is False:
    st.error('Nombre de usuario o contraseña incorrectos.')

elif authentication_status is None:
    st.warning('Por favor, ingresa tu nombre de usuario y contraseña.')

# -------------------- Registro de Nuevos Usuarios --------------------
st.markdown("---")
st.header("Registrar Nuevo Usuario")

with st.form("registration_form"):
    new_name = st.text_input("Nombre Completo")
    new_username = st.text_input("Nombre de Usuario")
    new_email = st.text_input("Correo Electrónico")
    new_password = st.text_input("Contraseña", type="password")
    new_password_confirm = st.text_input("Confirmar Contraseña", type="password")
    submit_button = st.form_submit_button("Registrar")

    if submit_button:
        if new_password != new_password_confirm:
            st.error("Las contraseñas no coinciden.")
        elif new_username in config['credentials']['usernames']:
            st.error("El nombre de usuario ya existe.")
        else:
            try:
                authenticator.register_user(
                    name=new_name,
                    email=new_email,
                    username=new_username,
                    password=new_password,
                    config=config
                )
                st.success("Usuario registrado exitosamente.")
                
                # Guardar la configuración actualizada
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            except RegisterError as e:
                st.error(e)
