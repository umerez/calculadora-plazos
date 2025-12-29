#!/usr/bin/env python3
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
import argparse
import csv
import sys
from typing import List, Tuple, Set

BANNER = """\
plazos.py — Calculadora de plazos (hábiles/naturales) con reglas configurables
Autor: ChatGPT (navidad inhábil, plazos por meses y agosto-interposición)
Uso básico:
  python plazos.py --inicio "2025-11-02 13:00" --duracion 20 --unidad dias --tipo habil --zona Europe/Madrid --detalle

Opciones relevantes:
  --agosto-inhabil         Marca todo el mes de agosto como inhábil (además de fines de semana y festivos)
  --navidad-inhabil        Marca inhábiles del 24 de diciembre al 6 de enero (ambos inclusive) de cada año
  --agosto-interposicion   Para plazos por meses de interposición de recurso contencioso-administrativo:
                           agosto no cuenta en absoluto; se "salta" al contar meses.
"""

# ------------- Utilidades de parsing ------------- #

def parse_hhmm(s: str) -> time:
    """
    Parsea una cadena HH:MM a un objeto time.
    """
    try:
        h, m = s.split(":")
        h = int(h)
        m = int(m)
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
        return time(hour=h, minute=m)
    except Exception:
        raise argparse.ArgumentTypeError(f"Formato de hora inválido (esperado HH:MM): {s!r}")


def parse_horario_laboral(s: str) -> List[Tuple[time, time]]:
    """
    Parsea un horario del estilo "09:00-14:00,16:00-18:00"
    y devuelve una lista de tuplas (inicio, fin) como time().
    """
    tramos: List[Tuple[time, time]] = []
    if not s:
        return tramos

    for parte in s.split(","):
        parte = parte.strip()
        if not parte:
            continue
        try:
            ini_str, fin_str = parte.split("-")
            ini_t = parse_hhmm(ini_str.strip())
            fin_t = parse_hhmm(fin_str.strip())
            if ini_t >= fin_t:
                raise ValueError
            tramos.append((ini_t, fin_t))
        except Exception:
            raise argparse.ArgumentTypeError(
                f"Tramo horario inválido (esperado HH:MM-HH:MM,HH:MM-HH:MM...): {s!r}"
            )
    return tramos


def leer_festivos_csv(path: str) -> Set[date]:
    """
    Lee un CSV sencillo con fechas de festivos en formato YYYY-MM-DD,
    una por línea (puede haber cabecera).
    """
    festivos: Set[date] = set()
    if not path:
        return festivos

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            campo = row[0].strip()
            if not campo:
                continue
            try:
                d = date.fromisoformat(campo)
                festivos.add(d)
            except ValueError:
                # Probable cabecera o formato raro; la ignoramos
                continue
    return festivos

# ------------- Reglas de día hábil / inhábil ------------- #

def es_periodo_navidad(d: date, navidad_inhabil: bool) -> bool:
    """
    Devuelve True si la fecha cae entre el 24 de diciembre y el 6 de enero
    (ambos inclusive) y se ha activado la opción --navidad-inhabil.
    """
    if not navidad_inhabil:
        return False

    if d.month == 12 and d.day >= 24:
        return True
    if d.month == 1 and d.day <= 6:
        return True
    return False


def es_agosto_inhabil(d: date, agosto_inhabil: bool) -> bool:
    """
    Devuelve True si la fecha está en agosto y se ha activado --agosto-inhabil.
    """
    return agosto_inhabil and d.month == 8


def es_dia_habil(
    d: date,
    festivos: Set[date],
    agosto_inhabil: bool,
    navidad_inhabil: bool,
) -> bool:
    """
    Define si un día es hábil:
      - Lunes a viernes
      - No está en festivos
      - No está en agosto si --agosto-inhabil
      - No está en el periodo de navidad si --navidad-inhabil
    """
    # Fines de semana siempre inhábiles
    if d.weekday() >= 5:  # 5 = sábado, 6 = domingo
        return False

    # Festivos explícitos
    if d in festivos:
        return False

    # Agosto inhábil (opcional)
    if es_agosto_inhabil(d, agosto_inhabil):
        return False

    # Navidad inhábil (opcional)
    if es_periodo_navidad(d, navidad_inhabil):
        return False

    return True

