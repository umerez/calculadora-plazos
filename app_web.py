import streamlit as st
from datetime import date
import plazos  # Importamos tu motor de cálculo

# Configuración de la página
st.set_page_config(page_title="Calculadora de Plazos", page_icon="⚖️")

st.title("⚖️ Calculadora de Plazos Legales")
st.markdown("""
Esta herramienta calcula vencimientos procesales y administrativos aplicando 
las reglas de **días hábiles**, **agosto inhábil** y **periodo navideño**.
""")

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("Configuración")

# 1. Selección de Modo (Basado en tu lógica de Swift)
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

# 2. Carga de Festivos
# Por defecto intenta leer 'festivos.csv', si no, puedes subir uno
archivo_festivos = st.sidebar.text_input("Nombre del archivo CSV de festivos", value="festivos.csv")
festivos = plazos.leer_festivos_csv(archivo_festivos)

if not festivos:
    st.sidebar.warning(f"No se detectaron festivos en '{archivo_festivos}'.")

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
    st.divider()
    
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                # Lógica simple para días naturales
                vencimiento = fecha_inicio + plazos.timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        # Mostrar Resultado
        st.success(f"### El vencimiento es el: {vencimiento.strftime('%d/%m/%Y')}")
        
        # Mostrar detalle paso a paso
        with st.expander("Ver detalle del cómputo (paso a paso)"):
            for linea in logs:
                st.write(f"- {linea}")

    except Exception as e:
        st.error(f"Ocurrió un error en el cálculo: {e}")

st.info(f"**Modo activo:** {config['nombre']}. Agosto inhábil: {'Sí' if config['agosto_inhabil'] else 'No'}.")
