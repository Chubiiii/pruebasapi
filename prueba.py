# Login.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Cargar la configuración desde 'config.yaml'
with open('config.yaml') as file:
    config = yaml.safe_load(file)

# Configurar el autenticador
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
    preauthorized=config.get('preauthorized')
)

# Renderizar el formulario de inicio de sesión
nombre, estado_autenticacion, nombre_usuario = authenticator.login('Iniciar sesión', 'main')

if estado_autenticacion:
    authenticator.logout('Cerrar sesión', 'sidebar')
    st.sidebar.write(f'Bienvenido/a *{nombre}*')
    st.title('Contenido de la aplicación')
    # Aquí coloca el contenido principal de tu aplicación
elif estado_autenticacion == False:
    st.error('Nombre de usuario o contraseña incorrectos')
elif estado_autenticacion == None:
    st.warning('Por favor ingresa tu nombre de usuario y contraseña')

# Registro de nuevos usuarios
if estado_autenticacion != True:
    try:
        if authenticator.register_user('Regístrate', preauthorization=False):
            st.success('Usuario registrado exitosamente')
            st.info('Por favor, inicia sesión con tus credenciales')
    except Exception as e:
        st.error(e)
