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

# --- DICCIONARIO DE MAPEO EXACTO ---
# Mapea lo que sale en el menú con el nombre real de tu archivo en GitHub
MAPEO_ARCHIVOS = {
    "Araba/Álava": "araba_alava.csv",
    "Coruña, A": "a-coruna.csv",
    "Ciudad Real": "ciudad-real.csv",
    "Rioja, La": "la-rioja.csv",
    "Palmas, Las": "las-palmas.csv",
    "Santa Cruz de Tenerife": "tenerife.csv",
    "Balears, Illes": "baleares.csv",
    "Castellón/Castelló": "castellon.csv",
    "Valencia/València": "valencia.csv"
}

def obtener_nombre_archivo(provincia_display):
    if provincia_display in MAPEO_ARCHIVOS:
        return MAPEO_ARCHIVOS[provincia_display]
    
    # Para el resto: quitar tildes y poner minúsculas
    # Ejemplo: "Albacete" -> "albacete.csv"
    texto = unicodedata.normalize('NFD', provincia_display)
    texto = texto.encode('ascii', 'ignore').decode("utf-8")
    return f"{texto.lower().strip()}.csv"

# --- CARGA DE PROVINCIAS ---
@st.cache_data
def cargar_provincias():
    fichero = "codprov.csv"
    if os.path.exists(fichero):
        try:
            # Probamos con encoding utf-8-sig por si viene de Excel/Windows
            df = pd.read_csv(fichero, header=None, encoding='utf-8-sig')
            lista = df[0].dropna().astype(str).tolist()
            return [p.strip() for p in lista]
        except Exception:
            pass
    
    # Si falla la lectura, devolvemos una lista mínima de emergencia
    return ["Bizkaia", "Gipuzkoa", "Araba/Álava", "Madrid", "Barcelona"]

# --- INTERFAZ ---
st.title("⚖️ Calculadora de Plazos Legales")
st.sidebar.header("Configuración")

lista_provincias = cargar_provincias()

# Si la lista sigue siendo corta, mostramos un aviso
if len(lista_provincias) <= 5:
    st.sidebar.warning("Nota: No se pudo cargar 'codprov.csv'. Usando lista limitada.")

provincia_sel = st.sidebar.selectbox(
    "Selecciona Provincia/Ciudad", 
    options=lista_provincias,
    index=lista_provincias.index("Bizkaia") if "Bizkaia" in lista_provincias else 0
)

# Localización del archivo CSV de festivos
nombre_fichero = obtener_nombre_archivo(provincia_sel)
festivos = plazos.leer_festivos_csv(nombre_fichero)

if festivos:
    st.sidebar.success(f"Calendario cargado: {nombre_fichero}", icon="✅")
else:
    st.sidebar.error(f"No se encontró: {nombre_fichero}", icon="🚨")

# Configuración del modo de plazo
st.sidebar.divider()
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]
st.sidebar.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)

# --- ENTRADA DE DATOS ---
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Fecha de notificación/publicación", date.today())
    unidad = st.radio("Cómputo por", ["Días", "Meses"])
with col2:
    duracion = st.number_input("Plazo", min_value=1, value=10)
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

        st.success(f"### Vencimiento: {vencimiento.strftime('%d/%m/%Y')}")
        with st.expander("Ver detalle del cómputo"):
            for linea in logs: st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")

st.info(f"**Modo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
