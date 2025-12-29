import streamlit as st
from datetime import date
import plazos  # Importamos tu motor de cálculo plazos.py

# Configuración de la página
st.set_page_config(
   page_title="Calculadora de Plazos Umerez",
   page_icon="⚖️",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("""
Esta herramienta calcula vencimientos procesales y administrativos, aplicando 
las reglas de los artículos 30 de la Ley 39/2015, 133 de la LEC y 128 de la LJCA. 
Por Esteban Umerez, con ayuda de ChatGPT y Gemini.
""")

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("Configuración de Calendario")

# 1. Selección del archivo de festivos
archivos_disponibles = {
    "Bizkaia y Gipuzkoa": "festivos_bizkaia_gipuzkoa.csv",
    "Araba": "festivos_araba.csv",
    "España (Nacionales)": "festivos_españa.csv"
}

seleccion_nombre = st.sidebar.selectbox(
    "Selecciona el Calendario de Festivos",
    options=list(archivos_disponibles.keys()),
    index=0
)

archivo_seleccionado = archivos_disponibles[seleccion_nombre]

# Carga de festivos
festivos = plazos.leer_festivos_csv(archivo_seleccionado)

if festivos:
    st.sidebar.success(f"Calendario '{seleccion_nombre}' cargado.", icon="✅")
else:
    st.sidebar.error(f"Error: No se encuentra el archivo {archivo_seleccionado}", icon="🚨")

# 2. Selección de Modo de Cálculo
st.sidebar.divider()
st.sidebar.header("Reglas de Cómputo")
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

# --- NUEVO: BOTÓN DE ENLACE EXTERNO ---
st.sidebar.divider()
st.sidebar.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)

# --- CUERPO PRINCIPAL (Entrada de datos) ---
col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input("Fecha de inicio (notificación/publicación)", date.today())
    unidad = st.radio("Unidad del plazo", ["Días", "Meses"])

with col2:
    duracion = st.number_input(f"Número de {unidad.lower()}", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])
    else:
        tipo_dia = "Meses"

# --- CÁLCULO ---
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

st.info(f"**Modo activo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
