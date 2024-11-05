import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests


# Título de la aplicación
st.title('Aplicación Web: Datos desde una API REST')
# URL de la API REST (puedes cambiarla por cualquier API pública que devuelva JSON)
api_url = 'https://jsonplaceholder.typicode.com/posts'
# Realizar la petición a la API
response = requests.get(api_url)
# Verificar que la respuesta sea exitosa (código 200)
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
    # Gráfico de barras basado en el conteo de IDs
    fig, ax = plt.subplots()
    df['userId'].value_counts().sort_index().plot(kind='bar', ax=ax)
    ax.set_title('Conteo de User ID')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Frecuencia')
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
