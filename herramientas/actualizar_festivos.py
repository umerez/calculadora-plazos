#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_festivos.py
======================
Script maestro para actualizar los calendarios de festivos de la
calculadora de plazos (un CSV por provincia, formato Fecha,Festividad).

Solo usa la biblioteca estándar de Python (sin requests, bs4 ni pandas),
así que funciona con cualquier python3 del Mac.

USO HABITUAL (añadir el año siguiente a los CSV):
    python3 actualizar_festivos.py --anio 2027

SOLO COMPROBAR si la web ya publica el calendario OFICIAL del año:
    python3 actualizar_festivos.py --anio 2027 --comprobar

CORREGIR festivos trasladados al lunes que quedaron guardados con la
fecha del domingo (defecto de los CSV generados antes de octubre 2026):
    python3 actualizar_festivos.py --corregir-traslados

CON PUSH A GITHUB (requiere Personal Access Token o `gh auth`):
    python3 actualizar_festivos.py --anio 2027 --push --token ghp_xxxx

OPCIONES:
    --anio                Año a descargar
    --destino             Carpeta con los CSV de la calculadora
                          (por defecto: ../calculadora-plazos-main)
    --comprobar           Solo verifica si hay calendario oficial publicado
    --corregir-traslados  Repara los traslados a lunes en los CSV existentes
    --forzar-no-oficial   Acepta páginas marcadas «No Oficial» (NO recomendado)
    --si                  No preguntar (ejecuciones no interactivas)
    --push / --token      git add + commit + push al terminar
    --detalle             Muestra los festivos descargados por provincia

FUENTE: https://calendarioslaborales.com/calendario-laboral-<slug>-<año>.htm
  * Desde octubre de 2026 la web lista cada festivo en un <li> con el
    formato «01 de enero – Año nuevo» (antes era «1 de Enero.Año nuevo»).
  * Las páginas de años todavía no publicados oficialmente llevan el rótulo
    «Calendario No Oficial. Festivos estimados de años anteriores» y su
    contenido es una estimación errónea: este script las rechaza.
  * Cuando un festivo cae en domingo y la comunidad lo traslada, la web lo
    anota «(se traslada al lunes)». Hoy muestra ya la fecha del lunes; las
    versiones antiguas mostraban la del domingo. El script normaliza siempre
    al lunes.
