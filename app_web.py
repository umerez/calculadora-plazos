import streamlit as st
import pandas as pd
from datetime import date
import plazos 
import unicodedata
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="wide"
)

# --- MAPEO DE SEGURIDAD (Adaptado a tus archivos reales) ---
MAPEO_EXCEPCIONES = {
    "Coruña, A": "a-coruna.csv",
    "Araba/Álava": "araba_alava.csv",
    "Ciudad Real": "ciudad-real.csv",
    "Rioja, La": "la-rioja.csv",
    "Palmas, Las": "las-palmas.csv",
    "Santa Cruz de Tenerife": "tenerife.csv",
    "Balears, Illes": "baleares.csv",
    "Castellón/Castelló": "castellon.csv",
    "Valencia/València": "valencia.csv"
}

def normalizar_nombre_fichero(nombre_provincia):
    if nombre_provincia in MAPEO_EXCEPCIONES:
        return MAPEO_EXCEPCIONES[nombre_provincia]
    
    # Quitar tildes, minúsculas y sustituir espacios/comas
    s = unicodedata.normalize('NFD', nombre_provincia)
    s = s.encode('ascii', 'ignore').decode("utf-8")
    return f"{s.lower().strip().replace(',', '').replace(' ', '-')}.csv"

# --- CARGA DEL LISTADO DE PROVINCIAS ---
@st.cache_data(show_spinner=False)
def obtener_lista_provincias():
    fichero = "codprov.csv"
    if os.path.exists(fichero):
        try:
            with open(fichero, 'r', encoding='utf-8-sig') as f:
                lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
            lista_limpia = [l.replace('"', '') for l in lineas]
            if lista_limpia:
                return sorted(lista_limpia)
        except:
            pass
    return None

# 2. DISEÑO DE LA INTERFAZ
st.title("⚖️ Calculadora de Plazos Legales")

# --- BARRA LATERAL ---
st.sidebar.header("Configuración")

provincias = obtener_lista_provincias()

if provincias is None:
    st.sidebar.error("🚨 Error cargando 'codprov.csv'")
    provincias = ["Bizkaia", "Madrid", "Barcelona", "Gipuzkoa", "Araba/Álava"]
else:
    st.sidebar.success(f"✅ {len(provincias)} provincias disponibles")

provincia_seleccionada = st.sidebar.selectbox(
    "Selecciona Provincia", 
    options=provincias,
    index=provincias.index("Bizkaia") if "Bizkaia" in provincias else 0
)

# Carga de festivos
nombre_csv = normalizar_nombre_fichero(provincia_seleccionada)
festivos = plazos.leer_festivos_csv(nombre_csv)

if festivos:
    st.sidebar.success(f"Calendario: {nombre_csv}", icon="📅")
else:
    st.sidebar.error(f"Falta archivo: {nombre_csv}", icon="❌")

# Selector de Modo de Plazo
st.sidebar.divider()
modo_key = st.sidebar.selectbox(
    "Tipo de Plazo",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

# BOTÓN A TU WEB EN LA BARRA LATERAL
st.sidebar.divider()
st.sidebar.link_button("🌐 Visitar umerez.eu", "https://umerez.eu", use_container_width=True, type="primary")

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Fecha de inicio", date.today())
    unidad = st.radio("Unidad", ["Días", "Meses"])
with col2:
    duracion = st.number_input("Plazo", min_value=1, value=10)
    tipo_dia = st.selectbox("Días", ["Hábiles", "Naturales"]) if unidad == "Días" else "Meses"

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
        with st.expander("Ver detalle del cálculo"):
            for linea in logs: st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error: {e}")

# --- PIE DE PÁGINA Y AVISO LEGAL ---
st.divider()

st.markdown("""
### Información sobre la aplicación
Esta herramienta es un **calendario de plazos procesales y administrativos** diseñado para facilitar el cómputo de vencimientos. 
Funciona aplicando de forma automatizada las reglas de días hábiles, exclusión de festivos locales/nacionales y periodos de inhabilidad (Agosto y Navidad) según la normativa vigente (Ley 39/2015, LEC y LJCA).

Creado por **Esteban Umerez**, con la asistencia de **ChatGPT** (OpenAI) y **Gemini** (Google). 
Puedes encontrar más recursos en [umerez.eu](https://umerez.eu).

---
**Aviso Legal:**
Esta aplicación se ofrece "tal cual" (*as is*), con fines puramente informativos y orientativos. El autor no garantiza la ausencia total de errores técnicos o de cálculo y **no se responsabiliza** de los posibles fallos en los resultados obtenidos, ni de las acciones, omisiones o decisiones legales que los usuarios adopten basándose en el cálculo realizado por esta herramienta. Se recomienda encarecidamente contrastar siempre los resultados con los calendarios oficiales de cada sede judicial o administrativa.
""")
