#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Casos de referencia de la calculadora de plazos. Ejecutar desde la raíz del repo:
    python3 tests/test_plazos.py
Sale con código 1 si algún caso falla. Sin dependencias externas.
"""
import os
import sys
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import festivos   # noqa: E402
import plazos     # noqa: E402

CASOS = [
    # (descripción, lugar, modo, inicio, dias|None, meses|None, esperado)
    ("Personación 10 días contencioso Bilbao, cruza agosto (25/07 → 08/09)", 'bilbao', 'contencioso', date(2026, 7, 25), 10, None, date(2026, 9, 8)),
    ("Interposición 2 meses desde 15/07, agosto no cuenta", 'bilbao', 'interposicion', date(2026, 7, 15), None, 2, date(2026, 10, 15)),
    ("STS 552/2022: notificado en agosto, 2 meses desde 1/09 → 1/11 domingo → 2/11", 'bilbao', 'interposicion', date(2026, 8, 20), None, 2, date(2026, 11, 2)),
    ("Madrid: 10 días administrativos desde 28/10/2026, 2/11 es festivo trasladado", 'madrid', 'administrativo', date(2026, 10, 28), 10, None, date(2026, 11, 13)),
    ("Bilbao: 10 días contencioso desde 23/12/2026 cruza Navidad inhábil (hasta 6/01)", 'bilbao', 'contencioso', date(2026, 12, 23), 10, None, date(2027, 1, 20)),
    ("Bilbao 2027: 1 mes administrativo desde 7/09 vence 7/10, festivo autonómico nuevo → 8/10", 'bilbao', 'administrativo', date(2027, 9, 7), None, 1, date(2027, 10, 8)),
    ("Bilbao 2027: 5 días administrativos desde 23/08 saltan el 27/08 (Aste Nagusia)", 'bilbao', 'administrativo', date(2027, 8, 23), 5, None, date(2027, 8, 31)),
    ("Donostia 2027: 3 días administrativos desde 18/01 saltan el 20/01 (San Sebastián)", 'donostia-san-sebastian', 'administrativo', date(2027, 1, 18), 3, None, date(2027, 1, 22)),
    ("Getxo 2027 (partido judicial): 3 días administrativos desde 22/09 saltan el 24/09 (Las Mercedes)", 'getxo', 'administrativo', date(2027, 9, 22), 3, None, date(2027, 9, 28)),
    ("Vitoria 2026: 2 días administrativos desde 27/04 saltan San Prudencio 28/04", 'vitoria-gasteiz', 'administrativo', date(2026, 4, 27), 2, None, date(2026, 4, 30)),
]


def main():
    fallos = 0
    for desc, lugar_id, modo, inicio, dias, meses, esperado in CASOS:
        fest = festivos.fechas(lugar_id)
        cfg = plazos.MODOS_CALCULO[modo]
        if dias is not None:
            venc, _ = plazos.sumar_dias_habiles(inicio, dias, fest, cfg)
        else:
            venc, _ = plazos.sumar_meses(inicio, meses, fest, cfg)
        ok = venc == esperado
        fallos += 0 if ok else 1
        print(f"{'✅' if ok else '❌'} {desc}\n     → {venc}{'' if ok else f'  (esperado {esperado})'}")
    # Comprobaciones estructurales
    for lid in ['bilbao', 'donostia-san-sebastian', 'vitoria-gasteiz', 'madrid', 'espana']:
        assert festivos.lugar(lid), f"falta el lugar {lid}"
    # Cobertura: 2026 y 2027 completos en Euskadi; 2025-2026 en el resto. (Bilbao 2025 no tiene local
    # verificado: no hay fuente oficial a mano del viernes de Aste Nagusia 2025.)
    for lid, anios in [('bilbao', (2026, 2027)), ('donostia-san-sebastian', (2025, 2026, 2027)),
                       ('vitoria-gasteiz', (2025, 2026, 2027)), ('getxo', (2026, 2027)), ('madrid', (2025, 2026))]:
        for anio in anios:
            if not festivos.cobertura_completa(lid, anio):
                print(f"❌ cobertura incompleta {lid} {anio}: {festivos.anios_cubiertos(lid)}")
                fallos += 1
    assert festivos.buscar('vizcaya')['id'] == 'bizkaia'
    assert festivos.buscar('San Sebastián')['id'] == 'donostia-san-sebastian'
    assert festivos.buscar('Madrid')['id'] == 'madrid'
    print(f"\n{'TODO CORRECTO' if not fallos else f'{fallos} FALLO(S)'}")
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()
