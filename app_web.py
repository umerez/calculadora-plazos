import streamlit as st
from datetime import date
import plazos  # Importamos tu motor de cálculo plazos.py

# Configuración de la página
st.set_page_config(page_title="Calculadora de Plazos", page_icon="⚖️")

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("""
Esta herramienta calcula vencimientos procesales y administrativos aplicando 
las reglas de **días hábiles**, **agosto inhábil** y **periodo navideño**.
""")

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("Configuración de Calendario")

# 1. Selección del archivo de festivos (Tus 3 archivos específicos)
archivos_disponibles = {
    "Bizkaia y Gipuzkoa": "festivos_bizkaia_gipuzkoa.csv",
    "Araba": "festivos_araba.csv",
    "España (Nacionales)": "festivos_españa.csv"
}

seleccion_nombre = st.sidebar.selectbox(
    "Selecciona el Calendario de Festivos",
    options=list(archivos_disponibles.keys()),
    index=0  # Esto hace que "Bizkaia y Gipuzkoa" sea el predeterminado
)

archivo_seleccionado = archivos_disponibles[seleccion_nombre]

# Carga de festivos usando la función de tu plazos.py
festivos = plazos.leer_festivos_csv(archivo_seleccionado)

if festivos:
    st.sidebar.success(format_func=None, icon="✅", body=f"Calendario '{seleccion_nombre}' cargado.")
else:
    st.sidebar.error(f"Error: No se encuentra el archivo {archivo_seleccionado} en GitHub.")

# 2. Selección de Modo de Cálculo
st.sidebar.divider()
st.sidebar.header("Reglas de Cómputo")
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

# --- CUERPO PRINCIPAL (Entrada de datos) ---
col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input("Fecha de inicio (notificación/publicación)", date.today())
    unidad = st.radio("Unidad del plazo", ["Días", "Meses"])

with col2:
    duracion = st.number_input(f"Número de {unidad.lower()}", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])

# --- CÁLCULO ---
if st.button("Calcular Vencimiento"):
    if not festivos and tipo_dia == "Hábiles":
        st.warning("Atención: El cálculo se realizará sin festivos porque el archivo no se ha encontrado.")
    
    st.divider()
    
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                # Días naturales
                vencimiento = fecha_inicio + plazos.timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        # Mostrar Resultado llamativo
        st.success(f"### El vencimiento es el: {vencimiento.strftime('%d/%m/%Y')}")
        
        # Mostrar detalle paso a paso
        with st.expander("Ver detalle del cómputo (paso a paso)"):
            for linea in logs:
                st.write(f"- {linea}")

    except Exception as e:
        st.error(f"Ocurrió un error en el cálculo: {e}")

st.info(f"**Modo activo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
