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
        "agosto_interposicion": True  # Activa reglas especiales de agosto para meses
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
    # Periodo inhábil del 24 de diciembre al 6 de enero
    if (fecha.month == 12 and fecha.day >= 24) or (fecha.month == 1 and fecha.day <= 6):
        return True
    return False

def es_dia_habil(fecha: date, festivos: Set[date], config: Dict) -> bool:
    # 1. Fines de semana
    if fecha.weekday() >= 5:
        return False
    # 2. Festivos cargados desde CSV
    if fecha in festivos:
        return False
    # 3. Agosto (si el modo lo marca como inhábil)
    if config['agosto_inhabil'] and fecha.month == 8:
        return False
    # 4. Navidad (si el modo lo marca como inhábil)
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
#  CÁLCULO POR MESES (Regla especial LJCA para Agosto)
# =============================================================================

def sumar_meses(inicio: date, meses: int, festivos: Set[date], config: Dict) -> Tuple[date, List[str]]:
    detalle = []
    
    # NUEVA REGLA: Si la fecha de inicio es en agosto y es interposición, empieza el 1 de sept.
    if config['agosto_interposicion'] and inicio.month == 8:
        f_inicio_calculo = date(inicio.year, 9, 1)
        detalle.append(f"Inicio en agosto ({inicio}): por regla de interposición, el cómputo comienza el 1 de septiembre.")
    else:
        f_inicio_calculo = inicio

    anio_cursor = f_inicio_calculo.year
    mes_cursor = f_inicio_calculo.month
    meses_contados = 0

    # 1. Avanzar los meses uno a uno para detectar agosto
    while meses_contados < meses:
        mes_cursor += 1
        if mes_cursor > 12:
            mes_cursor = 1
            anio_cursor += 1
        
        # Si es interposición, agosto no cuenta en el cómputo de meses
        if config['agosto_interposicion'] and mes_cursor == 8:
            detalle.append("Regla Agosto-Interposición: Agosto se omite en el cómputo de meses.")
            continue
        
        meses_contados += 1

    # 2. Ajustar el día (regla de fecha a fecha)
    # Si el mes destino tiene menos días (ej. inicio día 31 y destino es junio), se usa el último día del mes.
    ultimo_dia_mes_destino = calendar.monthrange(anio_cursor, mes_cursor)[1]
    dia_final = min(f_inicio_calculo.day, ultimo_dia_mes_destino)
    vencimiento = date(anio_cursor, mes_cursor, dia_final)
    
    if dia_final != f_inicio_calculo.day:
        detalle.append(f"Día ajustado al último día del mes destino: {vencimiento}")
    else:
        detalle.append(f"Vencimiento teórico (fecha a fecha): {vencimiento}")

    # 3. Prórroga si el día final es inhábil (fin de semana, festivo, agosto o navidad)
    while not es_dia_habil(vencimiento, festivos, config):
        razon = "Fin de semana / Festivo / Periodo Inhábil"
        vencimiento += timedelta(days=1)
        detalle.append(f"Prorrogado por vencimiento en día inhábil ({razon}) a: {vencimiento}")

    return vencimiento, detalle

# =============================================================================
#  TEST LOCAL
# =============================================================================

if __name__ == "__main__":
    print("--- TEST REGLA AGOSTO (INTERPOSICIÓN) ---")
    # Simulación: Notificación el 15 de agosto, plazo 2 meses
    f_test = date(2024, 8, 15)
    festivos_test = set() # Vacío para el test
    config_test = MODOS_CALCULO["interposicion"]
    
    venc, logs = sumar_meses(f_test, 2, festivos_test, config_test)
    print(f"Inicio: {f_test} | Plazo: 2 meses")
    print(f"Vencimiento final: {venc}")
    for log in logs:
        print(f"  > {log}")
