import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from datetime import date
import matplotlib.pyplot as plt

# Crear tabla si no existe
def create_database():
    conn = sqlite3.connect('finanzas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            descripcion TEXT,
            categoria TEXT,
            monto REAL
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutar la creación de la base de datos
create_database()

# Conectar con la base de datos
conn = sqlite3.connect('finanzas.db')
engine = create_engine('sqlite:///finanzas.db')

# Título de la App
st.title('App de Finanzas Personales')

# Formulario para registrar transacciones
st.header('Registrar una Transacción')
fecha = st.date_input('Fecha', date.today())
descripcion = st.text_input('Descripción')
categoria = st.selectbox('Categoría', ['Ingreso', 'Gasto'])
monto = st.number_input('Monto', step=0.01)

if st.button('Agregar Transacción'):
    nueva_transaccion = {
        'fecha': fecha,
        'descripcion': descripcion,
        'categoria': categoria,
        'monto': monto
    }
    df = pd.DataFrame([nueva_transaccion])
    df.to_sql('transacciones', con=engine, if_exists='append', index=False)
    st.success('Transacción agregada!')

# Mostrar transacciones
st.header('Transacciones Registradas')
df = pd.read_sql('SELECT * FROM transacciones', con=conn)

# Asegurarse de que las fechas sean interpretadas correctamente
df['fecha'] = pd.to_datetime(df['fecha'])

st.write(df)

# Filtro de fechas
st.header('Filtrar Transacciones por Fecha')
start_date = st.date_input('Fecha de inicio', date.today())
end_date = st.date_input('Fecha de fin', date.today())

if start_date and end_date:
    df_filtrado = df[(df['fecha'] >= pd.to_datetime(start_date)) & (df['fecha'] <= pd.to_datetime(end_date))]
    st.write(df_filtrado)

# Gráfico de gastos por descripción
st.header('Gastos por Descripción')
if not df.empty:
    df_gastos = df[df['categoria'] == 'Gasto']
    fig, ax = plt.subplots()
    df_gastos.groupby('descripcion')['monto'].sum().plot(kind='bar', ax=ax)
    ax.set_ylabel('Monto')
    ax.set_title('Gastos por Descripción')

    # Añadir etiquetas a las barras
    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

# Resumen Financiero
st.header('Análisis de Datos')
if not df.empty:
    ingresos = df[df['categoria'] == 'Ingreso']['monto'].sum()
    gastos = df[df['categoria'] == 'Gasto']['monto'].sum()
    st.write(f"Total Ingresos: {ingresos}")
    st.write(f"Total Gastos: {gastos}")

    st.subheader('Gráfico de Ingresos vs Gastos')
    fig, ax = plt.subplots()
    df.groupby('categoria')['monto'].sum().plot(kind='bar', ax=ax)

    # Añadir etiquetas a las barras
    for i in ax.containers:
        ax.bar_label(i, label_type='edge')

    st.pyplot(fig)

    st.subheader('Evolución de las Finanzas')
    fig, ax = plt.subplots()
    ingresos_df = df[df['categoria'] == 'Ingreso']
    gastos_df = df[df['categoria'] == 'Gasto']
    ingresos_df.groupby('fecha')['monto'].sum().plot(kind='line', ax=ax, label='Ingresos', color='green')
    gastos_df.groupby('fecha')['monto'].sum().plot(kind='line', ax=ax, label='Gastos', color='red')

    # Añadir etiquetas a los puntos de datos
    for i, v in ingresos_df.groupby('fecha')['monto'].sum().items():
        ax.text(i, v, f'{v:.2f}', color='green', ha='right', va='bottom')
    for i, v in gastos_df.groupby('fecha')['monto'].sum().items():
        ax.text(i, v, f'{v:.2f}', color='red', ha='right', va='bottom')

    ax.legend()
    st.pyplot(fig)
