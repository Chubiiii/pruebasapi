"""
Script description: Simplified login script using Streamlit-Authenticator.

Libraries imported:
- yaml: For loading configuration files.
- streamlit: For building the web application.
- streamlit_authenticator: For handling authentication.
"""

import bcrypt 
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
        
def save_config(config, config_path='config.yaml'):
    """Guardar configuración actualizada en el archivo YAML."""
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


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
    new_name = st.text_input("Nombre Completo")
    new_username = st.text_input("Nombre de Usuario")
    new_email = st.text_input("Correo Electrónico")
    new_password = st.text_input("Contraseña", type="password")
    new_password_confirm = st.text_input("Confirmar Contraseña", type="password")
    submit_button = st.form_submit_button("Registrar")

    if submit_button:
        if not new_name or not new_username or not new_email or not new_password:
            st.error("Por favor, completa todos los campos.")
        elif new_password != new_password_confirm:
            st.error("Las contraseñas no coinciden.")
        elif new_username in config['credentials']['usernames']:
            st.error("El nombre de usuario ya existe.")
        else:
            # Hash de la contraseña
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Agregar usuario al archivo de configuración
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'email': new_email,
                'password': hashed_password
            }

            try:
                save_config(config)  # Guardar los cambios en el archivo
                st.success("Usuario registrado exitosamente.")
            except Exception as e:
                st.error(f"Error al guardar configuración: {e}")
    
