import streamlit as st
from datetime import date, timedelta
import plazos

# Configuración de página
st.set_page_config(page_title="Calculadora Umerez", page_icon="⚖️", layout="wide")

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# --- BARRA LATERAL (Información y Autoría) ---
with st.sidebar:
    st.title("⚖️ Información")
    st.markdown("""
    Esta herramienta calcula vencimientos procesales y administrativos aplicando 
    las reglas de los artículos 30 de la Ley 39/2015, 133 de la LEC y 128 de la LJCA.
    
    **Autor:** Esteban Umerez  
    **Asistencia:** ChatGPT (OpenAI) y Gemini (Google).
    """)
    st.divider()
    st.link_button("Ir a umerez.eu", "https://umerez.eu", use_container_width=True)
    st.divider()
    st.warning("""
    **Aviso Legal (Disclaimer):** Esta herramienta es meramente informativa. El autor no se responsabiliza de 
    errores de cálculo ni de las decisiones legales basadas en estos resultados. 
    Contraste siempre con los calendarios oficiales.
    """)

# --- CUERPO PRINCIPAL (Selectores y Cálculo) ---
st.title("Calculadora de Plazos Legales")

# Diccionario de archivos (Corregido para coincidir con tus archivos)
archivos_disponibles = {
    "Bizkaia y Gipuzkoa": "festivos_bizkaia_gipuzkoa.csv",
    "Araba": "festivos_araba.csv",
    "España (Nacionales)": "festivos_españa.csv"
}

col_config1, col_config2 = st.columns(2)

with col_config1:
    seleccion_nombre = st.selectbox(
        "Provincia / Calendario", 
        options=list(archivos_disponibles.keys()),
        index=0 # Bizkaia por defecto
    )
    archivo_seleccionado = archivos_disponibles[seleccion_nombre]
    festivos = plazos.leer_festivos_csv(archivo_seleccionado)
    
    if not festivos:
        st.error(f"⚠️ No se encontró el archivo: {archivo_seleccionado}")
    else:
        st.caption(f"✅ Cargados festivos de {seleccion_nombre}")

with col_config2:
    modo_key = st.selectbox(
        "Tipo de Procedimiento",
        options=list(plazos.MODOS_CALCULO.keys()),
        format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
    )
    config = plazos.MODOS_CALCULO[modo_key]

st.divider()

col_data1, col_data2 = st.columns(2)

with col_data1:
    fecha_inicio = st.date_input("Fecha de notificación/publicación", date.today())
    unidad = st.radio("Unidad del plazo", ["Días", "Meses"], horizontal=True)

with col_data2:
    duracion = st.number_input("Cantidad", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])
    else:
        tipo_dia = "Meses"

if st.button("🚀 Calcular Vencimiento", type="primary", use_container_width=True):
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                vencimiento = fecha_inicio + timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
                while not plazos.es_dia_habil(vencimiento, festivos, config):
                    vencimiento += timedelta(days=1)
                    logs.append(f"Prorrogado por inhábil a: {vencimiento}")
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        nombre_dia = DIAS_SEMANA[vencimiento.weekday()]
        st.success(f"## Vencimiento: {nombre_dia}, {vencimiento.strftime('%d/%m/%Y')}")
        
        with st.expander("Ver detalle del cómputo"):
            for linea in logs:
                st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error: {e}")
