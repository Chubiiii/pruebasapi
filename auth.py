import streamlit as st
import streamlit_authenticator as stauth

# Definir nombres de usuarios y contraseñas
nombres = ['Usuario Uno', 'Usuario Dos']
nombres_usuario = ['usuario1', 'usuario2']
contraseñas = ['contraseña1', 'contraseña2']

# Encriptar las contraseñas
hashed_passwords = stauth.Hasher(contraseñas).generate()

# Configurar el autenticador
authenticator = stauth.Authenticate(
    nombres,
    nombres_usuario,
    hashed_passwords,
    'nombre_cookie',
    'clave_firma',
    cookie_expiry_days=30
)

# Renderizar el formulario de inicio de sesión
nombre, estado_autenticacion, nombre_usuario = authenticator.login('Iniciar sesión', 'main')

if estado_autenticacion:
    st.write(f'Bienvenido/a *{nombre}*')
    st.write('Accediste exitosamente a la aplicación.')
    # Aquí puedes colocar el resto de tu aplicación
elif estado_autenticacion == False:
    st.error('Nombre de usuario o contraseña incorrectos')
elif estado_autenticacion == None:
    st.warning('Por favor ingresa tu nombre de usuario y contraseña')
