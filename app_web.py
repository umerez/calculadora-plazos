import streamlit as st
import pandas as pd
from datetime import date
import plazos  # Importa tu motor plazos.py
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="wide"
)

# --- LÓGICA DE CORRESPONDENCIA DE ARCHIVOS ---

def obtener_nombre_archivo(provincia_display):
    """
    Mapea el nombre del selector con el nombre real del archivo en GitHub.
    """
    # Diccionario de casos especiales para coincidir con tus archivos
    excepciones = {
        "Coruña, A": "a-coruna.csv",
        "Araba/Álava": "araba_alava.csv",
        "Castellón/Castelló": "castellon.csv",
        "Ciudad Real": "ciudad-real.csv",
        "Rioja, La": "la-rioja.csv",
        "Palmas, Las": "las-palmas.csv",
        "Santa Cruz de Tenerife": "tenerife.csv",
        "Valencia/València": "valencia.csv",
        "Balears, Illes": "baleares.csv"
    }
    
    if provincia_display in excepciones:
        return excepciones[provincia_display]
    
    # Para el resto: quitar tildes, minúsculas y cambiar espacios por guiones medios
    texto = unicodedata.normalize('NFD', provincia_display)
    texto = texto.encode('ascii', 'ignore').decode("utf-8")
    return f"{texto.lower().replace(' ', '-')}.csv"

# --- INTERFAZ ---

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("Cómputo de plazos según Ley 39/2015, LEC y LJCA. *Por Esteban Umerez.*")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración")

@st.cache_data
def cargar_provincias():
    try:
        df = pd.read_csv("codprov.csv", header=None)
        return df[0].tolist()
    except:
        return ["Bizkaia", "Madrid", "Barcelona"]

lista_provincias = cargar_provincias()
provincia_sel = st.sidebar.selectbox("Provincia/Ciudad", options=lista_provincias, index=lista_provincias.index("Bizkaia") if "Bizkaia" in lista_provincias else 0)

# Localizar archivo
nombre_fichero = obtener_nombre_archivo(provincia_sel)
festivos = plazos.leer_festivos_csv(nombre_fichero)

if festivos:
    st.sidebar.success(f"Calendario cargado: {nombre_fichero}", icon="✅")
else:
    st.sidebar.error(f"No encontrado: {nombre_fichero}", icon="🚨")

# Configuración del modo
st.sidebar.divider()
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]
st.sidebar.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Fecha de inicio", date.today())
    unidad = st.radio("Unidad", ["Días", "Meses"])
with col2:
    duracion = st.number_input(f"Cantidad", min_value=1, value=10)
    tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"]) if unidad == "Días" else "Meses"

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

        st.success(f"### Vencimiento: {vencimiento.strftime('%d/%m/%Y')}")
        with st.expander("Ver detalle paso a paso"):
            for linea in logs: st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error: {e}")
