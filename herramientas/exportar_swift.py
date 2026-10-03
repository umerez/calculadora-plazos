#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exportar_swift.py — Empaqueta el modelo por capas en UN solo JSON para la app
Swift (macOS/iOS): `festivos_swift.json`, con el índice de lugares y las capas
que esos lugares usan. La app lo lee del bundle con Codable (FestivosStore.swift).

Uso (desde la raíz del repo):
    python3 herramientas/exportar_swift.py "/Users/umerez/SwiftUI umerez/CalculadoraDePlazos/CalculadoraDePlazos"
"""
import json
import os
import sys
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import festivos  # noqa: E402


def construir() -> dict:
    lugares = festivos.lugares()
    capas_usadas = sorted({c for l in lugares for c in l['capas']})
    capas = {}
    for c in capas_usadas:
        filas = festivos._leer_capa(c)
        capas[c] = [{'f': d.isoformat(), 'n': nombre} for d, nombre, _ in sorted(filas)]
    return {
        'version': date.today().isoformat(),
        'fuente_partidos': festivos._indice().get('fuente_partidos', ''),
        'lugares': [{
            'id': l['id'], 'nombre': l['nombre'], 'provincia': l.get('provincia', ''), 'ccaa': l.get('ccaa_nombre', ''),
            'capital': bool(l.get('capital')), 'partidoJudicial': bool(l.get('partido_judicial')),
            'localesPendientes': bool(l.get('locales_pendientes')), 'nota': l.get('nota', ''), 'capas': l['capas'],
        } for l in lugares],
        'capas': capas,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    destino = sys.argv[1]
    datos = construir()
    ruta = os.path.join(destino, 'festivos_swift.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))
    n_fechas = sum(len(v) for v in datos['capas'].values())
    print(f"{ruta}: {len(datos['lugares'])} lugares, {len(datos['capas'])} capas, {n_fechas} fechas, "
          f"{os.path.getsize(ruta) // 1024} KB")


if __name__ == '__main__':
    main()