"""

import argparse
import csv
import html
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta

# =============================================================================
#  CONFIGURACIÓN
# =============================================================================

# Provincias → slug en la URL de calendarioslaborales.com.
# Las capitales de provincia se excluyen: la calculadora usa un CSV por
# provincia (aunque la web, para algunas provincias, incluye los festivos
# locales de la capital; ver auditoría 2026-10-03).
PROVINCIAS = {
    'Álava / Araba': 'alava',
    'Albacete': 'albacete',
    'Alicante': 'alicante',
    'Almería': 'almeria',
    'Asturias': 'asturias',
    'Ávila': 'avila',
    'Badajoz': 'badajoz',
    'Baleares': 'baleares',
    'Barcelona': 'barcelona',
    'Burgos': 'burgos',
    'Cáceres': 'caceres',
    'Cádiz': 'cadiz',
    'Cantabria': 'cantabria',
    'Castellón': 'castellon',
    'Ceuta': 'ceuta',
    'Ciudad Real': 'ciudad-real',
    'Córdoba': 'cordoba',
    'A Coruña': 'la-coruna',
    'Cuenca': 'cuenca',
    'Girona': 'girona',
    'Granada': 'granada',
    'Guadalajara': 'guadalajara',
    'Gipuzkoa': 'guipuzcoa',
    'Huelva': 'huelva',
    'Huesca': 'huesca',
    'Jaén': 'jaen',
    'La Rioja': 'la-rioja',
    'Las Palmas': 'las-palmas',
    'León': 'leon',
    'Lleida': 'lleida',
    'Lugo': 'lugo',
    'Madrid': 'madrid',
    'Málaga': 'malaga',
    'Melilla': 'melilla',
    'Murcia': 'murcia',
    'Navarra': 'navarra',
    'Ourense': 'ourense',
    'Palencia': 'palencia',
    'Pontevedra': 'pontevedra',
    'Salamanca': 'salamanca',
    'Segovia': 'segovia',
    'Sevilla': 'sevilla',
    'Soria': 'soria',
    'Tarragona': 'tarragona',
    'Tenerife': 'tenerife',
    'Teruel': 'teruel',
    'Toledo': 'toledo',
    'Valencia': 'valencia',
    'Valladolid': 'valladolid',
    'Bizkaia': 'vizcaya',
    'Zamora': 'zamora',
    'Zaragoza': 'zaragoza',
}

# slug de la URL → nombre de archivo definitivo en la calculadora
SLUG_A_ARCHIVO = {
    'alava': 'araba_alava',
    'vizcaya': 'bizkaia',
    'guipuzcoa': 'gipuzkoa',
    'la-coruna': 'a-coruna',
}

# Provincias cuyos festivos NO se scrapean: se mantienen desde fuentes oficiales en festivos/
EUSKADI_OFICIAL = {'bizkaia', 'gipuzkoa', 'araba_alava'}

BASE_URL = "https://calendarioslaborales.com/calendario-laboral-{slug}-{anio}.htm"

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

MESES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'setiembre': 9, 'octubre': 10,
    'noviembre': 11, 'diciembre': 12,
}

# Un calendario laboral español tiene entre 8 y 14 festivos (la web no
# siempre incluye los dos locales). Menos de MIN_FESTIVOS → sospechoso.
MIN_FESTIVOS = 8

RE_UL_FESTIVOS = re.compile(r'<ul[^>]*class="[^"]*month-holidays[^"]*"[^>]*>(.*?)</ul>', re.S | re.I)
RE_LI = re.compile(r'<li[^>]*>(.*?)</li>', re.S | re.I)
RE_FESTIVO = re.compile(
    r'^(\d{1,2})\s+de\s+([a-záéíóú]+)\s*[–—-]\s*(.+)$', re.I)
RE_TRASLADO = re.compile(r'\(?\s*se\s+traslada\s+al\s+lunes\s*\)?', re.I)
MARCAS_NO_OFICIAL = ('no oficial', 'estimados de años anteriores',
                     'festivos estimados')


# =============================================================================
#  DESCARGA Y PARSEO
# =============================================================================

def descargar(url: str, timeout: int = 30) -> tuple[int, str]:
    """Descarga una URL siguiendo redirecciones. Devuelve (status, html)."""
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''


def texto_plano(fragmento_html: str) -> str:
    """Quita etiquetas, decodifica entidades y colapsa espacios."""
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', fragmento_html, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def es_oficial(pagina_html: str) -> bool:
    """True si la página NO lleva el rótulo de calendario estimado/no oficial."""
    t = texto_plano(pagina_html).lower()
    return not any(m in t for m in MARCAS_NO_OFICIAL)


def normalizar_traslado(fecha: date, nombre: str) -> tuple[date, str]:
    """
    Si el festivo lleva la anotación «se traslada al lunes» y la fecha es
    sábado o domingo, la mueve al lunes siguiente. Si ya es lunes, la deja.
    Devuelve la fecha corregida y el nombre con la anotación normalizada.
    """
    if not RE_TRASLADO.search(nombre):
        return fecha, nombre
    base = RE_TRASLADO.sub('', nombre).strip(' .,;')
    if fecha.weekday() == 6:      # domingo
        fecha = fecha + timedelta(days=1)
    elif fecha.weekday() == 5:    # sábado
        fecha = fecha + timedelta(days=2)
    return fecha, f"{base} (se traslada al lunes)"


def parsear_festivos(pagina_html: str, anio: int) -> list[dict]:
    """
    Extrae los festivos de la página. Devuelve lista de
    {'Fecha': 'YYYY-MM-DD', 'Festividad': str} ordenada y sin duplicados.
    """
    # Solo las listas de festivos (<ul class="month-holidays">); así los <li>
    # anidados del menú de navegación no desplazan el emparejado <li>…</li>.
    bloques = RE_UL_FESTIVOS.findall(pagina_html) or [pagina_html]
    vistos = {}
    for li in (li for bloque in bloques for li in RE_LI.findall(bloque)):
        t = texto_plano(li)
        m = RE_FESTIVO.match(t)
        if not m:
            continue
        dia, mes_txt, nombre = int(m.group(1)), m.group(2).lower(), m.group(3).strip()
        mes = MESES.get(mes_txt)
        if not mes:
            continue
        try:
            fecha = date(anio, mes, dia)
        except ValueError:
            continue
        fecha, nombre = normalizar_traslado(fecha, nombre)
        clave = fecha.isoformat()
        if clave not in vistos:
            vistos[clave] = {'Fecha': clave, 'Festividad': nombre}
    return [vistos[k] for k in sorted(vistos)]


def scrapear_provincia(slug: str, anio: int, forzar_no_oficial: bool = False) -> tuple[list[dict], str]:
    """
    Devuelve (festivos, estado). estado ∈ {'ok', 'no-oficial', 'http-<code>',
    'sin-datos', 'error: ...'}. Si la página no es oficial y no se fuerza,
    devuelve lista vacía con estado 'no-oficial'.
    """
    url = BASE_URL.format(slug=slug, anio=anio)
    try:
        status, cuerpo = descargar(url)
    except Exception as e:  # red, timeout…
        return [], f"error: {str(e)[:60]}"
    if status != 200 or not cuerpo:
        return [], f"http-{status}"
    if not es_oficial(cuerpo) and not forzar_no_oficial:
        return [], 'no-oficial'
    festivos = parsear_festivos(cuerpo, anio)
    if not festivos:
        return [], 'sin-datos'
    return festivos, 'ok'


def comprobar_disponibilidad(anio: int) -> bool:
    """
    Comprueba 3 provincias de referencia. Disponible = al menos 2 de 3 tienen
    página OFICIAL con un número razonable de festivos.
    """
    prueba = ['madrid', 'vizcaya', 'sevilla']
    ok = 0
    print(f"\n🔍 Comprobando disponibilidad del calendario OFICIAL {anio}...")
    for slug in prueba:
        festivos, estado = scrapear_provincia(slug, anio)
        url = BASE_URL.format(slug=slug, anio=anio)
        if estado == 'ok' and len(festivos) >= MIN_FESTIVOS:
            print(f"   {slug:12s} → ✅ {len(festivos)} festivos oficiales")
            ok += 1
        elif estado == 'no-oficial':
            print(f"   {slug:12s} → ⚠️  página publicada pero marcada «No Oficial / estimados»")
        else:
            print(f"   {slug:12s} → ❌ {estado}")
        print(f"   {'':12s}   {url}")
        time.sleep(0.5)
    disponible = ok >= 2
    print(f"\n{'✅ Calendario oficial disponible' if disponible else '❌ Calendario oficial aún no publicado'} "
          f"para {anio} ({ok}/3 provincias de prueba).")
    return disponible


# =============================================================================
#  CSV
# =============================================================================

def slug_a_nombre_archivo(slug: str) -> str:
    return SLUG_A_ARCHIVO.get(slug, slug)


def leer_csv(ruta: str) -> list[dict]:
    """Lee un CSV Fecha,Festividad. Tolera BOM y filas vacías."""
    if not os.path.exists(ruta):
        return []
    filas = []
    with open(ruta, newline='', encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            fecha = row[0].strip()
            if fecha.lower() == 'fecha':
                continue
            nombre = row[1].strip() if len(row) > 1 else ''
            filas.append({'Fecha': fecha, 'Festividad': nombre})
    return filas


def escribir_csv(ruta: str, filas: list[dict]) -> None:
    """Escribe el CSV ordenado por fecha y sin fechas duplicadas (utf-8-sig)."""
    unicos = {}
    for r in filas:
        unicos.setdefault(r['Fecha'], r)
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    with open(ruta, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')  # LF, como los CSV originales del repo
        w.writerow(['Fecha', 'Festividad'])
        for k in sorted(unicos):
            w.writerow([unicos[k]['Fecha'], unicos[k]['Festividad']])


def anios_en(filas: list[dict]) -> set[str]:
    return {r['Fecha'][:4] for r in filas if len(r['Fecha']) >= 4}


def corregir_traslados(destino: str) -> int:
    """
    Repara los CSV existentes: festivos anotados «se traslada al lunes» que
    quedaron guardados con la fecha del sábado/domingo pasan al lunes.
    Devuelve el número de filas corregidas.
    """
    print(f"\n🔧 Corrigiendo traslados a lunes en {destino} ...")
    total = 0
    for nombre in sorted(os.listdir(destino)):
        if not nombre.endswith('.csv') or nombre == 'codprov.csv':
            continue
        ruta = os.path.join(destino, nombre)
        filas = leer_csv(ruta)
        cambios = []
        nuevas = []
        for r in filas:
            try:
                fecha = date.fromisoformat(r['Fecha'])
            except ValueError:
                nuevas.append(r)
                continue
            nueva_fecha, nuevo_nombre = normalizar_traslado(fecha, r['Festividad'])
            if nueva_fecha != fecha:
                cambios.append(f"{r['Fecha']} → {nueva_fecha.isoformat()}  {nuevo_nombre}")
            nuevas.append({'Fecha': nueva_fecha.isoformat(), 'Festividad': nuevo_nombre})
        if cambios:
            escribir_csv(ruta, nuevas)
            escribir_capa_provincia(destino, nombre[:-4], nuevas)
            total += len(cambios)
            print(f"   {nombre:<20s} {len(cambios)} corregido(s)")
            for c in cambios:
                print(f"      {c}")
    print(f"\n   Total filas corregidas: {total}")
    return total


def destino_por_defecto() -> str:
    """Si el script vive en <repo>/herramientas/, el destino es <repo>; si no, ../calculadora-plazos-main."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    padre = os.path.dirname(aqui)
    if os.path.isdir(os.path.join(padre, 'festivos')):
        return padre
    return os.path.join(aqui, '..', 'calculadora-plazos-main')


