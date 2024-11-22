"""
Script description: Simplified login script using Streamlit-Authenticator.

Libraries imported:
- yaml: For loading configuration files.
- streamlit: For building the web application.
- streamlit_authenticator: For handling authentication.
"""

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import CredentialsError, LoginError, RegisterError

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# -------------------- Cargar Configuración --------------------
def load_config(config_path='config.yaml'):
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_config()

# -------------------- Crear Objeto Autenticador --------------------
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# -------------------- Widget de Inicio de Sesión --------------------
# Inicializar variables para evitar errores de variables no definidas
authentication_status = None
name = ""
username = ""

try:
    try:
        # Intentar usar la versión que retorna valores
        name, authentication_status, username = authenticator.login('Iniciar sesión', location='main')
    except TypeError:
        # Fallback para versiones que no retornan valores
        authenticator.login()
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
except LoginError as e:
    st.error(e)

# -------------------- Post-Autenticación --------------------
if authentication_status:
    # Mostrar opciones de cierre de sesión
    authenticator.logout('Cerrar sesión', 'sidebar')
    
    # Mensaje de bienvenida y contenido protegido
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
    new_name = st.text_input("Nombre Completo", key="new_name")
    new_username = st.text_input("Nombre de Usuario", key="new_username")
    new_email = st.text_input("Correo Electrónico", key="new_email")
    new_password = st.text_input("Contraseña", type="password", key="new_password")
    new_password_confirm = st.text_input("Confirmar Contraseña", type="password", key="new_password_confirm    ")
    submit_button = st.form_submit_button("Registrar")

    if submit_button:
        if new_password != new_password_confirm:
            st.error("Las contraseñas no coinciden.")
        elif new_username in config['credentials']['usernames']:
            st.error("El nombre de usuario ya existe.")
        else:
            try:
                # Registrar el nuevo usuario en la configuración
                hashed_password = stauth.Hasher([new_password]).generate()[0]  # Hashear contraseña
                config['credentials']['usernames'][new_username] = {
                    'name': new_name,
                    'email': new_email,
                    'password': hashed_password
                }
                save_config(config)  # Guardar la configuración actualizada
                st.success("Usuario registrado exitosamente.")
            except RegisterError as e:
                st.error(f"Error al registrar usuario: {e}")
