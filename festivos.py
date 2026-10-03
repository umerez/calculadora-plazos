#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
festivos.py — Acceso al modelo de festivos por capas de la calculadora de plazos.

Un «lugar» (provincia, territorio histórico, municipio…) se define en
festivos/lugares.json con la lista de capas que componen su calendario:

    calendario(lugar) = nacional ∪ ccaa/<x> ∪ territorial/<y> ∪ local/<municipio>

Cada capa es un CSV `festivos/<capa>.csv` con columnas Fecha,Festividad,Fuente.
Las provincias no vascas usan, de momento, una única capa plana heredada
`provincia/<slug>` (festivos estatales + autonómicos + locales de la capital).

Uso típico:

    import festivos
    lugar = festivos.buscar('Bilbao')            # → dict del lugar
    fechas = festivos.fechas(lugar['id'])        # → set[date] para plazos.py
    detalle = festivos.calendario(lugar['id'])   # → {date: (nombre, capa, fuente)}

Solo biblioteca estándar.
"""
import csv
import json
import os
import re
import unicodedata
from datetime import date
from functools import lru_cache

RAIZ = os.path.dirname(os.path.abspath(__file__))
DIR_FESTIVOS = os.path.join(RAIZ, 'festivos')
INDICE = os.path.join(DIR_FESTIVOS, 'lugares.json')


def _normalizar(texto: str) -> str:
    t = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


@lru_cache(maxsize=1)
def _indice() -> dict:
    with open(INDICE, encoding='utf-8') as f:
        return json.load(f)


def lugares() -> list[dict]:
    """Todos los lugares seleccionables, tal como están en lugares.json."""
    return list(_indice()['lugares'])


def lugar(lugar_id: str) -> dict | None:
    return next((l for l in _indice()['lugares'] if l['id'] == lugar_id), None)


def buscar(texto: str) -> dict | None:
    """
    Resuelve un nombre escrito de cualquier manera («Bizkaia», «vizcaya», «Donostia»,
    «San Sebastián», «araba_alava», «Madrid»…) al lugar más plausible.
    Prioridad: id exacto → alias → nombre exacto → nombre que empieza igual → contiene.
    """
    if not texto:
        return None
    t = _normalizar(texto).replace(' ', '-')
    tn = _normalizar(texto)
    # Sinónimos habituales → id de cabecera. Una provincia o territorio se resuelve a su capital.
    alias = {
        'vizcaya': 'bilbao', 'bizkaia': 'bilbao', 'guipuzcoa': 'donostia-san-sebastian', 'gipuzkoa': 'donostia-san-sebastian',
        'alava': 'vitoria-gasteiz', 'araba': 'vitoria-gasteiz', 'araba-alava': 'vitoria-gasteiz', 'araba_alava': 'vitoria-gasteiz',
        'san-sebastian': 'donostia-san-sebastian', 'donostia': 'donostia-san-sebastian', 'vitoria': 'vitoria-gasteiz',
        'gasteiz': 'vitoria-gasteiz', 'gernika': 'gernika-lumo', 'guernica': 'gernika-lumo', 'arrasate': 'arrasate-mondragon',
        'mondragon': 'arrasate-mondragon', 'la-coruna': 'a-coruna', 'coruna': 'a-coruna', 'tenerife': 'santa-cruz-de-tenerife',
        'baleares': 'palma', 'illes-balears': 'palma', 'islas-baleares': 'palma', 'palma-de-mallorca': 'palma',
        'asturias': 'oviedo', 'cantabria': 'santander', 'navarra': 'pamplona', 'iruna': 'pamplona', 'pamplona-iruna': 'pamplona',
        'la-rioja': 'logrono', 'rioja': 'logrono', 'las-palmas': 'las-palmas-de-gran-canaria', 'castellon': 'castello-de-la-plana',
        'castellon-de-la-plana': 'castello-de-la-plana', 'alicante': 'alicante-alacant', 'alacant': 'alicante-alacant',
        'elche': 'elche-elx', 'alcoy': 'alcoy-alcoi', 'espana': 'madrid', 'nacional': 'madrid',
    }
    todos = _indice()['lugares']
    por_id = {l['id']: l for l in todos}
    if t in por_id:
        return por_id[t]
    if t in alias and alias[t] in por_id:
        return por_id[alias[t]]
    for l in todos:
        if _normalizar(l['nombre']) == tn:
            return l
    # Nombre de provincia → su capital
    for l in todos:
        if l.get('capital') and _normalizar(l.get('provincia', '')) == tn:
            return l
    for l in todos:
        if _normalizar(l['nombre']).startswith(tn):
            return l
    for l in todos:
        if tn in _normalizar(l['nombre']):
            return l
    for l in todos:
        if l.get('capital') and tn in _normalizar(l.get('provincia', '')):
            return l
    # «Juzgado de Getxo», «Tribunal de Instancia de Barakaldo», «Ayuntamiento de Leioa»: probar con los
    # sufijos del texto (sin la primera palabra, luego sin las dos primeras…), evitando bucles.
    palabras = tn.split()
    if len(palabras) > 1:
        for i in range(1, len(palabras)):
            resto = ' '.join(palabras[i:])
            if resto in ('de', 'del', 'la', 'las', 'los', 'el'):
                continue
            encontrado = buscar(resto)
            if encontrado:
                return encontrado
    return None


@lru_cache(maxsize=None)
def _leer_capa(capa: str) -> tuple:
    """Devuelve tuplas (date, nombre, fuente) de festivos/<capa>.csv. Capa inexistente → vacío."""
    ruta = os.path.join(DIR_FESTIVOS, *capa.split('/')) + '.csv'
    if not os.path.exists(ruta):
        return tuple()
    filas = []
    with open(ruta, newline='', encoding='utf-8-sig') as f:
        for r in csv.reader(f):
            if not r or not r[0].strip() or r[0].strip().lower() == 'fecha':
                continue
            try:
                d = date.fromisoformat(r[0].strip())
            except ValueError:
                continue
            filas.append((d, r[1].strip() if len(r) > 1 else '', r[2].strip() if len(r) > 2 else ''))
    return tuple(filas)


def calendario(lugar_id: str) -> dict[date, tuple[str, str, str]]:
    """{fecha: (festividad, capa, fuente)} para el lugar. Las capas se aplican en orden; la primera gana."""
    l = lugar(lugar_id)
    if l is None:
        raise KeyError(f"Lugar desconocido: {lugar_id!r}")
    resultado: dict[date, tuple[str, str, str]] = {}
    for capa in l['capas']:
        for d, nombre, fuente in _leer_capa(capa):
            resultado.setdefault(d, (nombre, capa, fuente))
    return resultado


def fechas(lugar_id: str) -> set[date]:
    """Conjunto de fechas festivas, listo para plazos.py."""
    return set(calendario(lugar_id))


def anios_cubiertos(lugar_id: str) -> dict[str, list[int]]:
    """Qué años tiene cada capa del lugar. Útil para avisar de cobertura incompleta."""
    l = lugar(lugar_id)
    if l is None:
        raise KeyError(f"Lugar desconocido: {lugar_id!r}")
    return {capa: sorted({d.year for d, _, _ in _leer_capa(capa)}) for capa in l['capas']}


def cobertura_completa(lugar_id: str, anio: int) -> bool:
    """True si TODAS las capas del lugar tienen al menos un festivo en ese año."""
    return all(anio in anios for anios in anios_cubiertos(lugar_id).values())


if __name__ == '__main__':
    import sys
    consulta = ' '.join(sys.argv[1:]) or 'Bilbao'
    l = buscar(consulta)
    if not l:
        print(f"No encuentro «{consulta}»")
        sys.exit(1)
    print(f"{l['nombre']}  [{l['id']}]  tipo={l['tipo']}  capas={l['capas']}")
    for d, (nombre, capa, fuente) in sorted(calendario(l['id']).items()):
        print(f"  {d}  {nombre:<45s} {capa:<28s} {fuente}")
    print("Años por capa:", anios_cubiertos(l['id']))
