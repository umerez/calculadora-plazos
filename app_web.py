import streamlit as st
import pandas as pd
from datetime import date
import plazos  # Importa tu motor plazos.py
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- FUNCIONES DE APOYO ---

def normalizar_para_archivo(texto):
    """
    Convierte 'Araba/Álava' en 'araba_alava'
    Convierte 'Coruña, A' en 'coruna_a'
    """
    # 1. Quitar tildes y normalizar
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode("utf-8")
    # 2. Reemplazos de caracteres
    texto = texto.lower()
    texto = texto.replace("/", "_")
    texto = texto.replace(" ", "_")
    texto = texto.replace(",", "")
    return texto.strip("_")

@st.cache_data
def cargar_provincias():
    try:
        # Lee el archivo codprov.csv que tienes en la raíz
        df = pd.read_csv("codprov.csv", header=None)
        return df[0].tolist()
    except Exception as e:
        return ["Bizkaia", "Gipuzkoa", "Araba/Álava", "Madrid"]

# --- INTERFAZ ---

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("""
Calculadora de vencimientos procesales y administrativos. 
*Por Esteban Umerez.*
""")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración de Calendario")

# 1. Selector de Provincia
lista_provincias = cargar_provincias()
provincia_sel = st.sidebar.selectbox(
    "Selecciona la Provincia/Ciudad",
    options=lista_provincias,
    index=lista_provincias.index("Bizkaia") if "Bizkaia" in lista_provincias else 0
)

# 2. Carga del archivo correspondiente
nombre_fichero = f"{normalizar_para_archivo(provincia_sel)}.csv"
festivos = plazos.leer_festivos_csv(nombre_fichero)

if festivos:
    st.sidebar.success(f"Calendario '{provincia_sel}' cargado correctamente.", icon="✅")
else:
    st.sidebar.error(f"No se encontró el archivo: {nombre_fichero}", icon="🚨")
    st.sidebar.info("Asegúrate de que el nombre del archivo en GitHub sea exactamente el indicado arriba.")

# 3. Selector de Modo de Cálculo
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
                # Lógica para naturales
                vencimiento = fecha_inicio + plazos.timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        # Mostrar resultado
        st.success(f"### El vencimiento es el: {vencimiento.strftime('%d/%m/%Y')}")
        
        with st.expander("Ver detalle del cómputo paso a paso"):
            for linea in logs:
                st.write(f"- {linea}")

    except Exception as e:
        st.error(f"Error en el cálculo: {e}")

st.info(f"**Modo activo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
