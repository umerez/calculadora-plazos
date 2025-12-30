import streamlit as st
import pandas as pd
from datetime import date
import plazos 
import unicodedata
import os

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="wide"
)

# --- MAPEO MANUAL DE SEGURIDAD ---
# Esto asegura que los archivos con nombres "raros" se encuentren sí o sí
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
    # Si está en el mapa de excepciones, lo devolvemos directamente
    if nombre_provincia in MAPEO_EXCEPCIONES:
        return MAPEO_EXCEPCIONES[nombre_provincia]
    
    # Para el resto: Quitar tildes, minúsculas y espacios por guiones medios
    # Ejemplo: "Zaragoza" -> "zaragoza.csv"
    s = unicodedata.normalize('NFD', nombre_provincia)
    s = s.encode('ascii', 'ignore').decode("utf-8")
    return f"{s.lower().strip().replace(' ', '-')}.csv"

# --- CARGA DEL LISTADO DE PROVINCIAS ---
@st.cache_data
def obtener_lista_provincias():
    # Intentamos leer el archivo con diferentes variantes de nombre
    posibles_nombres = ["codprov.csv", "Codprov.csv", "CODPROV.CSV"]
    for nombre in posibles_nombres:
        if os.path.exists(nombre):
            try:
                # 'utf-8-sig' ayuda a leer archivos guardados desde Excel/Windows
                df = pd.read_csv(nombre, header=None, encoding='utf-8-sig')
                lista = df[0].dropna().astype(str).tolist()
                return [p.strip() for p in lista if p.strip()]
            except:
                continue
    return None

# --- DISEÑO DE LA APLICACIÓN ---
st.title("⚖️ Calculadora de Plazos Legales")

# Intentar cargar provincias
provincias = obtener_lista_provincias()

if provincias is None:
    st.sidebar.error("🚨 No se encontró el archivo 'codprov.csv' en GitHub.")
    # Lista de emergencia por si el archivo falla
    provincias = ["Bizkaia", "Madrid", "Barcelona", "Gipuzkoa", "Araba/Álava"]
else:
    st.sidebar.success(f"✅ Se han cargado {len(provincias)} provincias.")

# Selector de Provincia
provincia_seleccionada = st.sidebar.selectbox(
    "Selecciona Provincia", 
    options=provincias,
    index=provincias.index("Bizkaia") if "Bizkaia" in provincias else 0
)

# Determinar y cargar el archivo de festivos
nombre_csv = normalizar_nombre_fichero(provincia_seleccionada)
festivos = plazos.leer_festivos_csv(nombre_csv)

if festivos:
    st.sidebar.success(f"Calendario: {nombre_csv}", icon="📅")
else:
    st.sidebar.error(f"Archivo no encontrado: {nombre_csv}", icon="❌")

# --- SELECTOR DE MODO ---
st.sidebar.divider()
modo_key = st.sidebar.selectbox(
    "Tipo de Plazo",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]
st.sidebar.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)

# --- ENTRADA DE DATOS Y CÁLCULO ---
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

st.info(f"**Modo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
