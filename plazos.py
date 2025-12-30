#!/usr/bin/env python3
import csv
import calendar
import sys
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from typing import List, Tuple, Set, Dict

# =============================================================================
#  CONFIGURACIÓN DE TIPOS DE PLAZO (Traducción de la lógica Swift)
# =============================================================================

MODOS_CALCULO = {
    "contencioso": {
        "nombre": "Plazo Procesal",
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
        "nombre": "Interposición Recurso Contencioso",
        "agosto_inhabil": True,
        "navidad_inhabil": True,
        "agosto_interposicion": True  # Agosto no cuenta en el cómputo de meses
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
                if not linea or "Fecha" in linea: # Salta cabecera o vacíos
                    continue
                # Toma la parte antes de la primera coma
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
    # 24 de diciembre al 6 de enero
    if (fecha.month == 12 and fecha.day >= 24) or (fecha.month == 1 and fecha.day <= 6):
        return True
    return False

def es_dia_habil(fecha: date, festivos: Set[date], config: Dict) -> bool:
    # 1. Fines de semana (Sábado=5, Domingo=6 en Python)
    if fecha.weekday() >= 5:
        return False
    # 2. Festivos CSV
    if fecha in festivos:
        return False
    # 3. Agosto
    if config['agosto_inhabil'] and fecha.month == 8:
        return False
    # 4. Navidad (24/12 - 06/01)
    if es_periodo_navidad(fecha, config['navidad_inhabil']):
        return False
    return True

# =============================================================================
#  CÁLCULO POR DÍAS
# =============================================================================

def sumar_dias_habiles(inicio: date, duracion: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    if duracion <= 0:
        return inicio, ["Duración 0: el vencimiento es el mismo día."]
    
    fecha_cursor = inicio
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
#  CÁLCULO POR MESES (Regla especial Swift)
# =============================================================================

def sumar_meses(inicio: date, meses: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    fecha_cursor = inicio
    
    # 1. Aplicar salto de agosto si es interposición
    if config['agosto_interposicion']:
        meses_restantes = meses
        while meses_restantes > 0:
            # Avanzar un mes
            proximo_mes = fecha_cursor.month + 1
            proximo_anio = fecha_cursor.year
            if proximo_mes > 12:
                proximo_mes = 1
                proximo_anio += 1
            
            fecha_cursor = date(proximo_anio, proximo_mes, 1)
            if fecha_cursor.month != 8:
                meses_restantes -= 1
            else:
                detalle.append("Regla Agosto-Interposición: Agosto se salta en el cómputo.")
    else:
        # Suma de meses estándar
        m = inicio.month - 1 + meses
        anio = inicio.year + (m // 12)
        mes = (m % 12) + 1
        fecha_cursor = date(anio, mes, 1)

    # 2. Ajustar el día (si el mes destino tiene menos días que el de inicio)
    ultimo_dia_mes = calendar.monthrange(fecha_cursor.year, fecha_cursor.month)[1]
    dia_final = min(inicio.day, ultimo_dia_mes)
    vencimiento = date(fecha_cursor.year, fecha_cursor.month, dia_final)
    
    if dia_final != inicio.day:
        detalle.append(f"Ajustado al último día del mes: {vencimiento}")

    # 3. Prórroga si el último día es inhábil
    while not es_dia_habil(vencimiento, festivos, config):
        vencimiento += timedelta(days=1)
        detalle.append(f"Prorrogado por vencimiento en día inhábil a: {vencimiento}")

    return vencimiento, detalle

# =============================================================================
#  INTERFAZ DE LÍNEA DE COMANDOS (Para probar en local)
# =============================================================================

if __name__ == "__main__":
    # Ejemplo rápido de uso si ejecutas: python plazos.py
    print("--- TEST RÁPIDO ---")
    festivos_test = leer_festivos_csv("festivos.csv") # Asegúrate de tener este archivo
    config_test = MODOS_CALCULO["contencioso"]
    
    resultado, log = sumar_dias_habiles(date.today(), 10, festivos_test, config_test)
    print(f"Resultado 10 días hábiles desde hoy: {resultado}")
