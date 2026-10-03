import streamlit as st
from datetime import date, timedelta
import plazos
import festivos

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Calculadora de Plazos Umerez",
    page_icon="⚖️",
    layout="wide"
)


# --- LUGARES (modelo por capas: festivos/lugares.json) ---
@st.cache_data(show_spinner=False)
def obtener_lugares():
    """Lista ordenada de (id, etiqueta): capitales primero, luego el resto de cabeceras de partido judicial."""
    opciones = []
    for l in festivos.lugares():
        etiqueta = l['nombre']
        if l.get('provincia') and l['provincia'].lower() != l['nombre'].lower():
            etiqueta += f" ({l['provincia']})"
        if l.get('capital'):
            etiqueta += " · capital"
        opciones.append((l['id'], etiqueta, bool(l.get('capital'))))
    opciones.sort(key=lambda o: (not o[2], o[1].lower()))
    return [(o[0], o[1]) for o in opciones]


# --- BARRA LATERAL (DESCRIPCIÓN Y DISCLAIMER) ---
with st.sidebar:
    st.header("Sobre esta Aplicación")
    st.markdown("""
    Esta herramienta es un **calendario de plazos procesales y administrativos** diseñado para facilitar el cómputo de vencimientos.

    Aplica de forma automatizada las reglas de:
    * Días hábiles e inhábiles.
    * Exclusión de festivos estatales, autonómicos y locales del lugar elegido.
    * Periodos de inhabilidad (Agosto y Navidad) según la normativa vigente (Ley 39/2015, LEC y LJCA).

    **Lugares:** las 431 cabeceras de partido judicial de España (incluidas las 52 capitales de provincia), según
    el Censo Judicial del Ministerio de Justicia. El calendario correcto para un plazo procesal es el de la localidad
    donde tiene su sede el órgano judicial (art. 182 LOPJ). Cada cabecera lleva sus festivos estatales, autonómicos
    (e insulares en Canarias) y locales, tomados de los boletines oficiales y portales de datos de cada comunidad; cuando
    falta algún año la aplicación lo avisa.

    **Créditos:** Creado por **Esteban Umerez**, con la asistencia de **ChatGPT** (OpenAI), **Gemini** (Google) y **Claude** (Anthropic).
    """)

    st.link_button("🌐 Visitar umerez.eu", "https://umerez.eu/2026/01/06/calculadora-de-plazos-procesales-y.html", use_container_width=True)

    st.divider()
    st.caption("⚠️ **Aviso Legal:**")
    st.caption("""
    Esta aplicación se ofrece "tal cual" (*as is*), con fines orientativos. El autor no garantiza la ausencia de errores y **no se responsabiliza** de los resultados obtenidos ni de las decisiones legales adoptadas basadas en este cálculo. Se recomienda contrastar los resultados con los calendarios oficiales. [Más info](https://umerez.eu/2026/01/06/calculadora-de-plazos-procesales-y.html)
    """)

# --- INTERFAZ PRINCIPAL ---
st.title("⚖️ Calculadora de Plazos Legales")

# 1. Fila de Configuración (Lugar y Tipo de Plazo)
lugares = obtener_lugares()
ids = [l[0] for l in lugares]
etiquetas = dict(lugares)

c1, c2 = st.columns(2)

with c1:
    lugar_id = st.selectbox(
        "Sede del órgano (cabecera de partido judicial o capital de provincia)",
        options=ids,
        format_func=lambda i: etiquetas[i],
        index=ids.index("bilbao") if "bilbao" in ids else 0,
        help="Escribe para buscar. Son las 431 cabeceras de partido judicial de España.",
    )
    lugar = festivos.lugar(lugar_id)
    calendario = festivos.calendario(lugar_id)
    festivos_set = set(calendario)
    anios = festivos.anios_cubiertos(lugar_id)
    anios_todos = sorted({a for v in anios.values() for a in v})
    if festivos_set:
        st.success(
            f"Calendario de **{lugar['nombre']}** cargado: {len(festivos_set)} festivos "
            f"({', '.join(c.split('/')[0] for c in lugar['capas'])}). Años: {anios_todos[0]}–{anios_todos[-1]}.",
            icon="✅",
        )
    else:
        st.error(f"No hay festivos cargados para {lugar['nombre']}", icon="🚨")
    if lugar.get('locales_pendientes'):
        st.warning(lugar.get('nota') or f"Festivos locales de {lugar['nombre']} pendientes de cargar.", icon="📍")

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
    unidad = st.radio("Unidad del plazo", ["Días", "Meses"], horizontal=True)

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
                vencimiento, logs = plazos.sumar_dias_habiles(fecha_inicio, duracion, festivos_set, config)
            else:
                vencimiento = fecha_inicio + timedelta(days=duracion)
                logs = [f"Cómputo por días naturales: {duracion} días."]
        else:
            vencimiento, logs = plazos.sumar_meses(fecha_inicio, duracion, festivos_set, config)

        nombre_dia = DIAS_SEMANA[vencimiento.weekday()]
        fecha_formateada = vencimiento.strftime('%d/%m/%Y')

        st.success(f"### Vencimiento: {fecha_formateada} ({nombre_dia})")

        # Aviso de cobertura: alguna capa del lugar no tiene festivos del año del vencimiento
        for anio in sorted({fecha_inicio.year, vencimiento.year}):
            capas_sin = [c for c, a in anios.items() if anio not in a]
            if capas_sin:
                st.warning(
                    f"Para {anio} faltan los festivos de: {', '.join(capas_sin)}. "
                    f"El resultado puede variar en uno o varios días cuando se publiquen.",
                    icon="⚠️",
                )

        with st.expander("🔍 Ver detalle del cómputo paso a paso"):
            for linea in logs:
                st.write(f"- {linea}")
        with st.expander("📅 Festivos aplicados en este lugar, con su fuente oficial"):
            st.caption("Cada festivo indica la capa de la que procede (estatal, autonómica, insular, territorial o local) "
                       "y el boletín oficial o conjunto de datos abiertos del que se ha tomado.")
            filas = []
            for d in sorted(calendario):
                if fecha_inicio.year <= d.year <= vencimiento.year:
                    nombre, capa, fuente = calendario[d]
                    filas.append({"Fecha": d.strftime('%d/%m/%Y'), "Festividad": nombre,
                                  "Ámbito": capa.split('/')[0], "Fuente": fuente or "—"})
            if filas:
                st.dataframe(filas, use_container_width=True, hide_index=True)
            else:
                st.write("No hay festivos cargados en el intervalo del cómputo.")
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
