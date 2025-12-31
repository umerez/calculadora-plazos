import streamlit as st
from datetime import date, timedelta
import plazos  # Importa el motor de cálculo plazos.py

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="centered"
)

# Diccionario de nombres de días en español
DIAS_SEMANA = [
    "Lunes", "Martes", "Miércoles", "Jueves", 
    "Viernes", "Sábado", "Domingo"
]

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("⚖️ Calculadora de Plazos Legales Umerez")
st.markdown("""
Esta herramienta aplica las reglas de cómputo de la **LEC, LPAC y LJCA**.
Calcula vencimientos automáticos gestionando periodos inhábiles (Agosto, Navidad) y festivos locales.
""")

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("⚙️ Configuración")

# Mapeo de provincias a sus archivos CSV (asegúrate de que los archivos estén en la misma carpeta)
provincias = {
    "A Coruña": "a-coruna.csv",
    "Albacete": "albacete.csv",
    "Alicante": "alicante.csv",
    "Almería": "almeria.csv",
    "Araba/Álava": "araba_alava.csv",
    "Asturias": "asturias.csv",
    "Ávila": "avila.csv",
    "Badajoz": "badajoz.csv",
    "Bizkaia": "bizkaia_2026.csv",
    "Sevilla": "sevilla.csv",
    "Soria": "soria.csv",
    "Toledo": "toledo.csv",
    "Valladolid": "valladolid.csv",
    "Zamora": "zamora_2026.csv",
    "Zaragoza": "zaragoza.csv"
}

seleccion_provincia = st.sidebar.selectbox("Selecciona Provincia", list(provincias.keys()))
archivo_csv = provincias[seleccion_provincia]

# Carga de festivos desde el motor plazos.py
try:
    festivos = plazos.leer_festivos_csv(archivo_csv)
    st.sidebar.success(f"📅 Calendario de {seleccion_provincia} cargado.")
except Exception:
    festivos = set()
    st.sidebar.warning("⚠️ No se encontró el archivo de festivos. Se usarán solo fines de semana.")

# Selección del Tipo de Procedimiento
modo_key = st.sidebar.selectbox(
    "Tipo de Procedimiento",
    options=list(plazos.MODOS_CALCULO.keys()),
    format_func=lambda x: plazos.MODOS_CALCULO[x]["nombre"]
)
config = plazos.MODOS_CALCULO[modo_key]

# --- CUERPO PRINCIPAL (Entrada de Datos) ---
st.divider()

col1, col2 = st.columns(2)

with col1:
    fecha_inicio = st.date_input("Fecha de inicio (notificación)", date.today())
    unidad = st.radio("Cómputo por:", ["Días", "Meses"], horizontal=True)

with col2:
    duracion = st.number_input(f"Cantidad de {unidad}", min_value=1, value=10)
    if unidad == "Días":
        tipo_dia = st.selectbox("Tipo de días", ["Hábiles", "Naturales"])
    else:
        tipo_dia = "Meses"

st.divider()

# --- ACCIÓN DE CÁLCULO ---
if st.button("🚀 Calcular Vencimiento", use_container_width=True, type="primary"):
    try:
        if unidad == "Días":
            if tipo_dia == "Hábiles":
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos, config)
            else:
                # Días naturales
                vencimiento = fecha_inicio + timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
                # Prórroga si el natural cae en inhábil (Regla general administrativa/procesal)
                while not plazos.es_dia_habil(vencimiento, festivos, config):
                    vencimiento += timedelta(days=1)
                    logs.append(f"Prorrogado por vencimiento en día inhábil a: {vencimiento}")
        else:
            # Cómputo por meses
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos, config)

        # Mostrar resultado resaltado
        dia_semana_texto = DIAS_SEMANA[vencimiento.weekday()]
        st.balloons()
        
        st.markdown(f"""
        ### Resultado del Cómputo:
        La fecha de vencimiento es el:
        # {dia_semana_texto}, {vencimiento.strftime('%d/%m/%Y')}
        """)

        # Desglose de pasos
        with st.expander("🔍 Ver detalle del cálculo (paso a paso)"):
            for l in logs:
                st.write(f"- {l}")

    except Exception as e:
        st.error(f"Se ha producido un error en el cálculo: {e}")

# Pie de página
st.markdown("---")
st.caption(f"Configuración actual: {config['nombre']} | Provincia: {seleccion_provincia}")