# ------------- Utilidades de fechas para meses ------------- #

def ultimo_dia_mes(anio: int, mes: int) -> int:
    """
    Devuelve el último día (28-31) del mes dado.
    """
    if mes == 12:
        siguiente = date(anio + 1, 1, 1)
    else:
        siguiente = date(anio, mes + 1, 1)
    ultimo = siguiente - timedelta(days=1)
    return ultimo.day


def sumar_meses_fecha(base: date, meses: int) -> Tuple[date, bool]:
    """
    Suma 'meses' meses a una fecha base en el calendario normal.
    Intenta conservar el mismo número de día.
    Si en el mes resultante no existe ese día, usa el último día del mes.
    Devuelve la fecha resultante y un booleano que indica si se ha tenido que ajustar
    al último día del mes por inexistencia del día equivalente.
    """
    if meses == 0:
        return base, False

    total_meses = (base.year * 12 + (base.month - 1)) + meses
    nuevo_anio = total_meses // 12
    nuevo_mes = total_meses % 12 + 1

    dia_deseado = base.day
    ultimo_dia = ultimo_dia_mes(nuevo_anio, nuevo_mes)
    if dia_deseado > ultimo_dia:
        return date(nuevo_anio, nuevo_mes, ultimo_dia), True
    else:
        return date(nuevo_anio, nuevo_mes, dia_deseado), False


def sumar_meses_fecha_interposicion_agosto(
    base: date,
    meses: int,
) -> Tuple[date, bool]:
    """
    Suma 'meses' meses a una fecha base para el caso de interposición de recurso
    contencioso-administrativo cuando agosto no cuenta en absoluto (--agosto-interposicion).

    Regla: el mes de agosto se "salta" en la cuenta de meses.
    Es decir, al avanzar de mes en mes, los meses de agosto no consumen un mes de plazo.

    Ejemplos:
      - 20/06 + 2 meses → 20/07 (1º mes), 20/09 (2º mes) → 20/09
      - 24/07 + 2 meses → 24/09 (1º mes), 24/10 (2º mes) → 24/10
    """
    if meses == 0:
        return base, False

    current_year = base.year
    current_month = base.month
    meses_restantes = meses

    while meses_restantes > 0:
        # Avanzamos un mes de calendario
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

        # Si llegamos a agosto, ese mes no cuenta: no decrementamos meses_restantes
        if current_month == 8:
            continue

        # Mes "contado"
        meses_restantes -= 1

    dia_deseado = base.day
    ultimo_dia = ultimo_dia_mes(current_year, current_month)
    if dia_deseado > ultimo_dia:
        return date(current_year, current_month, ultimo_dia), True
    else:
        return date(current_year, current_month, dia_deseado), False

# ------------- Cómputo de plazos en días ------------- #

def sumar_dias_naturales(
    inicio: datetime,
    duracion: int,
) -> Tuple[datetime, List[str]]:
    """
    Suma 'duracion' días naturales a partir de 'inicio'.
    """
    detalle: List[str] = []
    vencimiento = inicio + timedelta(days=duracion)
    detalle.append(
        f"Suma de {duracion} días naturales desde {inicio.isoformat()} → {vencimiento.isoformat()}"
    )
    return vencimiento, detalle


