import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Cargar la configuración desde 'config.yaml'
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Configurar el autenticador
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days'],
    preauthorized=config['preauthorized']
)

# Renderizar el formulario de inicio de sesión
nombre, estado_autenticacion, nombre_usuario = authenticator.login('Iniciar sesión', 'main')

if estado_autenticacion:
    # Mostrar botón de logout
    authenticator.logout('Cerrar sesión', 'sidebar')
    
    st.sidebar.write(f'Bienvenido/a *{nombre}*')
    st.title('Contenido de la aplicación')
    # Aquí puedes colocar el contenido principal de tu aplicación
elif estado_autenticacion == False:
    st.error('Nombre de usuario o contraseña incorrectos')
elif estado_autenticacion == None:
    st.warning('Por favor ingresa tu nombre de usuario y contraseña')

# Permitir registro de nuevos usuarios si no están autenticados
if estado_autenticacion != True:
    try:
        # Formulario de registro de usuario
        if authenticator.register_user('Regístrate', preauthorization=True):
            st.success('Usuario registrado exitosamente')
            st.info('Por favor, inicia sesión con tus credenciales')
    except Exception as e:
        st.error(e)