def escribir_capa_provincia(destino: str, archivo: str, filas: list[dict]) -> None:
    """Mantiene sincronizada la capa festivos/provincia/<archivo>.csv (modelo por capas) con el CSV plano."""
    carpeta = os.path.join(destino, 'festivos', 'provincia')
    if not os.path.isdir(carpeta):
        return
    ruta = os.path.join(carpeta, f'{archivo}.csv')
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['Fecha', 'Festividad', 'Fuente'])
        for r in sorted(filas, key=lambda r: r['Fecha']):
            w.writerow([r['Fecha'], r['Festividad'], 'calendarioslaborales.com (calendario provincial con locales de la capital)'])


# =============================================================================
#  GIT
# =============================================================================

def hacer_push_github(destino: str, mensaje: str, token: str) -> bool:
    def run(cmd):
        return subprocess.run(cmd, cwd=destino, capture_output=True, text=True)

    print("\n📤 Subiendo cambios a GitHub...")
    r = run(['git', 'remote', 'get-url', 'origin'])
    if r.returncode != 0:
        print("   ❌ No se encontró remoto 'origin'. ¿Es un repositorio git?")
        return False
    remote_url = r.stdout.strip()

    run(['git', 'add', '*.csv'])
    r = run(['git', 'commit', '-m', mensaje])
    if 'nothing to commit' in (r.stdout + r.stderr):
        print("   ℹ️  No hay cambios nuevos que commitear.")
        return True

    # El token va solo en el comando push; nunca se persiste en .git/config.
    push_target = 'origin'
    if token and remote_url.startswith('https://'):
        push_target = remote_url.replace('https://', f'https://{token}@')
    r = run(['git', 'push', push_target, 'main'])
    if r.returncode == 0:
        print(f"   ✅ Push completado: «{mensaje}»")
        return True
    print(f"   ❌ Error en push: {r.stderr[:200]}")
    print("   💡 Alternativa: `gh auth login` y volver a lanzar, o subir los CSV desde github.com.")
    return False