def sumar_dias_habiles(
    inicio: datetime,
    duracion: int,
    festivos: Set[date],
    agosto_inhabil: bool,
    navidad_inhabil: bool,
) -> Tuple[datetime, List[str]]:
    """
    Suma 'duracion' días hábiles.
    Criterio adoptado:
      - El cómputo comienza al día siguiente de la fecha de inicio (criterio típico procesal).
      - Se van contando únicamente los días que resultan hábiles.
      - El vencimiento conserva la misma hora que 'inicio'.
    """
    detalle: List[str] = []

    if duracion <= 0:
        detalle.append("Duración 0 o negativa: el vencimiento coincide con la fecha de inicio.")
        return inicio, detalle

    contador = 0
    fecha_cursor = inicio.date()

    detalle.append(
        f"Inicio del cómputo (día siguiente a {fecha_cursor.isoformat()}) para {duracion} días hábiles."
    )

    while contador < duracion:
        fecha_cursor += timedelta(days=1)
        if es_dia_habil(fecha_cursor, festivos, agosto_inhabil, navidad_inhabil):
            contador += 1
            detalle.append(
                f"Día hábil {contador}: {fecha_cursor.isoformat()}"
            )
        else:
            motivo = []
            if fecha_cursor.weekday() >= 5:
                motivo.append("fin de semana")
            if fecha_cursor in festivos:
                motivo.append("festivo")
            if es_agosto_inhabil(fecha_cursor, agosto_inhabil):
                motivo.append("agosto inhábil")
            if es_periodo_navidad(fecha_cursor, navidad_inhabil):
                motivo.append("periodo de navidad inhábil (24/12–06/01)")
            if not motivo:
                motivo.append("regla personalizada")
            detalle.append(
                f"Día inhábil: {fecha_cursor.isoformat()} ({', '.join(motivo)})"
            )

    # Mantener la misma hora que el inicio
    vencimiento = datetime.combine(fecha_cursor, inicio.timetz())
    detalle.append(
        f"Vencimiento tras {duracion} días hábiles: {vencimiento.isoformat()}"
    )

    return vencimiento, detalle

# ------------- Cómputo de plazos en horas ------------- #

def sumar_horas_naturales(
    inicio: datetime,
    duracion_horas: int,
) -> Tuple[datetime, List[str]]:
    detalle: List[str] = []
    vencimiento = inicio + timedelta(hours=duracion_horas)
    detalle.append(
        f"Suma de {duracion_horas} horas naturales desde {inicio.isoformat()} → {vencimiento.isoformat()}"
    )
    return vencimiento, detalle


def siguiente_dia_habil(
    d: date,
    festivos: Set[date],
    agosto_inhabil: bool,
    navidad_inhabil: bool,
) -> date:
    """
    Devuelve el siguiente día hábil estrictamente posterior a d.
    """
    cursor = d
    while True:
        cursor += timedelta(days=1)
        if es_dia_habil(cursor, festivos, agosto_inhabil, navidad_inhabil):
            return cursor


