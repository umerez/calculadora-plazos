#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plazo_cli.py — Interfaz de línea de comandos de la calculadora de plazos para los Atajos
(«Plazos a Expedientes», «Computar plazos»…) y para uso directo en la terminal.

Mantiene la interfaz del antiguo Scripts/plazos/plazos.py (misma salida «Vence: YYYY-MM-DD…»,
que es lo que los Atajos extraen con una expresión regular) y añade la SEDE del órgano:
una de las 431 cabeceras de partido judicial, escrita de cualquier manera («Bilbao», «Getxo»,
«Juzgado de Barakaldo», «Madrid», «vizcaya»). Por defecto, Bilbao.

Ejemplos:
  plazo_cli.py --inicio 2026-10-03 --duracion 10 --unidad dias --tipo habil --agosto-inhabil --navidad-inhabil --sede Bilbao
  plazo_cli.py --inicio 2026-07-15 --duracion 2 --unidad meses --tipo habil --agosto-interposicion --navidad-inhabil --sede Getxo
  plazo_cli.py --inicio 2026-10-03 --duracion 20 --unidad dias --tipo natural

Opciones de inhabilidad (como antes):
  --agosto-inhabil         agosto inhábil (plazos procesales, art. 128.1 LJCA / 183 LOPJ)
  --navidad-inhabil        24/12–06/01 inhábiles (art. 183 LOPJ)
  --agosto-interposicion   plazo por meses de interposición del contencioso: agosto no cuenta (art. 128.2 LJCA)
                           y, si la notificación es de agosto, el plazo corre desde el 1 de septiembre (STS 552/2022)
  --festivos RUTA          se acepta y se IGNORA (compatibilidad con los Atajos antiguos); los festivos salen de la sede
"""
import argparse
import calendar
import sys
from datetime import date, datetime, timedelta

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import festivos  # noqa: E402
import plazos    # noqa: E402

DIAS_SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def sumar_meses_naturales(inicio: date, meses: int) -> date:
    """Mismo número de día en el mes de vencimiento; si no existe, el último día del mes. Sin prórroga."""
    m = inicio.month - 1 + meses
    anio, mes = inicio.year + m // 12, m % 12 + 1
    return date(anio, mes, min(inicio.day, calendar.monthrange(anio, mes)[1]))


def main() -> None:
    p = argparse.ArgumentParser(description="Calculadora de plazos (sede = cabecera de partido judicial).")
    p.add_argument("--inicio", required=True, help="Fecha de inicio: YYYY-MM-DD (se admite hora, se ignora)")
    p.add_argument("--duracion", type=int, required=True)
    p.add_argument("--unidad", choices=["dias", "meses"], required=True)
    p.add_argument("--tipo", choices=["natural", "habil"], default="habil")
    p.add_argument("--sede", default="bilbao", help="Cabecera de partido judicial (defecto: Bilbao)")
    p.add_argument("--agosto-inhabil", action="store_true")
    p.add_argument("--navidad-inhabil", action="store_true")
    p.add_argument("--agosto-interposicion", action="store_true")
    p.add_argument("--festivos", default="", help="(ignorado; compatibilidad)")
    p.add_argument("--zona", default="Europe/Madrid", help="(ignorado; compatibilidad)")
    p.add_argument("--detalle", action="store_true")
    a = p.parse_args()

    try:
        inicio = datetime.fromisoformat(a.inicio.replace("T", " ").strip()).date()
    except ValueError:
        print(f"Error: formato de --inicio inválido: {a.inicio!r}", file=sys.stderr)
        sys.exit(1)

    lugar = festivos.buscar(a.sede)
    aviso_sede = ""
    if lugar is None:
        aviso_sede = f"Sede «{a.sede}» no reconocida; se usa Bilbao."
        lugar = festivos.lugar("bilbao")
    calendario = festivos.calendario(lugar["id"])
    fest = set(calendario)
    config = {"agosto_inhabil": a.agosto_inhabil, "navidad_inhabil": a.navidad_inhabil,
              "agosto_interposicion": a.agosto_interposicion}

    detalle = [f"Sede: {lugar['nombre']} ({lugar.get('provincia', '')}) — capas: {', '.join(lugar['capas'])}"]
    if aviso_sede:
        detalle.append("AVISO: " + aviso_sede)

    if a.unidad == "dias":
        if a.tipo == "natural":
            venc = inicio + timedelta(days=a.duracion)
            detalle.append(f"Suma de {a.duracion} días naturales desde {inicio.isoformat()} → {venc.isoformat()}")
        else:
            venc, log = plazos.sumar_dias_habiles(inicio, a.duracion, fest, config)
            detalle += log
    else:
        if a.tipo == "natural":
            venc = sumar_meses_naturales(inicio, a.duracion)
            detalle.append(f"Suma de {a.duracion} meses naturales desde {inicio.isoformat()} → {venc.isoformat()} (sin prórroga)")
        else:
            venc, log = plazos.sumar_meses(inicio, a.duracion, fest, config)
            detalle += log

    # Cobertura: capas sin festivos en los años del cómputo
    anios = festivos.anios_cubiertos(lugar["id"])
    avisos = []
    for anio in sorted({inicio.year, venc.year}):
        faltan = [c for c, ys in anios.items() if anio not in ys]
        if faltan:
            avisos.append(f"{anio}: faltan {', '.join(faltan)}")

    print("=== CÓMPUTO DE PLAZO ===")
    print(f"Inicio:                  {inicio.isoformat()}")
    print(f"Duración:                {a.duracion}")
    print(f"Unidad:                  {a.unidad}")
    print(f"Tipo:                    {a.tipo}")
    print(f"Sede:                    {lugar['nombre']} ({lugar.get('provincia', '')}) [{lugar['id']}]")
    print(f"Agosto inhábil:          {'Sí' if a.agosto_inhabil else 'No'}")
    print(f"Navidad inhábil:         {'Sí' if a.navidad_inhabil else 'No'}")
    print(f"Agosto interposición:    {'Sí' if a.agosto_interposicion else 'No'}")
    print(f"Festivos cargados:       {len(fest)}")
    print(f"Cobertura:               {'; '.join(avisos) if avisos else 'completa'}")
    if aviso_sede:
        print(f"Aviso:                   {aviso_sede}")
    print(f"Vence:                   {venc.isoformat()} ({DIAS_SEMANA[venc.weekday()]})")
    if a.detalle:
        print("\n--- DETALLE ---")
        for linea in detalle:
            print(linea)
        print("\n--- FESTIVOS APLICADOS (con fuente) ---")
        for d in sorted(calendario):
            if inicio <= d <= venc:
                nombre, capa, fuente = calendario[d]
                print(f"{d.isoformat()}  {nombre}  [{capa}]  {fuente}")


if __name__ == "__main__":
    main()
