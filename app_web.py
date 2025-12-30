import streamlit as st
import pandas as pd
from datetime import date
import plazos  # Tu motor de cálculo
import os

# Configuración de la página
st.set_page_config(page_title="Calculadora de Plazos Umerez", page_icon="⚖️", layout="wide")

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("""
Calculadora de vencimientos procesales y administrativos (Ley 39/2015, LEC y LJCA).
Por Esteban Umerez.
""")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración de Calendario")

# 1. Cargar el listado de provincias desde codprov.csv
@st.cache_data
def cargar_nombres_provincias():
    try:
        # Leemos el archivo que subiste
        df = pd.read_csv("codprov.csv", header=None)
        return df[0].tolist()
    except:
        return ["Bizkaia", "Gipuzkoa", "Araba/Álava", "Madrid"] # Fallback por si falla

lista_provincias = cargar_nombres_provincias()

# 2. Selector de Provincia
provincia_seleccionada = st.sidebar.selectbox(
    "Selecciona la Provincia/Ciudad",
    options=lista_provincias,
    index=lista_provincias.index("Bizkaia") if "Bizkaia" in lista_provincias else 0
)

# 3. Construir el nombre del archivo automáticamente
# Limpiamos el nombre: minúsculas, quitamos barras y espacios
nombre_limpio = provincia_seleccionada.lower().replace("/", "_").replace(" ", "_")
archivo_csv = f"{nombre_limpio}.csv"

# Carga de festivos
festivos = plazos.leer_festivos_csv(archivo_csv)

if festivos:
    st.sidebar.success(f"Calendario de {provincia_seleccionada} cargado.", icon="✅")
else:
    st.sidebar.warning(f"No se encontró el archivo: {archivo_csv}. Se usará calendario sin festivos locales.", icon="⚠️")

# 4. Selector de Modo de Cálculo
st.sidebar.divider()
st.sidebar.header("Reglas de Cómputo")
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

st.sidebar.divider()
st.sidebar.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input("Fecha de inicio", date.today())
    unidad = st.radio("Unidad del plazo", ["Días", "Meses"])

with col2:
    duracion = st.number_input(f"Número de {unidad.lower()}", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])
    else:
        tipo_dia = "Meses"

if st.button("Calcular Vencimiento"):
    st.divider()
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                vencimiento = fecha_inicio + plazos.timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        st.success(f"### El vencimiento es el: {vencimiento.strftime('%d/%m/%Y')}")
        with st.expander("Ver detalle del cómputo"):
            for linea in logs:
                st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