def sumar_horas_habiles(
    inicio: datetime,
    duracion_horas: int,
    festivos: Set[date],
    agosto_inhabil: bool,
    navidad_inhabil: bool,
    tramos_laborales: List[Tuple[time, time]],
    tz: ZoneInfo,
) -> Tuple[datetime, List[str]]:
    """
    Suma horas hábiles limitadas a una jornada laboral (tramos_laborales)
    y a días hábiles según las reglas anteriores.
    """
    detalle: List[str] = []

    if duracion_horas <= 0:
        detalle.append("Duración 0 o negativa: el vencimiento coincide con la fecha de inicio.")
        return inicio, detalle

    if not tramos_laborales:
        raise ValueError("Para horas hábiles es necesario definir al menos un tramo horario laboral.")

    restante = duracion_horas
    actual = inicio

    detalle.append(
        f"Inicio del cómputo de {duracion_horas} horas hábiles desde {inicio.isoformat()}."
    )

    while restante > 0:
        fecha = actual.date()

        # Si el día no es hábil, saltamos al siguiente día hábil y al primer tramo horario
        if not es_dia_habil(fecha, festivos, agosto_inhabil, navidad_inhabil):
            detalle.append(
                f"Día inhábil completo: {fecha.isoformat()} (se salta al siguiente hábil)."
            )
            fecha = siguiente_dia_habil(fecha, festivos, agosto_inhabil, navidad_inhabil)
            primer_tramo = tramos_laborales[0]
            actual = datetime.combine(fecha, primer_tramo[0], tzinfo=tz)
            continue

        # Recorremos los tramos laborales de ese día
        avanzamos_en_este_dia = False
        for ini_t, fin_t in tramos_laborales:
            ini_dt = datetime.combine(fecha, ini_t, tzinfo=tz)
            fin_dt = datetime.combine(fecha, fin_t, tzinfo=tz)

            if actual >= fin_dt:
                # Ya hemos pasado este tramo
                continue

            # Hora de inicio efectiva dentro del tramo
            inicio_tramo_efectivo = max(actual, ini_dt)
            if inicio_tramo_efectivo >= fin_dt:
                continue

            capacidad_horas = (fin_dt - inicio_tramo_efectivo).total_seconds() / 3600.0

            if restante <= capacidad_horas + 1e-9:
                # Cabe dentro de este tramo
                avance = timedelta(hours=restante)
                nuevo_momento = inicio_tramo_efectivo + avance
                detalle.append(
                    f"Se consumen las últimas {restante} h hábiles el {fecha.isoformat()} "
                    f"entre {inicio_tramo_efectivo.timetz()} y {nuevo_momento.timetz()}."
                )
                actual = nuevo_momento
                restante = 0
                avanzamos_en_este_dia = True
                break
            else:
                # Consumimos todo el tramo
                detalle.append(
                    f"Se consumen {capacidad_horas:.2f} h hábiles el {fecha.isoformat()} "
                    f"entre {inicio_tramo_efectivo.timetz()} y {fin_dt.timetz()}."
                )
                restante -= capacidad_horas
                actual = fin_dt
                avanzamos_en_este_dia = True

        if restante > 0 and not avanzamos_en_este_dia:
            # No quedaban tramos útiles este día; saltamos al siguiente hábil
            siguiente = siguiente_dia_habil(fecha, festivos, agosto_inhabil, navidad_inhabil)
            primer_tramo = tramos_laborales[0]
            detalle.append(
                f"No quedan tramos laborales en {fecha.isoformat()}; "
                f"se salta al siguiente día hábil {siguiente.isoformat()} "
                f"a las {primer_tramo[0].isoformat(timespec='minutes')}."
            )
            actual = datetime.combine(siguiente, primer_tramo[0], tzinfo=tz)

    detalle.append(f"Vencimiento tras horas hábiles: {actual.isoformat()}")
    return actual, detalle

# ------------- Cómputo de plazos en meses ------------- #

