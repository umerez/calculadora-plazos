#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_planos.py — Regenera, a partir del modelo por capas, los CSV planos que
siguen leyendo los clientes antiguos:

  * En la raíz del repo: bizkaia.csv, gipuzkoa.csv, araba_alava.csv
    (= nacional + Euskadi + territorio + local de la capital), que es lo que
    espera app_web.py en modo compatibilidad y el skill de Clara.
  * Con --swift DIR: los tres CSV de la app macOS y de los Atajos
    (festivos_bizkaia_gipuzkoa.csv, festivos_araba.csv, festivos_espana.csv),
    sin festivos locales, con columnas Fecha,Festividad.

Uso (desde la raíz del repo):
    python3 herramientas/generar_planos.py
    python3 herramientas/generar_planos.py --swift "/Users/umerez/SwiftUI umerez/CalculadoraDePlazos/CalculadoraDePlazos"
    python3 herramientas/generar_planos.py --swift /Users/umerez/Scripts/plazos
"""
import argparse
import csv
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import festivos  # noqa: E402

PLANOS_RAIZ = {          # fichero → lugar cuyo calendario completo se vuelca
    'bizkaia.csv': 'bilbao',
    'gipuzkoa.csv': 'donostia-san-sebastian',
    'araba_alava.csv': 'vitoria-gasteiz',
}
PLANOS_SWIFT = {         # fichero → capas (sin locales)
    'festivos_bizkaia_gipuzkoa.csv': ['nacional', 'ccaa/pv', 'territorial/bizkaia'],
    'festivos_araba.csv': ['nacional', 'ccaa/pv', 'territorial/araba'],
    'festivos_espana.csv': ['nacional'],
}


def escribir(ruta, filas, bom=True):
    with open(ruta, 'w', newline='', encoding='utf-8-sig' if bom else 'utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['Fecha', 'Festividad'])
        for d, nombre in sorted(filas):
            w.writerow([d.isoformat(), nombre])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--swift', metavar='DIR', help='carpeta donde escribir los 3 CSV de la app Swift / Atajos')
    args = ap.parse_args()

    for fichero, lugar_id in PLANOS_RAIZ.items():
        cal = festivos.calendario(lugar_id)
        escribir(os.path.join(RAIZ, fichero), [(d, v[0]) for d, v in cal.items()])
        print(f"{fichero:<22s} ← {lugar_id:<24s} {len(cal)} festivos")

    if args.swift:
        for fichero, capas in PLANOS_SWIFT.items():
            filas = {}
            for capa in capas:
                for d, nombre, _ in festivos._leer_capa(capa):
                    filas.setdefault(d, nombre)
            # El CSV de España de los Atajos se llama con ñ en Scripts/plazos
            destino = os.path.join(args.swift, fichero)
            if fichero == 'festivos_espana.csv' and os.path.exists(os.path.join(args.swift, 'festivos_españa.csv')):
                destino = os.path.join(args.swift, 'festivos_españa.csv')
            escribir(destino, list(filas.items()))
            print(f"{os.path.basename(destino):<30s} ← {'+'.join(capas):<45s} {len(filas)} festivos")


if __name__ == '__main__':
    main()
