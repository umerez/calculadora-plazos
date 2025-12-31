#!/usr/bin/env python3
import csv
import calendar
from datetime import datetime, date, timedelta
from typing import List, Tuple, Set, Dict

# =============================================================================
#  CONFIGURACIÓN DE TIPOS DE PLAZO
# =============================================================================

MODOS_CALCULO = {
    "contencioso": {
        "nombre": "Plazo Procesal (LEC-LJCA)",
        "agosto_inhabil": True,
        "navidad_inhabil": True,
        "agosto_interposicion": False
    },
    "administrativo": {
        "nombre": "Plazo Administrativo (LPAC)",
        "agosto_inhabil": False,
        "navidad_inhabil": False,
        "agosto_interposicion": False
    },
    "interposicion": {
        "nombre": "Interposición Recurso Contencioso (LJCA)",
        "agosto_inhabil": True,
        "navidad_inhabil": True,
        "agosto_interposicion": True  
    }
}

# =============================================================================
#  UTILIDADES Y CARGA DE DATOS
# =============================================================================

def leer_festivos_csv(ruta_csv: str) -> Set[date]:
    festivos = set()
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            lineas = f.readlines()
            for linea in lineas:
                linea = linea.strip()
                if not linea or "Fecha" in linea:
                    continue
                fecha_str = linea.split(',')[0].strip()
                try:
                    d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                    festivos.add(d)
                except ValueError:
                    continue
    except FileNotFoundError:
        return set()
    return festivos

# =============================================================================
#  LÓGICA DE COMPROBACIÓN DE DÍAS (Inhabilidades)
# =============================================================================

def es_periodo_navidad(fecha: date, activo: bool) -> bool:
    if not activo: return False
    if (fecha.month == 12 and fecha.day >= 24) or (fecha.month == 1 and fecha.day <= 6):
        return True
    return False

def es_dia_habil(fecha: date, festivos: Set[date], config: Dict) -> bool:
    if fecha.weekday() >= 5: # Sábado y Domingo
        return False
    if fecha in festivos:
        return False
    if config['agosto_inhabil'] and fecha.month == 8:
        return False
    if es_periodo_navidad(fecha, config['navidad_inhabil']):
        return False
    return True

def obtener_primer_habil_septiembre(anio: int, festivos: Set[date], config: Dict) -> date:
    """Busca el primer día hábil de septiembre de un año dado."""
    fecha = date(anio, 9, 1)
    while not es_dia_habil(fecha, festivos, config):
        fecha += timedelta(days=1)
    return fecha

# =============================================================================
#  CÁLCULO POR DÍAS
# =============================================================================

def sumar_dias_habiles(inicio: date, duracion: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    if duracion <= 0:
        return inicio, ["Duración 0: el vencimiento es el mismo día."]
    
    fecha_cursor = inicio
    
    # REGLA AGOSTO: Si el inicio es en agosto y el modo es procesal/interposición
    if config['agosto_inhabil'] and inicio.month == 8:
        primer_habil_sept = obtener_primer_habil_septiembre(inicio.year, festivos, config)
        # Ajustamos el cursor al día anterior al primer hábil para que el primer paso del bucle sea dicho día
        fecha_cursor = primer_habil_sept - timedelta(days=1)
        detalle.append(f"Notificación en agosto: el cómputo de días hábiles comienza el primer día hábil de septiembre ({primer_habil_sept}).")

    contador = 0
    while contador < duracion:
        fecha_cursor += timedelta(days=1)
        if es_dia_habil(fecha_cursor, festivos, config):
            contador += 1
            detalle.append(f"Día {contador}: {fecha_cursor} (Hábil)")
        else:
            detalle.append(f"Omitido: {fecha_cursor} (Inhábil/Festivo)")
            
    return fecha_cursor, detalle

# =============================================================================
#  CÁLCULO POR MESES
# =============================================================================

def sumar_meses(inicio: date, meses: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    
    # REGLA AGOSTO: Si el inicio es en agosto y el modo es procesal/interposición
    if config['agosto_inhabil'] and inicio.month == 8:
        f_inicio_calculo = obtener_primer_habil_septiembre(inicio.year, festivos, config)
        detalle.append(f"Inicio en agosto: el cómputo de meses comienza el primer día hábil de septiembre ({f_inicio_calculo}).")
    else:
        f_inicio_calculo = inicio

    anio_cursor = f_inicio_calculo.year
    mes_cursor = f_inicio_calculo.month
    meses_contados = 0

    # 1. Avanzar los meses uno a uno
    while meses_contados < meses:
        mes_cursor += 1
        if mes_cursor > 12:
            mes_cursor = 1
            anio_cursor += 1
        
        # En modo interposición, agosto no cuenta en el cómputo de meses
        if config['agosto_interposicion'] and mes_cursor == 8:
            detalle.append("Regla Agosto-Interposición: Agosto se omite en el cómputo de meses.")
            continue
        
        meses_contados += 1

    # 2. Ajustar el día (fecha a fecha)
    ultimo_dia_mes_destino = calendar.monthrange(anio_cursor, mes_cursor)[1]
    dia_final = min(f_inicio_calculo.day, ultimo_dia_mes_destino)
    vencimiento = date(anio_cursor, mes_cursor, dia_final)
    
    if dia_final != f_inicio_calculo.day:
        detalle.append(f"Día ajustado al último día del mes destino: {vencimiento}")
    else:
        detalle.append(f"Vencimiento teórico (fecha a fecha): {vencimiento}")

    # 3. Prórroga si el día final es inhábil
    while not es_dia_habil(vencimiento, festivos, config):
        vencimiento += timedelta(days=1)
        detalle.append(f"Prorrogado por vencimiento en día inhábil a: {vencimiento}")

    return vencimiento, detalle

# =============================================================================
#  INTERFAZ CLI (TEST)
# =============================================================================

if __name__ == "__main__":
    print("--- TEST INICIO EN AGOSTO ---")
    f_notificacion = date(2025, 8, 10) # 10 de agosto (domingo)
    # Imaginemos que el 1 de sept es lunes (hábil)
    festivos_vacio = set() 
    
    print("\nModo Procesal (10 días hábiles):")
    v, log = sumar_dias_habiles(f_notificacion, 10, festivos_vacio, MODOS_CALCULO["contencioso"])
    for l in log[:2]: print(f"  {l}")
    print(f"  Vencimiento: {v}")

    print("\nModo Interposición (2 meses):")
    v2, log2 = sumar_meses(f_notificacion, 2, festivos_vacio, MODOS_CALCULO["interposicion"])
    for l in log2[:2]: print(f"  {l}")
    print(f"  Vencimiento: {v2}")
