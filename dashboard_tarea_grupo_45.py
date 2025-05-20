# --- CÓDIGO PARA dashboard_tarea_grupo_45.py ---
# (Este bloque NO se ejecuta directamente en Jupyter)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Carga de datos en archivo .csv
# Asegúrate de que el archivo data.csv esté en la misma carpeta que el script .py
try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    st.error("Error: 'data.csv' no encontrado. Asegúrate de que el archivo esté en la misma carpeta.")
    st.stop() # Detiene la ejecución si el archivo no se encuentra

st.title('Análisis Visual de Ventas de Tienda de Conveniencia')
st.markdown("""
Este dashboard presenta un análisis de las ventas, productos y clientes de una cadena de tiendas de conveniencia,
utilizando técnicas de visualización de datos.
""")

# --- Filtros Interactivos (Opcional pero recomendado) ---
st.sidebar.header('Filtros')

cities = df['City'].unique()
selected_city = st.sidebar.selectbox('Seleccionar Ciudad', ['Todas'] + list(cities))

product_lines = df['Product line'].unique()
selected_product_line = st.sidebar.selectbox('Seleccionar Línea de Producto', ['Todas'] + list(product_lines))

customer_types = df['Customer type'].unique()
selected_customer_type = st.sidebar.selectbox('Seleccionar Tipo de Cliente', ['Todos'] + list(customer_types))

# Aplicar filtros
filtered_df = df.copy()
if selected_city != 'Todas':
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if selected_product_line != 'Todas':
    filtered_df = filtered_df[filtered_df['Product line'] == selected_product_line]
if selected_customer_type != 'Todos':
    filtered_df = filtered_df[filtered_df['Customer type'] == selected_customer_type]

# Mostrar el dataframe filtrado (opcional)
# st.subheader('Datos Filtrados')
# st.dataframe(filtered_df.head()) # Muestra solo las primeras filas


# --- Visualizaciones ---

# 1. Evolución de las Ventas Totales
st.subheader('1. Evolución de las Ventas Totales')
if not filtered_df.empty:
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    ventas_por_fecha = filtered_df.groupby('Date')['Total'].sum().reset_index()
    st.line_chart(ventas_por_fecha.set_index('Date')['Total'])
    st.write("Este gráfico muestra la suma total de las ventas por cada día, basado en los filtros aplicados.")
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")


# 2. Ingresos por Línea de Producto
st.subheader('2. Ingresos por Línea de Producto')
if not filtered_df.empty:
    ingresos_por_producto = filtered_df.groupby('Product line')['Total'].sum().reset_index()
    ingresos_por_producto = ingresos_por_producto.sort_values('Total', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=ingresos_por_producto, x='Product line', y='Total', palette='viridis', ax=ax)
    ax.set_title('Ingresos Totales por Línea de Producto')
    ax.set_xlabel('Línea de Producto')
    ax.set_ylabel('Ingresos Totales')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    st.write("Compara los ingresos totales generados por cada línea de producto, considerando los filtros activos.")
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")


# 3. Distribución de la Calificación de Clientes
st.subheader('3. Distribución de la Calificación de Clientes')
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=filtered_df, x='Rating', bins=20, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribución de las Calificaciones de Clientes')
    ax.set_xlabel('Calificación (Rating)')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)
    st.write("Este histograma muestra la distribución de las calificaciones de los clientes según los filtros.")
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")


# 4. Comparación del Gasto por Tipo de Cliente
st.subheader('4. Comparación del Gasto por Tipo de Cliente')
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=filtered_df, x='Customer type', y='Total', ax=ax, palette='Set2')
    ax.set_title('Comparación del Gasto Total por Tipo de Cliente')
    ax.set_xlabel('Tipo de Cliente')
    ax.set_ylabel('Gasto Total')
    st.pyplot(fig)
    st.write("Compara la distribución del gasto total entre clientes 'Member' y 'Normal' bajo los filtros aplicados.")
else:
    st.write("No hay datos para mostrar con los filtros seleccionados.")

# Reflexión sobre la interactividad
st.markdown("---")
st.subheader("Reflexión sobre la interactividad")
st.write("""
La interactividad proporcionada por los filtros (Ciudad, Línea de Producto, Tipo de Cliente)
mejora significativamente la experiencia del usuario en este dashboard. Permite a los usuarios
explorar subconjuntos específicos de datos en tiempo real, sin necesidad de generar nuevos
gráficos o modificar código. Esto facilita la identificación de patrones y tendencias
particulares para cada ciudad, línea de producto o tipo de cliente.

Por ejemplo, un gerente de la tienda en "Yangon" puede filtrar por su ciudad para ver
específicamente la evolución de ventas en su sucursal, las líneas de producto más rentables
localmente o cómo se distribuyen las calificaciones de sus clientes. De manera similar,
un analista de marketing puede filtrar por "Member" para entender mejor el comportamiento
de gasto de los clientes miembros.

Esta capacidad de segmentación instantánea es crucial para tomar decisiones basadas en datos
más informadas y dirigidas, ya que permite un análisis más granular y pertinente a las
preguntas de negocio específicas.
""")