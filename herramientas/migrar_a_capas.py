#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrar_a_capas.py — Construye la carpeta `festivos/` (modelo por capas) a partir de:

  * los 52 CSV provinciales planos de la raíz del repo (2025-2026, más 2027 en Euskadi),
  * festivos/fuentes/opendata_euskadi_calendario_laboral_2026.ics (todos los municipios vascos),
  * festivos/fuentes/{bizkaia,gipuzkoa,araba}_municipios_2027.csv (BOB, BOG y prensa),
  * las listas nacionales fijas.

Capas generadas (todas con columnas Fecha,Festividad,Fuente):

  festivos/nacional.csv                      festivos de ámbito estatal
  festivos/ccaa/pv.csv                       festivos autonómicos de Euskadi
  festivos/territorial/{araba,bizkaia,gipuzkoa}.csv
  festivos/local/<slug-municipio>.csv        festivos locales (Euskadi)
  festivos/provincia/<slug>.csv              calendario plano heredado del resto de provincias
  festivos/lugares.json                      índice de lugares seleccionables y sus capas

Idempotente: se puede volver a ejecutar; sobrescribe lo generado.
Se ejecuta desde la raíz del repo:  python3 herramientas/migrar_a_capas.py
"""
import csv
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEST = os.path.join(RAIZ, 'festivos')
FUENTES = os.path.join(FEST, 'fuentes')

# ─────────────────────────────────────────────────────────────────────────────
#  Catálogo de provincias (slug del CSV plano → nombre, CCAA)
# ─────────────────────────────────────────────────────────────────────────────
PROVINCIAS = {
    'a-coruna': ('A Coruña', 'ga'), 'lugo': ('Lugo', 'ga'), 'ourense': ('Ourense', 'ga'), 'pontevedra': ('Pontevedra', 'ga'),
    'asturias': ('Asturias', 'as'), 'cantabria': ('Cantabria', 'cb'),
    'araba_alava': ('Araba/Álava', 'pv'), 'bizkaia': ('Bizkaia', 'pv'), 'gipuzkoa': ('Gipuzkoa', 'pv'),
    'navarra': ('Navarra', 'na'), 'la-rioja': ('La Rioja', 'ri'),
    'huesca': ('Huesca', 'ar'), 'teruel': ('Teruel', 'ar'), 'zaragoza': ('Zaragoza', 'ar'),
    'barcelona': ('Barcelona', 'ct'), 'girona': ('Girona', 'ct'), 'lleida': ('Lleida', 'ct'), 'tarragona': ('Tarragona', 'ct'),
    'alicante': ('Alicante/Alacant', 'vc'), 'castellon': ('Castellón/Castelló', 'vc'), 'valencia': ('Valencia/València', 'vc'),
    'baleares': ('Illes Balears', 'ib'),
    'avila': ('Ávila', 'cl'), 'burgos': ('Burgos', 'cl'), 'leon': ('León', 'cl'), 'palencia': ('Palencia', 'cl'),
    'salamanca': ('Salamanca', 'cl'), 'segovia': ('Segovia', 'cl'), 'soria': ('Soria', 'cl'), 'valladolid': ('Valladolid', 'cl'), 'zamora': ('Zamora', 'cl'),
    'madrid': ('Madrid', 'md'),
    'albacete': ('Albacete', 'cm'), 'ciudad-real': ('Ciudad Real', 'cm'), 'cuenca': ('Cuenca', 'cm'), 'guadalajara': ('Guadalajara', 'cm'), 'toledo': ('Toledo', 'cm'),
    'badajoz': ('Badajoz', 'ex'), 'caceres': ('Cáceres', 'ex'),
    'almeria': ('Almería', 'an'), 'cadiz': ('Cádiz', 'an'), 'cordoba': ('Córdoba', 'an'), 'granada': ('Granada', 'an'),
    'huelva': ('Huelva', 'an'), 'jaen': ('Jaén', 'an'), 'malaga': ('Málaga', 'an'), 'sevilla': ('Sevilla', 'an'),
    'murcia': ('Murcia', 'mc'),
    'las-palmas': ('Las Palmas', 'cn'), 'tenerife': ('Santa Cruz de Tenerife', 'cn'),
    'ceuta': ('Ceuta', 'ce'), 'melilla': ('Melilla', 'ml'),
}
CCAA = {
    'ga': 'Galicia', 'as': 'Asturias', 'cb': 'Cantabria', 'pv': 'País Vasco', 'na': 'Navarra', 'ri': 'La Rioja',
    'ar': 'Aragón', 'ct': 'Cataluña', 'vc': 'Comunitat Valenciana', 'ib': 'Illes Balears', 'cl': 'Castilla y León',
    'md': 'Comunidad de Madrid', 'cm': 'Castilla-La Mancha', 'ex': 'Extremadura', 'an': 'Andalucía', 'mc': 'Región de Murcia',
    'cn': 'Canarias', 'ce': 'Ceuta', 'ml': 'Melilla',
}

# ─────────────────────────────────────────────────────────────────────────────
#  Datos verificados a mano
# ─────────────────────────────────────────────────────────────────────────────
F_BOE = 'Festivo estatal (art. 37.2 ET; resolución anual del BOE)'
NACIONAL = {
    2025: [('2025-01-01', 'Año Nuevo'), ('2025-01-06', 'Epifanía del Señor'), ('2025-04-18', 'Viernes Santo'),
           ('2025-05-01', 'Fiesta del Trabajo'), ('2025-08-15', 'Asunción de la Virgen'), ('2025-10-12', 'Fiesta Nacional de España'),
           ('2025-11-01', 'Todos los Santos'), ('2025-12-06', 'Día de la Constitución'), ('2025-12-08', 'Inmaculada Concepción'),
           ('2025-12-25', 'Navidad')],
    2026: [('2026-01-01', 'Año Nuevo'), ('2026-01-06', 'Epifanía del Señor'), ('2026-04-03', 'Viernes Santo'),
           ('2026-05-01', 'Fiesta del Trabajo'), ('2026-08-15', 'Asunción de la Virgen'), ('2026-10-12', 'Fiesta Nacional de España'),
           ('2026-11-01', 'Todos los Santos'), ('2026-12-06', 'Día de la Constitución'), ('2026-12-08', 'Inmaculada Concepción'),
           ('2026-12-25', 'Navidad')],
    2027: [('2027-01-01', 'Año Nuevo'), ('2027-01-06', 'Epifanía del Señor'), ('2027-03-26', 'Viernes Santo'),
           ('2027-05-01', 'Fiesta del Trabajo'), ('2027-08-15', 'Asunción de la Virgen'), ('2027-10-12', 'Fiesta Nacional de España'),
           ('2027-11-01', 'Todos los Santos'), ('2027-12-06', 'Día de la Constitución'), ('2027-12-08', 'Inmaculada Concepción'),
           ('2027-12-25', 'Navidad')],
}
# Euskadi: festivos autonómicos que NO son estatales
F_PV_2025 = 'Calendario laboral CAE 2025 (Gobierno Vasco)'
F_PV_2026 = 'Decreto Gobierno Vasco calendario laboral 2026; Open Data Euskadi'
F_PV_2027 = 'Decreto 90/2026, de 9 de junio (BOPV 16/07/2026)'
PV = [
    ('2025-04-17', 'Jueves Santo', F_PV_2025), ('2025-04-21', 'Lunes de Pascua', F_PV_2025), ('2025-07-25', 'Santiago Apóstol', F_PV_2025),
    ('2025-10-25', 'Día del País Vasco (sábado)', 'calendarioslaborales.com 2025 (coincide en Araba, Bizkaia y Gipuzkoa); sin efecto en plazos'),
    ('2026-03-19', 'San José', F_PV_2026), ('2026-04-02', 'Jueves Santo', F_PV_2026), ('2026-04-06', 'Lunes de Pascua', F_PV_2026),
    ('2026-07-25', 'Santiago Apóstol', F_PV_2026),
    ('2027-03-25', 'Jueves Santo', F_PV_2027), ('2027-03-29', 'Lunes de Pascua', F_PV_2027),
    ('2027-10-07', 'Aniversario del primer Gobierno de Euskadi', F_PV_2027),
]
TERRITORIAL = {
    'araba': [('2025-04-28', 'San Prudencio', F_PV_2025), ('2026-04-28', 'San Prudencio', F_PV_2026), ('2027-04-28', 'San Prudencio', F_PV_2027)],
    'bizkaia': [('2025-07-31', 'San Ignacio de Loyola', F_PV_2025), ('2026-07-31', 'San Ignacio de Loyola', F_PV_2026),
                ('2027-07-31', 'San Ignacio de Loyola', 'BOB núm. 181, 22/09/2026')],
    'gipuzkoa': [('2025-07-31', 'San Ignacio de Loyola', F_PV_2025), ('2026-07-31', 'San Ignacio de Loyola', F_PV_2026),
                 ('2027-07-31', 'San Ignacio de Loyola', 'BOG núm. 187, 01/10/2026')],
}
# Locales 2025 de capitales vascas con fuente conocida (Bilbao 2025 sin fuente oficial: no se incluye)
LOCALES_2025 = {
    'donostia-san-sebastian': [('2025-01-20', 'San Sebastián', 'Calendario laboral Donostia 2025')],
    'vitoria-gasteiz': [('2025-08-05', 'Virgen Blanca', 'Calendario laboral Vitoria-Gasteiz 2025')],
}
CAPITALES = {'bilbao': 'bizkaia', 'donostia-san-sebastian': 'gipuzkoa', 'vitoria-gasteiz': 'araba'}
PARTIDOS_JUDICIALES = {
    'araba': ['vitoria-gasteiz', 'amurrio'],
    'bizkaia': ['bilbao', 'barakaldo', 'getxo', 'durango', 'gernika-lumo', 'balmaseda'],
    'gipuzkoa': ['donostia-san-sebastian', 'irun', 'tolosa', 'eibar', 'azpeitia', 'bergara'],
}
# Nombres de los boletines 2027 → slug del ICS (cuando no coinciden al normalizar)
ALIAS = {
    'arrasate-mondragon': 'mondragon', 'soraluze-placencia-de-las-armas': 'soraluze-placencia-de-las-armas',
    'valle-de-karrantza': 'valle-de-carranza', 'abanto-y-ciervana': 'abanto-y-ciervana-abanto-zierbena',
    'trucios': 'trucios-turtzioz', 'orduna': 'urduna-orduna', 'sopela': 'sopelana', 'zaratamo': 'zaratamo',
    'arrankudiaga-zollo': 'arrankudiaga-zollo', 'munitibar-arbatzegi-gerrikaitz': 'munitibar-arbatzegi-gerrikaitz',
    'leaburu-txarama': 'leaburu-txarama', 'ezkio-itsaso-barrio-ezkio': 'ezkio-itsaso-barrio-ezkio',
    'ezkio-itsaso-barrio-santa-luzia-anduaga': 'ezkio-itsaso-barrio-santa-luzia-anduaga',
    'ezkio-itsaso-barrio-itsaso-alegia': 'ezkio-itsaso-barrio-itsaso-alegia',
    'ezkio-itsaso-itsaso-centro': 'ezkio-itsaso-itsaso-centro', 'ezkio-itsaso-mendialdea-zozkera': 'ezkio-itsaso-mendialdea',
    'bidania-goiatz-bidania': 'bidania-goiatz-bidania', 'bidania-goiatz-goiatz': 'bidania-goiatz-goiatz',
    'pasaia-donibane': 'pasaia-p-donibane', 'pasaia-san-pedro': 'pasaia-p-san-pedro', 'pasaia-antxo': 'pasaia-p-antxo',
    'pasaia-trintxerpe': 'pasaia-trintxerpe', 'villabona': 'villabona', 'elduain': 'elduaien', 'belauntza': 'belaunza',
    'san-sebastian': 'donostia-san-sebastian', 'leaburu': 'leaburu-txarama', 'placencia-de': 'soraluze-placencia-de-las-armas',
    'soraluze': 'soraluze-placencia-de-las-armas', 'arratzua-ubarrundia': 'arrazua-ubarrundia',
    'iruna-de-oca': 'iruna-de-oca-nanclares-de-la-oca',
    'zierbena': 'zierbena', 'usansolo': 'usansolo', 'gueenes': 'guenes', 'guenes': 'guenes', 'donostia-san-sebastian': 'donostia-san-sebastian',
}

CPRO_A_SLUG = {
    '01': 'araba_alava', '02': 'albacete', '03': 'alicante', '04': 'almeria', '05': 'avila', '06': 'badajoz',
    '07': 'baleares', '08': 'barcelona', '09': 'burgos', '10': 'caceres', '11': 'cadiz', '12': 'castellon',
    '13': 'ciudad-real', '14': 'cordoba', '15': 'a-coruna', '16': 'cuenca', '17': 'girona', '18': 'granada',
    '19': 'guadalajara', '20': 'gipuzkoa', '21': 'huelva', '22': 'huesca', '23': 'jaen', '24': 'leon', '25': 'lleida',
    '26': 'la-rioja', '27': 'lugo', '28': 'madrid', '29': 'malaga', '30': 'murcia', '31': 'navarra', '32': 'ourense',
    '33': 'asturias', '34': 'palencia', '35': 'las-palmas', '36': 'pontevedra', '37': 'salamanca', '38': 'tenerife',
    '39': 'cantabria', '40': 'segovia', '41': 'sevilla', '42': 'soria', '43': 'tarragona', '44': 'teruel', '45': 'toledo',
    '46': 'valencia', '47': 'valladolid', '48': 'bizkaia', '49': 'zamora', '50': 'zaragoza', '51': 'ceuta', '52': 'melilla',
}
# Nombre de cabecera en el Censo Judicial → id usado en festivos/local/ (solo cuando el slug no coincide)
ALIAS_CABECERAS = {}

PALABRAS_MINUSCULA = {'de', 'del', 'la', 'las', 'los', 'el', 'y', 'e', 'i', 'o', 'a', 'd', 'da', 'das', 'do', 'dos', 'en', 'les', 'sa', 'ses', 'na', 'o'}


def titulo(nombre: str) -> str:
    """'DONOSTIA/SAN SEBASTIÁN' → 'Donostia/San Sebastián'; 'ALCALÁ DE HENARES' → 'Alcalá de Henares'."""
    partes = re.split(r'(\s+|/|-|\(|\))', nombre.strip())
    out = []
    for i, p in enumerate(partes):
        if not p or re.fullmatch(r'\s+|/|-|\(|\)', p):
            out.append(p)
            continue
        pl = p.lower()
        if pl in PALABRAS_MINUSCULA and i != 0 and out and not out[-1].endswith(('(', '/', '-')):
            out.append(pl)
        elif "'" in p:
            out.append("'".join(x.capitalize() for x in pl.split("'")))
        else:
            out.append(pl.capitalize())
    return ''.join(out)


# Concejos del municipio de Ayala/Aiara: el BOTHA los lista sueltos; el ICS como «Ayala - <concejo>»
CONCEJOS_AYALA = {'aginaga', 'anes', 'beotegi', 'costera', 'erbi', 'etxegoien', 'izoria', 'lejarzo', 'lujo', 'luiaondo',
                  'llanteno', 'madaria', 'marono', 'menagarai', 'menoio', 'murga', 'olabezar', 'ozeka', 'quejana',
                  'respaldiza', 'retes-de-llanteno', 'salmanton', 'sojo', 'zuaza'}

MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
         'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}


# ─────────────────────────────────────────────────────────────────────────────
#  Utilidades
# ─────────────────────────────────────────────────────────────────────────────
def slug(texto: str, bilingue: bool = False) -> str:
    """Identificador estable. Con bilingue=True toma solo la parte castellana de 'Bilbao / Bilbo'."""
    t = texto.split(' / ')[0] if bilingue else texto
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    t = re.sub(r'[^A-Za-z0-9]+', '-', t).strip('-').lower()
    return t


def leer_plano(ruta):
    filas = []
    with open(ruta, newline='', encoding='utf-8-sig') as f:
        for r in csv.reader(f):
            if r and r[0].strip() and r[0].strip().lower() != 'fecha':
                filas.append((r[0].strip(), r[1].strip() if len(r) > 1 else ''))
    return filas


def escribir_capa(ruta, filas):
    """filas: iterable de (fecha, nombre, fuente). Ordena y elimina fechas repetidas."""
    unicos = {}
    for fecha, nombre, fuente in filas:
        unicos.setdefault(fecha, (fecha, nombre, fuente))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['Fecha', 'Festividad', 'Fuente'])
        for k in sorted(unicos):
            w.writerow(unicos[k])
    return len(unicos)


def leer_ics(ruta):
    """Devuelve lista de (fecha_iso, resumen_es, location_es). Corrige la doble codificación del fichero."""
    raw = open(ruta, 'rb').read().decode('utf-8', 'replace')
    try:
        raw = raw.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    eventos = []
    for ev in raw.split('BEGIN:VEVENT')[1:]:
        d = re.search(r'DTSTART;VALUE=DATE:(\d{4})(\d{2})(\d{2})', ev)
        s = re.search(r'SUMMARY:(.*)', ev)
        l = re.search(r'LOCATION:(.*)', ev)
        if d and s and l:
            eventos.append((f"{d.group(1)}-{d.group(2)}-{d.group(3)}",
                            s.group(1).split(' / ')[0].strip(), l.group(1).strip()))
    return eventos


CCAA_NOMBRE_A_CODIGO = {
    'ANDALUCÍA': 'an', 'ARAGÓN': 'ar', 'ASTURIAS': 'as', 'CANARIAS': 'cn', 'CANTABRIA': 'cb', 'CASTILLA Y LEÓN': 'cl',
    'CASTILLA-LA MANCHA': 'cm', 'CATALUÑA': 'ct', 'CEUTA': 'ce', 'COMUNITAT VALENCIANA': 'vc', 'EXTREMADURA': 'ex',
    'GALICIA': 'ga', 'ILLES BALEARS': 'ib', 'LA RIOJA': 'ri', 'MADRID': 'md', 'MELILLA': 'ml', 'MURCIA': 'mc',
    'NAVARRA': 'na', 'PAÍS VASCO': 'pv',
}


def _codigo_ccaa(texto: str) -> str | None:
    t = unicodedata.normalize('NFKD', texto or '').encode('ascii', 'ignore').decode().upper().strip()
    for nombre, codigo in CCAA_NOMBRE_A_CODIGO.items():
        n = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode().upper()
        if t == n or t == codigo.upper():
            return codigo
    for nombre, codigo in CCAA_NOMBRE_A_CODIGO.items():
        n = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode().upper()
        if n in t or t in n:
            return codigo
    return None


def _fecha_valida(f: str) -> bool:
    try:
        date.fromisoformat(f)
        return True
    except (ValueError, TypeError):
        return False


# Canarias: cada isla tiene un festivo insular propio (sustituye a Santiago Apóstol). Cabecera → isla.
ISLA_DE_CABECERA = {
    'arrecife': 'lanzarote', 'puerto-del-rosario': 'fuerteventura',
    'arucas': 'gran-canaria', 'las-palmas-de-gran-canaria': 'gran-canaria', 'san-bartolome-de-tirajana': 'gran-canaria',
    'santa-maria-de-guia-de-gran-canaria': 'gran-canaria', 'telde': 'gran-canaria',
    'arona': 'tenerife', 'granadilla-de-abona': 'tenerife', 'guimar': 'tenerife', 'icod-de-los-vinos': 'tenerife',
    'la-orotava': 'tenerife', 'puerto-de-la-cruz': 'tenerife', 'san-cristobal-de-la-laguna': 'tenerife',
    'santa-cruz-de-tenerife': 'tenerife',
    'los-llanos-de-aridane': 'la-palma', 'santa-cruz-de-la-palma': 'la-palma',
    'san-sebastian-de-la-gomera': 'la-gomera', 'valverde': 'el-hierro',
}
RE_INSULAR = re.compile(r'festivo insular\s+(.+?)\s*$', re.I)


def _slug_isla(texto: str) -> str | None:
    t = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode().lower()
    for isla in ('tenerife', 'gran canaria', 'lanzarote', 'fuerteventura', 'la palma', 'la gomera', 'el hierro'):
        if isla in t:
            return isla.replace(' ', '-')
    return None


def construir_resto_espana(ine_a_slug: dict, partidos: list) -> tuple[dict, dict, dict, list]:
    """
    Lee festivos/fuentes/locales/locales_*.csv (ccaa,cpro,ine_municipio,municipio,fecha,festividad,fuente,url,calidad)
    y ccaa_*.csv (ccaa,fecha,festividad,fuente,url). Devuelve:
      locales: {slug_cabecera: [(fecha, nombre, fuente)]}   solo cabeceras no vascas
      ccaa:    {codigo: [(fecha, nombre, fuente)]}          festivos autonómicos (sin los estatales)
      resumen: líneas informativas
    La capa autonómica se completa, para los años sin ccaa_*.csv, derivándola de los CSV provinciales planos:
    intersección de las provincias de la CCAA menos los estatales (en CCAA uniprovinciales, menos además los locales
    de la capital si se conocen).
    """
    carpeta = os.path.join(FUENTES, 'locales')
    locales = defaultdict(list)
    ccaa = defaultdict(list)
    insular = defaultdict(list)
    resumen = []
    if not os.path.isdir(carpeta):
        return {}, {}, {}, ['(sin carpeta festivos/fuentes/locales)']

    nacional_por_anio = defaultdict(set)
    for anio, filas in NACIONAL.items():
        for f, _ in filas:
            nacional_por_anio[anio].add(f)

    descartadas = 0
    for nombre in sorted(os.listdir(carpeta)):
        ruta = os.path.join(carpeta, nombre)
        if nombre.startswith('locales_') and nombre.endswith('.csv'):
            with open(ruta, newline='', encoding='utf-8-sig') as f:
                for r in csv.DictReader(f):
                    ine = (r.get('ine_municipio') or '').strip().zfill(5)
                    fecha = (r.get('fecha') or '').strip()
                    if ine not in ine_a_slug or not _fecha_valida(fecha):
                        descartadas += 1
                        continue
                    s = ine_a_slug[ine]
                    fuente = (r.get('fuente') or '').strip()
                    if (r.get('calidad') or '').strip() not in ('', 'oficial'):
                        fuente = f"{fuente} [{r['calidad'].strip()}]"
                    locales[s].append((fecha, (r.get('festividad') or '').strip() or 'Fiesta local', fuente))
        elif nombre.startswith('ccaa_') and nombre.endswith('.csv'):
            with open(ruta, newline='', encoding='utf-8-sig') as f:
                for r in csv.DictReader(f):
                    codigo = _codigo_ccaa(r.get('ccaa', ''))
                    fecha = (r.get('fecha') or '').strip()
                    if not codigo or not _fecha_valida(fecha) or codigo == 'pv':
                        continue
                    if fecha in nacional_por_anio.get(int(fecha[:4]), set()):
                        continue  # estatal: ya está en nacional.csv
                    nombre_f = (r.get('festividad') or '').strip() or 'Festivo autonómico'
                    if codigo == 'ct' and 'aran' in nombre_f.lower() and ('només' in nombre_f.lower() or 'solo' in nombre_f.lower() or 'sólo' in nombre_f.lower()):
                        # Festa d'Aran: solo rige en la Val d'Aran (cabecera Vielha e Mijaran) → capa territorial/aran
                        insular['__aran__'].append((fecha, nombre_f, (r.get('fuente') or '').strip()))
                        continue
                    m_ins = RE_INSULAR.search(nombre_f)
                    if codigo == 'cn' and m_ins and _slug_isla(m_ins.group(1)):
                        insular[_slug_isla(m_ins.group(1))].append((fecha, nombre_f, (r.get('fuente') or '').strip()))
                        continue
                    ccaa[codigo].append((fecha, nombre_f, (r.get('fuente') or '').strip()))
    if descartadas:
        resumen.append(f"filas de locales descartadas (INE no es cabecera o fecha inválida): {descartadas}")

    # Capitales por CCAA (slug) para limpiar la derivación en CCAA uniprovinciales
    capitales = {}
    for p in partidos:
        if p['es_capital_provincia'] == 'si':
            capitales.setdefault(PROVINCIAS[CPRO_A_SLUG[p['cpro']]][1], []).append(ine_a_slug[p['ine_cabecera']])

    # Derivación desde los planos para los años que falten en cada CCAA
    provincias_por_ccaa = defaultdict(list)
    for slug_prov, (_, codigo) in PROVINCIAS.items():
        if codigo != 'pv':
            provincias_por_ccaa[codigo].append(slug_prov)
    for codigo, provs in provincias_por_ccaa.items():
        anios_ccaa = {f[:4] for f, _, _ in ccaa.get(codigo, [])}
        planos = []
        for sp in provs:
            ruta = os.path.join(RAIZ, f'{sp}.csv')
            planos.append({f: n for f, n in leer_plano(ruta)} if os.path.exists(ruta) else {})
        anios_planos = {f[:4] for pl in planos for f in pl}
        for anio in sorted(anios_planos - anios_ccaa):
            comunes = None
            for pl in planos:
                fechas = {f for f in pl if f.startswith(anio)}
                comunes = fechas if comunes is None else comunes & fechas
            comunes = (comunes or set()) - nacional_por_anio.get(int(anio), set())
            # Quitar los locales conocidos de las capitales: en CCAA uniprovinciales son todo el "exceso" del plano,
            # y en las demás evitan que un local compartido por todas las capitales (p. ej. San Juan) parezca autonómico.
            for cap in capitales.get(codigo, []):
                comunes -= {f for f, _, _ in locales.get(cap, []) if f.startswith(anio)}
            nombres = planos[0]
            for f in sorted(comunes):
                ccaa[codigo].append((f, nombres.get(f, 'Festivo autonómico'),
                                     f'Derivado de los calendarios provinciales {anio} (calendarioslaborales.com)'))
            if comunes:
                resumen.append(f"ccaa/{codigo} {anio}: {len(comunes)} autonómicos derivados de los planos")
    return dict(locales), dict(ccaa), dict(insular), resumen


# ─────────────────────────────────────────────────────────────────────────────
#  Construcción
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # 1. Nacional
    n = escribir_capa(os.path.join(FEST, 'nacional.csv'),
                      [(f, nom, F_BOE) for anio in NACIONAL for f, nom in NACIONAL[anio]])
    print(f"nacional.csv: {n} festivos")

    # 2. Autonómico Euskadi
    n = escribir_capa(os.path.join(FEST, 'ccaa', 'pv.csv'), PV)
    print(f"ccaa/pv.csv: {n}")

    # 3. Territorial
    for t, filas in TERRITORIAL.items():
        escribir_capa(os.path.join(FEST, 'territorial', f'{t}.csv'), filas)
    print("territorial: araba, bizkaia, gipuzkoa")

    # 4. Local Euskadi: ICS 2026 + boletines 2027 + capitales 2025
    locales = defaultdict(list)      # slug → [(fecha, nombre, fuente)]
    nombres = {}                     # slug → nombre legible
    territorio_de = {}               # slug → araba/bizkaia/gipuzkoa (se deduce de los boletines)
    ics = os.path.join(FUENTES, 'opendata_euskadi_calendario_laboral_2026.ics')
    for fecha, resumen, loc in leer_ics(ics):
        if loc.startswith('CAE') or loc.startswith('Bizkaia') or loc.startswith('Gipuzkoa') or loc.startswith('Álava'):
            continue
        s = slug(loc, bilingue=True)
        nombres.setdefault(s, loc.split(' / ')[0].strip())
        locales[s].append((fecha, resumen, 'Open Data Euskadi, calendario laboral 2026'))
    print(f"ICS 2026: {len(locales)} localidades")

    # Boletines oficiales por territorio y año (bizkaia|gipuzkoa|araba)_municipios_<año>.csv. Para un municipio
    # y año presentes en el boletín, el boletín SUSTITUYE lo que dijera el ICS de Open Data Euskadi de ese año
    # (el ICS no recoge las modificaciones posteriores: p. ej. Bilbao 2026 pasó del 21 al 28 de agosto).
    sin_match = []
    ficheros_oficiales = sorted(f for f in os.listdir(FUENTES) if re.match(r'(bizkaia|gipuzkoa|araba)_municipios_\d{4}\.csv$', f))
    sustituidos = set()
    for fichero in ficheros_oficiales:
        terr = fichero.split('_')[0]
        with open(os.path.join(FUENTES, fichero), newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r['Municipio'].startswith('(') or not r['Fecha'][:4].isdigit():
                    continue
                s0 = slug(r['Municipio'])
                s = ALIAS.get(s0, s0)
                if s in CONCEJOS_AYALA:
                    s = 'ayala-' + s
                anio = r['Fecha'][:4]
                if s not in locales and s not in nombres:
                    sin_match.append((terr, r['Municipio'], s))
                    nombres[s] = r['Municipio']
                if (s, anio) not in sustituidos:
                    locales[s] = [fila for fila in locales[s]
                                  if not (fila[0].startswith(anio) and fila[2].startswith('Open Data Euskadi'))]
                    sustituidos.add((s, anio))
                territorio_de[s] = terr
                locales[s].append((r['Fecha'], r['Festividad'] or 'Fiesta local', r['Fuente']))
    print(f"boletines oficiales aplicados: {ficheros_oficiales} ({len(sustituidos)} municipio-año sustituyen al ICS)")
    for s, filas in LOCALES_2025.items():
        locales[s].extend(filas)

    # Territorio de las localidades que solo están en el ICS 2026: los boletines 2027 de Bizkaia y Gipuzkoa
    # cubren todos sus municipios, así que lo que queda sin asignar es de Araba (cuyo BOTHA 2027 aún no
    # se ha publicado), salvo sub-localidades (barrios, concejos) cuyo municipio ya tiene territorio.
    for s in locales:
        if s in territorio_de:
            continue
        padre = next((p for p in territorio_de if s.startswith(p + '-')), None)
        territorio_de[s] = territorio_de[padre] if padre else 'araba'

    for s, filas in locales.items():
        escribir_capa(os.path.join(FEST, 'local', f'{s}.csv'), filas)
    print(f"local/: {len(locales)} ficheros")
    if sin_match:
        print("  ⚠️  Nombres de boletín 2027 sin correspondencia en el ICS 2026 (se crean como localidad nueva):")
        for terr, nombre, s in sin_match:
            print(f"      {terr:9s} {nombre!r:45s} → {s}")

    # 5. Provincias no vascas: capa plana heredada
    for slug_prov, (nombre, ccaa) in PROVINCIAS.items():
        if ccaa == 'pv':
            continue
        filas = [(f, nom, 'CSV provincial heredado (calendarioslaborales.com, incluye locales de la capital)')
                 for f, nom in leer_plano(os.path.join(RAIZ, f'{slug_prov}.csv'))]
        escribir_capa(os.path.join(FEST, 'provincia', f'{slug_prov}.csv'), filas)
    print("provincia/: 49 ficheros heredados")

    # 5b. Resto de España: festivos locales de las cabeceras (boletines/datos abiertos de cada CCAA, recogidos en
    #     festivos/fuentes/locales/locales_*.csv) y capa autonómica (ccaa_*.csv + derivación desde los planos).
    with open(os.path.join(FUENTES, 'partidos_judiciales_mjusticia.csv'), newline='', encoding='utf-8') as f:
        partidos = list(csv.DictReader(f))
    ine_a_slug = {}
    for p in partidos:
        s0 = slug(p['cabecera'])
        ine_a_slug[p['ine_cabecera']] = ALIAS_CABECERAS.get(s0, s0)
    locales_resto, ccaa_capas, insular_capas, resumen_locales = construir_resto_espana(ine_a_slug, partidos)
    for s, filas in locales_resto.items():
        escribir_capa(os.path.join(FEST, 'local', f'{s}.csv'), filas)
    for codigo, filas in ccaa_capas.items():
        escribir_capa(os.path.join(FEST, 'ccaa', f'{codigo}.csv'), filas)
    for isla, filas in insular_capas.items():
        if isla == '__aran__':
            escribir_capa(os.path.join(FEST, 'territorial', 'aran.csv'), filas)
        else:
            escribir_capa(os.path.join(FEST, 'insular', f'{isla}.csv'), filas)
    print(f"resto de España: {len(locales_resto)} cabeceras con festivos locales; capas ccaa/: {sorted(ccaa_capas)}; "
          f"insular/: {sorted(insular_capas)}")
    for linea in resumen_locales:
        print("  " + linea)

    # 6. Índice de lugares: SOLO cabeceras de partido judicial (incluyen las 52 capitales de provincia).
    #    Fuente: Censo Judicial del Ministerio de Justicia (festivos/fuentes/partidos_judiciales_mjusticia.csv).
    lugares = []
    sin_local = []
    pv_terr = {'01': 'araba', '20': 'gipuzkoa', '48': 'bizkaia'}
    for p in partidos:
        slug_prov = CPRO_A_SLUG[p['cpro']]
        nombre_prov, ccaa = PROVINCIAS[slug_prov]
        s = ine_a_slug[p['ine_cabecera']]
        es_capital = p['es_capital_provincia'] == 'si'
        lugar_ = {
            'id': s, 'nombre': titulo(p['cabecera']), 'tipo': 'partido_judicial',
            'ine': p['ine_cabecera'], 'provincia': nombre_prov, 'provincia_slug': slug_prov, 'cpro': p['cpro'],
            'ccaa': ccaa, 'ccaa_nombre': CCAA[ccaa], 'capital': es_capital, 'partido_judicial': True,
            'n_municipios': int(p['n_municipios']), 'poblacion': int(p['poblacion']),
        }
        if ccaa == 'pv':
            terr = pv_terr[p['cpro']]
            lugar_['territorio'] = terr
            lugar_['capas'] = ['nacional', 'ccaa/pv', f'territorial/{terr}', f'local/{s}']
            lugar_['locales_pendientes'] = s not in locales
            if s not in locales:
                sin_local.append(s)
        elif s in locales_resto and ccaa in ccaa_capas:
            # Modelo completo: estatal + autonómico (+ insular en Canarias) + local propio de la cabecera
            capas = ['nacional', f'ccaa/{ccaa}']
            if ccaa == 'cn' and s in ISLA_DE_CABECERA and ISLA_DE_CABECERA[s] in insular_capas:
                capas.append(f'insular/{ISLA_DE_CABECERA[s]}')
                lugar_['isla'] = ISLA_DE_CABECERA[s]
            if s == 'vielha-e-mijaran' and '__aran__' in insular_capas:
                capas.append('territorial/aran')
            capas.append(f'local/{s}')
            lugar_['capas'] = capas
            lugar_['locales_pendientes'] = False
        else:
            # Capa plana heredada de la provincia (incluye los locales de la capital). Para una cabecera que no es
            # capital, los festivos locales propios aún no están cargados: se avisa en la interfaz.
            lugar_['capas'] = [f'provincia/{slug_prov}']
            lugar_['locales_pendientes'] = not es_capital
            if not es_capital:
                lugar_['nota'] = f'Festivos locales de {titulo(p["cabecera"])} pendientes; se aplican los de {nombre_prov} capital.'
        lugares.append(lugar_)
    ids = [l['id'] for l in lugares]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        print(f"  ⚠️  ids duplicados: {sorted(dup)}")
    if sin_local:
        print(f"  ⚠️  Cabeceras vascas sin capa local: {sin_local}")
    lugares.sort(key=lambda l: (not l['capital'], l['nombre'].lower()))
    with open(os.path.join(FEST, 'lugares.json'), 'w', encoding='utf-8') as f:
        json.dump({'version': date.today().isoformat(),
                   'fuente_partidos': 'Censo Judicial, Ministerio de Justicia (planta Ley 38/1988; nomenclátor 30/12/2025)',
                   'lugares': lugares}, f, ensure_ascii=False, indent=1)
    caps = sum(1 for l in lugares if l['capital'])
    pend = sum(1 for l in lugares if l['locales_pendientes'])
    print(f"lugares.json: {len(lugares)} cabeceras de partido judicial ({caps} capitales; {pend} con festivos locales pendientes)")


if __name__ == '__main__':
    main()
