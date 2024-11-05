import requests
import pandas as pd
import streamlit as st
st.title("Aplicacion web, datos desde una API")
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

if response.status_code == 200:
    # Convertir los datos JSON en un DataFrame de Pandas
    data = response.json()
    df = pd.DataFrame(data)
    # Mostrar los primeros registros
    st.write('Datos obtenidos de la API:')
    st.write(df.head())
    # Seleccionar una columna para mostrar en Streamlit
    columnas = st.multiselect('Selecciona las columnas a visualizar',
    df.columns.tolist(), default=df.columns.tolist())
    df_seleccionado = df[columnas]
    # Mostrar el DataFrame con las columnas seleccionadas
    st.write('Datos seleccionados:')
    st.write(df_seleccionado)
    # Filtro por ID
    id_filtro = st.slider('Filtrar por ID (entre 1 y 100)', 1, 100, 50)
    df_filtrado = df[df['id'] <= id_filtro]
    st.write(f'Mostrando datos donde ID <= {id_filtro}:')
    st.write(df_filtrado)