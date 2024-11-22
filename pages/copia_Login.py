import bcrypt
import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError

# -------------------- Configuración de la Página --------------------
st.set_page_config(page_title="Login", page_icon="🔑", layout="wide")

# -------------------- Cargar Configuración --------------------
def load_config(config_path='config.yaml'):
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

def save_config(config, config_path='config.yaml'):
    """Guardar configuración actualizada en el archivo YAML."""
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

config = load_config()

# -------------------- Estilo CSS --------------------
st.markdown("""
    <style>
        body {
            background-color: #e3edfc;
            font-family: 'Arial', sans-serif;
        }
        .main-container {
            display: flex;
            justify-content: space-between;
            margin: 50px auto;
            max-width: 900px;
        }
        .form-container {
            background-color: #7c83db;
            padding: 30px;
            border-radius: 15px;
            width: 45%;
            color: white;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-container h2 {
            text-align: center;
            margin-bottom: 20px;
            font-size: 24px;
            font-weight: bold;
        }
        .form-container label {
            font-size: 16px;
            font-weight: bold;
        }
        .form-container input {
            margin-top: 10px;
            margin-bottom: 20px;
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .form-container button {
            background-color: #005fa3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }
        .form-container button:hover {
            background-color: #00407a;
        }
        .link {
            text-align: center;
            margin-top: 10px;
        }
        .link a {
            color: #ffdd99;
            text-decoration: none;
        }
        .link a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Dividir Página en Secciones --------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# -------------------- Sección de Inicio de Sesión --------------------
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<h2>Iniciar Sesión</h2>', unsafe_allow_html=True)

with st.form("login_form"):
    username = st.text_input("Usuario", key="login_username")
    password = st.text_input("Contraseña", type="password", key="login_password")
    login_button = st.form_submit_button("Iniciar Sesión")

    if login_button:
        try:
            authenticator = stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days']
            )
            name, authentication_status, username = authenticator.login('Iniciar sesión', location='main')

            if authentication_status:
                st.success(f"¡Bienvenido {name}!")
            elif authentication_status is False:
                st.error("Nombre de usuario o contraseña incorrectos.")
            else:
                st.warning("Por favor ingresa tus credenciales.")
        except LoginError as e:
            st.error(e)

st.markdown('<div class="link"><a href="#">¿Olvidaste tu contraseña?</a></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Sección de Registro --------------------
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<h2>Crear Cuenta</h2>', unsafe_allow_html=True)

with st.form("registration_form"):
    new_name = st.text_input("Nombre Completo", key="register_name")
    new_username = st.text_input("Nombre de Usuario", key="register_username")
    new_email = st.text_input("Correo Electrónico", key="register_email")
    new_password = st.text_input("Contraseña", type="password", key="register_password")
    new_password_confirm = st.text_input("Confirmar Contraseña", type="password", key="register_password_confirm")
    submit_button = st.form_submit_button("Registrar")

    if submit_button:
        if not new_name or not new_username or not new_email or not new_password:
            st.error("Por favor, completa todos los campos.")
        elif new_password != new_password_confirm:
            st.error("Las contraseñas no coinciden.")
        elif new_username in config['credentials']['usernames']:
            st.error("El nombre de usuario ya existe.")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            config['credentials']['usernames'][new_username] = {
                'name': new_name,
                'email': new_email,
                'password': hashed_password
            }
            save_config(config)
            st.success("Usuario registrado exitosamente.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
