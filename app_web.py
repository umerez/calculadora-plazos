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

# --- MAPEO DE SEGURIDAD ---
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
    s = unicodedata.normalize('NFD', nombre_provincia)
    s = s.encode('ascii', 'ignore').decode("utf-8")
    return f"{s.lower().strip().replace(',', '').replace(' ', '-')}.csv"

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

# --- BARRA LATERAL (DESCRIPCIÓN Y DISCLAIMER) ---
with st.sidebar:
    st.header("Sobre esta Aplicación")
    st.markdown("""
    Esta herramienta es un **calendario de plazos procesales y administrativos** diseñado para facilitar el cómputo de vencimientos. 
    
    Aplica de forma automatizada las reglas de:
    * Días hábiles e inhábiles.
    * Exclusión de festivos locales y nacionales.
    * Periodos de inhabilidad (Agosto y Navidad) según la normativa vigente (Ley 39/2015, LEC y LJCA).

    **Créditos:** Creado por **Esteban Umerez**, con la asistencia de **ChatGPT** (OpenAI) y **Gemini** (Google).
    """)
    
    st.link_button("🌐 Visitar umerez.eu", "https://umerez.eu", use_container_width=True)
    
    st.divider()
    st.caption("⚠️ **Aviso Legal:**")
    st.caption("""
    Esta aplicación se ofrece "tal cual" (*as is*), con fines orientativos. El autor no garantiza la ausencia de errores y **no se responsabiliza** de los resultados obtenidos ni de las decisiones legales adoptadas basadas en este cálculo. Se recomienda contrastar los resultados con los calendarios oficiales.
    """)

# --- INTERFAZ PRINCIPAL ---
st.title("⚖️ Calculadora de Plazos Legales")

# 1. Fila de Configuración (Provincia y Tipo de Plazo)
provincias = obtener_lista_provincias()
if provincias is None:
    st.error("🚨 Error cargando 'codprov.csv'")
    provincias = ["Bizkaia", "Madrid", "Barcelona", "Gipuzkoa", "Araba/Álava"]

c1, c2 = st.columns(2)

with c1:
    provincia_seleccionada = st.selectbox(
        "Selecciona Provincia", 
        options=provincias,
        index=provincias.index("Bizkaia") if "Bizkaia" in provincias else 0
    )
    # Carga de festivos y aviso inmediato debajo
    nombre_csv = normalizar_nombre_fichero(provincia_seleccionada)
    festivos = plazos.leer_festivos_csv(nombre_csv)
    
    if festivos:
        st.success(f"Calendario de {provincia_seleccionada} cargado (archivo: {nombre_csv})", icon="✅")
    else:
        st.error(f"No se encontró el archivo: {nombre_csv}", icon="🚨")

with c2:
    modo_key = st.selectbox(
        "Tipo de Procedimiento / Plazo",
        options=list(plazos.MODOS_CALCULO.keys()),
        format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
    )
    config = plazos.MODOS_CALCULO[modo_key]
    st.info(f"**Reglas:** Agosto {'inhábil' if config['agosto_inhabil'] else 'hábil'} | Navidad {'inhábil' if config['navidad_inhabil'] else 'hábil'}")

st.divider()

# 2. Fila de Entrada de Datos (Fecha y Cantidad)
col_a, col_b = st.columns(2)

with col_a:
    fecha_inicio = st.date_input("Fecha de inicio (notificación/publicación)", date.today())
    unidad = st.radio("📏 Unidad del plazo", ["Días", "Meses"], horizontal=True)

with col_b:
    duracion = st.number_input("Duración del plazo", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])
    else:
        tipo_dia = "Meses"

# 3. Botón de Cálculo y Resultados
if st.button("Calcular Vencimiento", use_container_width=True, type="primary"):
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                vencimiento = fecha_inicio + plazos.timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        st.success(f"## Vencimiento: {vencimiento.strftime('%d/%m/%Y')}")
        with st.expander("🔍 Ver detalle del cómputo paso a paso"):
            for linea in logs:
                st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
