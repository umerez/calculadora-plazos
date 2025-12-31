import streamlit as st
import plazos
from datetime import date

# ... (Configuración inicial y carga de festivos igual que antes)

# Diccionario para nombres de días en español
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# --- BLOQUE DE RESULTADO ---
if st.button("🚀 Calcular Vencimiento", use_container_width=True, type="primary"):
    try:
        # (Lógica de llamada a plazos.py igual...)
        
        # Formateo del resultado con el día de la semana
        nombre_dia = DIAS_SEMANA[vencimiento.weekday()]
        fecha_formateada = vencimiento.strftime('%d/%m/%Y')
        
        st.success(f"## Vencimiento: {nombre_dia}, {fecha_formateada}")
        
        with st.expander("🔍 Ver detalle del cómputo paso a paso"):
            for linea in logs:
                st.write(f"- {linea}")
    except Exception as e:
        st.error(f"Error: {e}")