def sumar_meses(
    inicio: datetime,
    duracion_meses: int,
    festivos: Set[date],
    agosto_inhabil: bool,
    navidad_inhabil: bool,
    tipo: str,                 # "natural" o "habil"
    agosto_interposicion: bool # True si se aplica la regla de que agosto no cuenta en absoluto
) -> Tuple[datetime, List[str]]:
    """
    Cómputo de plazos por meses con las reglas:
      1) El plazo concluye el mismo número de día de la fecha inicial.
      2) Si en el mes de vencimiento no hubiera día equivalente, expira el último día del mes.
      3) Si el último día del plazo es inhábil y el tipo es 'habil', se prorroga al primer día hábil siguiente.
      4) Si --agosto-interposicion está activo, al contar meses se "salta" completamente el mes de agosto
         (no consume meses de plazo).
    """
    detalle: List[str] = []

    if duracion_meses <= 0:
        detalle.append("Duración en meses 0 o negativa: el vencimiento coincide con la fecha de inicio.")
        return inicio, detalle

    fecha_inicial = inicio.date()
    detalle.append(
        f"Fecha inicial de cómputo por meses: {fecha_inicial.isoformat()} (duración: {duracion_meses} meses)."
    )

    if agosto_interposicion:
        detalle.append(
            "Aplicando regla de agosto-interposición: agosto no cuenta al computar los meses."
        )
        fecha_prov, ajustado_fin_mes = sumar_meses_fecha_interposicion_agosto(
            fecha_inicial,
            duracion_meses,
        )
    else:
        fecha_prov, ajustado_fin_mes = sumar_meses_fecha(fecha_inicial, duracion_meses)

    if ajustado_fin_mes:
        detalle.append(
            f"No existe el día {fecha_inicial.day} en el mes de vencimiento; "
            f"se ajusta al último día del mes: {fecha_prov.isoformat()}."
        )
    else:
        detalle.append(
            f"Se alcanza el mismo número de día en el mes de vencimiento: {fecha_prov.isoformat()}."
        )

    # Primer vencimiento "teórico" (antes de prórroga por inhabilidad)
    vencimiento_prov = datetime.combine(fecha_prov, inicio.timetz())
    detalle.append(
        f"Vencimiento teórico por meses: {vencimiento_prov.isoformat()}."
    )

    if tipo == "natural":
        # En plazos naturales por meses no se prorroga por inhabilidad
        detalle.append(
            "Tipo de plazo: natural. No se aplica prórroga aunque el último día sea inhábil."
        )
        return vencimiento_prov, detalle

    # tipo == "habil": aplicamos prórroga al primer día hábil siguiente si el día final es inhábil
    if es_dia_habil(fecha_prov, festivos, agosto_inhabil, navidad_inhabil):
        detalle.append(
            "El último día del plazo es hábil; no procede prórroga."
        )
        return vencimiento_prov, detalle
    else:
        motivo = []
        if fecha_prov.weekday() >= 5:
            motivo.append("fin de semana")
        if fecha_prov in festivos:
            motivo.append("festivo")
        if es_agosto_inhabil(fecha_prov, agosto_inhabil):
            motivo.append("agosto inhábil")
        if es_periodo_navidad(fecha_prov, navidad_inhabil):
            motivo.append("periodo de navidad inhábil (24/12–06/01)")
        if not motivo:
            motivo.append("regla personalizada")

        detalle.append(
            f"El último día del plazo es inhábil ({', '.join(motivo)}); "
            "se prorroga al primer día hábil siguiente."
        )

        fecha_prorrogada = siguiente_dia_habil(fecha_prov, festivos, agosto_inhabil, navidad_inhabil)
        vencimiento_def = datetime.combine(fecha_prorrogada, inicio.timetz())
        detalle.append(
            f"Vencimiento definitivo tras prórroga: {vencimiento_def.isoformat()}."
        )
        return vencimiento_def, detalle

# ------------- Argumentos CLI y flujo principal ------------- #

