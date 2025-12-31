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
        "agosto_interposicion": False  # No aplica la regla de "agosto no cuenta" para meses
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
        "agosto_interposicion": True  # Agosto se salta en meses y el inicio en agosto pasa a sept.
    }
}

# =============================================================================
#  UTILIDADES
# =============================================================================

def leer_festivos_csv(ruta_csv: str) -> Set[date]:
    festivos = set()
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            lineas = f.readlines()
            for linea in lineas:
                linea = linea.strip()
                if not linea or "Fecha" in linea: continue
                fecha_str = linea.split(',')[0].strip()
                try:
                    d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                    festivos.add(d)
                except ValueError: continue
    except FileNotFoundError: return set()
    return festivos

def es_periodo_navidad(fecha: date, activo: bool) -> bool:
    if not activo: return False
    if (fecha.month == 12 and fecha.day >= 24) or (fecha.month == 1 and fecha.day <= 6):
        return True
    return False

def es_dia_habil(fecha: date, festivos: Set[date], config: Dict) -> bool:
    if fecha.weekday() >= 5: return False # Sábado/Domingo
    if fecha in festivos: return False
    if config['agosto_inhabil'] and fecha.month == 8: return False
    if es_periodo_navidad(fecha, config['navidad_inhabil']): return False
    return True

def obtener_primer_habil_septiembre(anio: int, festivos: Set[date], config: Dict) -> date:
    fecha = date(anio, 9, 1)
    while not es_dia_habil(fecha, festivos, config):
        fecha += timedelta(days=1)
    return fecha

# =============================================================================
#  CÁLCULO POR DÍAS
# =============================================================================

def sumar_dias_habiles(inicio: date, duracion: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    if duracion <= 0: return inicio, ["Plazo 0."]
    
    fecha_cursor = inicio
    
    # REGLA DÍAS EN AGOSTO: Si agosto es inhábil, el cómputo por días empieza en septiembre
    if config['agosto_inhabil'] and inicio.month == 8:
        primer_habil_sept = obtener_primer_habil_septiembre(inicio.year, festivos, config)
        fecha_cursor = primer_habil_sept - timedelta(days=1)
        detalle.append(f"Notificación en agosto (inhábil): el cómputo por días comienza el {primer_habil_sept}.")

    contador = 0
    while contador < duracion:
        fecha_cursor += timedelta(days=1)
        if es_dia_habil(fecha_cursor, festivos, config):
            contador += 1
            detalle.append(f"Día {contador}: {fecha_cursor}")
        else:
            detalle.append(f"Omitido: {fecha_cursor} (Inhábil)")
            
    return fecha_cursor, detalle

# =============================================================================
#  CÁLCULO POR MESES
# =============================================================================

def sumar_meses(inicio: date, meses: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    
    # REGLA MESES: Solo salta al 1 de septiembre si es Interposición. 
    # En Plazo Procesal estándar, computa de fecha a fecha desde agosto.
    if config['agosto_interposicion'] and inicio.month == 8:
        f_inicio_calculo = obtener_primer_habil_septiembre(inicio.year, festivos, config)
        detalle.append(f"Interposición LJCA: inicio en agosto traslada el cómputo mensual al {f_inicio_calculo}.")
    else:
        f_inicio_calculo = inicio
        detalle.append(f"Cómputo mensual de fecha a fecha desde el {f_inicio_calculo}.")

    anio_cursor = f_inicio_calculo.year
    mes_cursor = f_inicio_calculo.month
    meses_contados = 0

    while meses_contados < meses:
        mes_cursor += 1
        if mes_cursor > 12:
            mes_cursor = 1
            anio_cursor += 1
        
        # En modo interposición, agosto no cuenta en la suma de meses
        if config['agosto_interposicion'] and mes_cursor == 8:
            detalle.append("Agosto omitido en el cómputo de meses (Art. 128.2 LJCA).")
            continue
        meses_contados += 1

    # Ajuste de fecha a fecha
    ultimo_dia_mes_destino = calendar.monthrange(anio_cursor, mes_cursor)[1]
    dia_final = min(f_inicio_calculo.day, ultimo_dia_mes_destino)
    vencimiento = date(anio_cursor, mes_cursor, dia_final)
    detalle.append(f"Vencimiento teórico: {vencimiento}")

    # Prórroga si el vencimiento es inhábil
    while not es_dia_habil(vencimiento, festivos, config):
        vencimiento += timedelta(days=1)
        detalle.append(f"Prorrogado por inhabilidad a: {vencimiento}")

    return vencimiento, detalle
