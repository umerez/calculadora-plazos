#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
informe_cobertura.py — Genera festivos/COBERTURA.md: para cada comunidad, qué cabeceras de partido
judicial tienen festivos locales cargados por año, cuáles faltan y cuáles son provisionales
(fuente no oficial: ayuntamiento o prensa). Ejecutar desde la raíz del repo tras migrar_a_capas.py.
"""
import os
import sys
from collections import defaultdict
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import festivos  # noqa: E402

ANIOS = (2025, 2026, 2027)


def main():
    lugares = festivos.lugares()
    por_ccaa = defaultdict(list)
    for l in lugares:
        por_ccaa[l['ccaa_nombre']].append(l)

    lineas = [f"# Cobertura de festivos por cabecera de partido judicial", "",
              f"Generado el {date.today().isoformat()} con `herramientas/informe_cobertura.py`. "
              f"{len(lugares)} cabeceras. Para cada año se indica cuántas cabeceras tienen festivos LOCALES cargados; "
              f"«provisional» = fuente no oficial (acuerdo municipal o prensa) pendiente de boletín.", ""]
    lineas += ["| Comunidad | Cabeceras | Local 2025 | Local 2026 | Local 2027 | CCAA 2027 |", "|---|---:|---:|---:|---:|---:|"]
    detalle = []
    for ccaa_nombre in sorted(por_ccaa):
        ls = por_ccaa[ccaa_nombre]
        cuenta = {a: 0 for a in ANIOS}
        faltan = {a: [] for a in ANIOS}
        provisionales = {a: [] for a in ANIOS}
        ccaa_2027 = 'sí'
        for l in ls:
            cal = festivos.calendario(l['id'])
            capa_local = next((c for c in l['capas'] if c.startswith('local/')), None)
            capa_ccaa = next((c for c in l['capas'] if c.startswith('ccaa/')), None)
            if capa_ccaa and 2027 not in {d.year for d, _, _ in festivos._leer_capa(capa_ccaa)}:
                ccaa_2027 = 'no'
            if not capa_local:
                for a in ANIOS:
                    faltan[a].append(l['nombre'] + ' (sin capa local)')
                continue
            filas = festivos._leer_capa(capa_local)
            for a in ANIOS:
                del_anio = [f for f in filas if f[0].year == a]
                if del_anio:
                    cuenta[a] += 1
                    if any('[prensa]' in f[2] or '[ayuntamiento]' in f[2] for f in del_anio):
                        provisionales[a].append(l['nombre'])
                else:
                    faltan[a].append(l['nombre'])
        lineas.append(f"| {ccaa_nombre} | {len(ls)} | {cuenta[2025]} | {cuenta[2026]} | {cuenta[2027]} | {ccaa_2027} |")
        detalle.append(f"## {ccaa_nombre} ({len(ls)} cabeceras)")
        for a in ANIOS:
            if faltan[a]:
                detalle.append(f"- **{a} sin festivos locales ({len(faltan[a])}):** " + ', '.join(sorted(faltan[a])))
            if provisionales[a]:
                detalle.append(f"- **{a} provisionales (fuente no oficial, {len(provisionales[a])}):** " + ', '.join(sorted(provisionales[a])))
        if not any(faltan[a] or provisionales[a] for a in ANIOS):
            detalle.append("- Completa y oficial en los tres años.")
        detalle.append("")
    lineas += ["", "Las fuentes de cada comunidad están en `festivos/fuentes/locales/INFORME_*.md`.", ""] + detalle
    ruta = os.path.join(RAIZ, 'festivos', 'COBERTURA.md')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas))
    print('\n'.join(lineas[:4 + len(por_ccaa)]))
    print(f"\n→ {ruta}")


if __name__ == '__main__':
    main()