def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculadora de plazos hábiles/naturales con reglas configurables."
    )
    parser.add_argument(
        "--inicio",
        required=True,
        help="Fecha/hora inicial en formato ISO, p. ej. '2025-11-02 13:00' o '2025-11-02T13:00'.",
    )
    parser.add_argument(
        "--duracion",
        type=int,
        required=True,
        help="Duración del plazo (entero).",
    )
    parser.add_argument(
        "--unidad",
        choices=["dias", "horas", "meses"],
        required=True,
        help="Unidad de la duración: 'dias', 'horas' o 'meses'.",
    )
    parser.add_argument(
        "--tipo",
        choices=["natural", "habil"],
        required=True,
        help="Tipo de plazo: 'natural' o 'habil'.",
    )
    parser.add_argument(
        "--zona",
        default="Europe/Madrid",
        help="Zona horaria para el cómputo (por defecto Europe/Madrid).",
    )
    parser.add_argument(
        "--festivos-csv",
        default="",
        help="Ruta a CSV con festivos (formato YYYY-MM-DD, una fecha por línea).",
    )
    parser.add_argument(
        "--horario-laboral",
        type=parse_horario_laboral,
        default="09:00-14:00,16:00-18:00",
        help="Horario laboral para horas hábiles. Ejemplo: '09:00-14:00,16:00-18:00'.",
    )
    parser.add_argument(
        "--agosto-inhabil",
        action="store_true",
        help="Si se indica, todo agosto se considera inhábil.",
    )
    parser.add_argument(
        "--navidad-inhabil",
        action="store_true",
        help="Si se indica, son inhábiles los días entre el 24 de diciembre y el 6 de enero (ambos inclusive).",
    )
    parser.add_argument(
        "--agosto-interposicion",
        action="store_true",
        help=(
            "Para plazos por meses de interposición de recurso contencioso-administrativo: "
            "agosto no cuenta en absoluto; se salta al computar los meses."
        ),
    )
    parser.add_argument(
        "--detalle",
        action="store_true",
        help="Muestra el detalle del cómputo paso a paso.",
    )
    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    tz = ZoneInfo(args.zona)

    # Parseo de fecha/hora de inicio
    try:
        # Permitimos "YYYY-MM-DD HH:MM" o "YYYY-MM-DDTHH:MM"
        inicio_str = args.inicio.replace("T", " ")
        inicio_dt = datetime.fromisoformat(inicio_str)
    except ValueError:
        print(f"Error: formato de --inicio inválido: {args.inicio!r}", file=sys.stderr)
        sys.exit(1)

    if inicio_dt.tzinfo is None:
        inicio_dt = inicio_dt.replace(tzinfo=tz)
    else:
        inicio_dt = inicio_dt.astimezone(tz)

    festivos = leer_festivos_csv(args.festivos_csv)

    # Si el horario_laboral viene del default, sigue siendo str; lo normalizamos aquí:
    if isinstance(args.horario_laboral, str):
        args.horario_laboral = parse_horario_laboral(args.horario_laboral)

    # Cálculo principal
    if args.unidad == "dias":
        if args.tipo == "natural":
            vencimiento_dt, detalle = sumar_dias_naturales(
                inicio_dt,
                args.duracion,
            )
        else:  # habil
            vencimiento_dt, detalle = sumar_dias_habiles(
                inicio_dt,
                args.duracion,
                festivos,
                args.agosto_inhabil,
                args.navidad_inhabil,
            )

    elif args.unidad == "horas":
        if args.tipo == "natural":
            vencimiento_dt, detalle = sumar_horas_naturales(
                inicio_dt,
                args.duracion,
            )
        else:  # habil
            vencimiento_dt, detalle = sumar_horas_habiles(
                inicio_dt,
                args.duracion,
                festivos,
                args.agosto_inhabil,
                args.navidad_inhabil,
                args.horario_laboral,
                tz,
            )

    else:  # meses
        vencimiento_dt, detalle = sumar_meses(
            inicio_dt,
            args.duracion,
            festivos,
            args.agosto_inhabil,
            args.navidad_inhabil,
            args.tipo,
            args.agosto_interposicion,
        )

    # ------------- Salida ------------- #
    print("=== CÓMPUTO DE PLAZO ===")
    print(f"Inicio:                  {inicio_dt.astimezone(tz)}")
    print(f"Duración:                {args.duracion}")
    print(f"Unidad:                  {args.unidad}")
    print(f"Tipo:                    {args.tipo}")
    print(f"Zona:                    {args.zona}")
    print(f"Agosto inhábil:          {'Sí' if args.agosto_inhabil else 'No'}")
    print(f"Navidad inhábil:         {'Sí' if args.navidad_inhabil else 'No'}")
    print(f"Agosto interposición:    {'Sí' if args.agosto_interposicion else 'No'}")
    if args.unidad == "horas" and args.tipo == "habil":
        tramos_str = ",".join(
            f"{t1.strftime('%H:%M')}-{t2.strftime('%H:%M')}" for t1, t2 in args.horario_laboral
        )
        print(f"Jornada:                 {tramos_str}")
    print(f"Vence:                   {vencimiento_dt.astimezone(tz)}")

    if args.detalle:
        print("\n--- DETALLE ---")
        for line in detalle:
            print(line)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(BANNER)
        sys.exit(0)
    main()