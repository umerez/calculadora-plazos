import streamlit as st
from plazos import sumar_dias_habiles, leer_festivos_csv # Importas tu lógica
from datetime import datetime

st.title("Calculadora de Plazos Judiciales")

# Crear el formulario en la web
fecha_inicio = st.date_input("Fecha de inicio")
duracion = st.number_input("Días de plazo", value=20)
agosto = st.checkbox("Agosto inhábil")

if st.button("Calcular"):
    # Aquí llamas a las funciones que ya escribiste en plazos.py
    festivos = leer_festivos_csv("festivos_bizkaia_gipuzkoa.csv") 
    # ... resto de la lógica de llamada ...
    st.success(f"El vencimiento es el día...")