# =============================================================================
#  MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Actualiza los calendarios de festivos de la calculadora de plazos.',
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    parser.add_argument('--anio', type=int, help='Año a descargar (ej: 2027)')
    parser.add_argument('--destino', type=str, default=destino_por_defecto(),
                        help='Raíz del repo de la calculadora (con festivos/ y los CSV planos)')
    parser.add_argument('--comprobar', action='store_true',
                        help='Solo verifica si hay calendario oficial publicado')
    parser.add_argument('--corregir-traslados', action='store_true',
                        help='Repara traslados a lunes en los CSV existentes')
    parser.add_argument('--forzar-no-oficial', action='store_true',
                        help='Acepta páginas marcadas «No Oficial» (no recomendado)')
    parser.add_argument('--si', action='store_true',
                        help='No preguntar (ejecuciones no interactivas)')
    parser.add_argument('--push', action='store_true', help='git commit + push al finalizar')
    parser.add_argument('--token', type=str, default='', help='GitHub Personal Access Token')
    parser.add_argument('--detalle', action='store_true', help='Muestra los festivos descargados')
    args = parser.parse_args()

    destino = os.path.normpath(args.destino)
    if not os.path.isdir(destino):
        print(f"ERROR: la carpeta destino no existe: {destino}")
        sys.exit(2)

    print("=" * 70)
    print(f"  ACTUALIZACIÓN DE FESTIVOS{f' — AÑO {args.anio}' if args.anio else ''}")
    print(f"  Destino: {destino}")
    print(f"  Inicio:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    hubo_cambios = False

    # ── Corrección de traslados (puede combinarse con --anio) ────────────────
    if args.corregir_traslados:
        hubo_cambios = corregir_traslados(destino) > 0
        if not args.anio:
            if args.push and hubo_cambios:
                hacer_push_github(destino, 'Corrección festivos trasladados al lunes', args.token)
            return

    if not args.anio:
        parser.error('indica --anio (o usa --corregir-traslados)')
    anio = args.anio

    # ── Modo solo-comprobar ───────────────────────────────────────────────────
    if args.comprobar:
        sys.exit(0 if comprobar_disponibilidad(anio) else 1)

    # ── Comprobar antes de descargar ──────────────────────────────────────────
    if not comprobar_disponibilidad(anio) and not args.forzar_no_oficial:
        print(f"\n⚠️  No hay calendario oficial de {anio} en la web. No se descarga nada.")
        print("   (Solo con --forzar-no-oficial se aceptarían los festivos estimados; no es recomendable.)")
        sys.exit(1)

    # ── Descarga y fusión ─────────────────────────────────────────────────────
    print(f"\n📥 Descargando festivos {anio} para {len(PROVINCIAS)} provincias...\n")
    ok, fallidas, total_nuevos = 0, [], 0

    for i, (nombre, slug) in enumerate(PROVINCIAS.items(), 1):
        archivo = slug_a_nombre_archivo(slug)
        ruta_csv = os.path.join(destino, f"{archivo}.csv")
        print(f"[{i:2d}/{len(PROVINCIAS)}] {nombre:<16s}", end=" ", flush=True)

        if archivo in EUSKADI_OFICIAL:
            # Euskadi se mantiene desde el BOPV/BOB/BOG/BOTHA en festivos/ (modelo por capas);
            # los CSV planos bizkaia/gipuzkoa/araba_alava se regeneran con herramientas/generar_planos.py
            print("⏭️  Euskadi: fuentes oficiales (festivos/ccaa, territorial, local); no se scrapea")
            ok += 1
            continue

        nuevos, estado = scrapear_provincia(slug, anio, args.forzar_no_oficial)
        if estado != 'ok':
            print(f"❌ {estado}")
            fallidas.append(f"{nombre} ({estado})")
            time.sleep(0.3)
            continue
        if len(nuevos) < MIN_FESTIVOS:
            print(f"⚠️  solo {len(nuevos)} festivos: se omite por sospechoso")
            fallidas.append(f"{nombre} (solo {len(nuevos)} festivos)")
            time.sleep(0.3)
            continue

        existentes = leer_csv(ruta_csv)
        # Fusión por fecha: si el año ya está (p. ej. cargado a mano desde el
        # BOPV), solo se añaden las fechas que falten; nunca se pisa lo existente.
        fechas_ya = {r['Fecha'] for r in existentes}
        a_anadir = [f for f in nuevos if f['Fecha'] not in fechas_ya]
        ok += 1
        if not a_anadir:
            print(f"⏭️  {anio} ya completo en {archivo}.csv ({len(nuevos)} festivos ya presentes)")
            time.sleep(0.2)
            continue

        escribir_csv(ruta_csv, existentes + a_anadir)
        escribir_capa_provincia(destino, archivo, existentes + a_anadir)
        total_nuevos += len(a_anadir)
        hubo_cambios = True
        print(f"✅ +{len(a_anadir)} festivos → {archivo}.csv")
        if args.detalle:
            for f in a_anadir:
                print(f"      {f['Fecha']}  {f['Festividad']}")
        time.sleep(0.3)

    # ── Resumen ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  RESUMEN:")
    print(f"  • Provincias correctas: {ok}/{len(PROVINCIAS)}")
    if fallidas:
        print(f"  • Con errores ({len(fallidas)}): {', '.join(fallidas)}")
    print(f"  • Festivos nuevos añadidos: {total_nuevos}")
    print(f"  • Archivos en: {destino}")
    print(f"  Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    if args.push and hubo_cambios:
        hacer_push_github(destino,
                          f"Actualización festivos {anio} — {datetime.now().strftime('%Y-%m-%d')}",
                          args.token)
    elif args.push:
        print("\n⚠️  No se hace push porque no hubo cambios.")

    if fallidas:
        print(f"\n💡 Para reintentar: python3 actualizar_festivos.py --anio {anio}")
        sys.exit(1)


if __name__ == "__main__":
    main()
