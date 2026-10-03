# INFORME – Grupo 5: GALICIA y EXTREMADURA (66 cabeceras de partido judicial)

Fecha de elaboración: 03/10/2026. Ficheros: `locales.csv` (156 filas), `ccaa.csv` (51 filas). Script: `build.py`. Documentos fuente descargados en `raw/`.

## Recuento

| | 2026 | 2027 |
|---|---|---|
| Cabeceras con festivos locales | **66 / 66** (todas, calidad `oficial`) | **12 / 66** (9 `oficial` + 3 `prensa`) |
| Galicia (45) | 45 oficial | 9 oficial (prov. Lugo) + 3 prensa (A Coruña, Ferrol, Pontevedra) |
| Extremadura (21) | 21 oficial | 0 |

Festivos autonómicos (`ccaa.csv`): Galicia 2026 (12) y 2027 (12); Extremadura 2026 (12 + 2 descansos trasladados) y 2027 (12 + 1 descanso trasladado).

## Fuentes usadas

### Galicia
- **Locales 2026 (oficial)**: dataset «Calendario laboral 2026» del portal Abertos de la Xunta (CSV con `id_municipio` = código INE, 35 KB), <https://abertos.xunta.gal/es/catalogo/economia-empresa-emprego/-/dataset/0684/calendario-laboral-2026>. Es la transcripción de la **Resolución de 21/10/2025 de la Secretaría Xeral de Emprego e Relacións Laborais, DOG núm. 210, 30/10/2025** <https://www.xunta.gal/dog/Publicados/2025/20251030/AnuncioG0767-221025-0001_es.html>. Comprobé las 90 fechas (45 cabeceras × 2) contra el texto del DOG: coinciden al 100 %. Nombres de festividad tomados del dataset (en gallego); en dos casos la fuente no da nombre (Caldas de Reis 14/08/2026 y Vigo 17/08/2026) y figura «Fiesta local». La columna `url` apunta al DOG.
- **Locales 2027, provincia de Lugo (oficial)**: **BOP Lugo núm. 221, 26/09/2026**, «Resolución sobre o calendario laboral do ano 2027 para a Provincia de Lugo» (Dirección Territorial de Emprego, Comercio e Emigración, 23/09/2026, R. 2552) <https://www.deputacionlugo.gal/sites/deputacionlugo.org/files/inline-files/26-09-2026.pdf> (PDF íntegro del boletín, págs. 1-3). Cubre las 9 cabeceras lucenses. Transcripción verificada por script contra el texto extraído con `pdftotext`.
- **Locales 2027, prensa (calidad `prensa`)**:
  - A Coruña (9/2 Martes de Entroido y 24/6 San Xoán): El Ideal Gallego 29/07/2026 (aprobación por la Xunta de Goberno Local) <https://www.elidealgallego.com/a-coruna/2026-07-29/confirmados-estos-seran-los-festivos-locales-de-a-coruna-en-870769.html>.
  - Ferrol (7/1 San Xiao y 29/3 Luns de Pascua–Chamorro): Quincemil/El Español 24/09/2026 (Pleno 24/09/2026) <https://www.elespanol.com/quincemil/ferrolterra/20260924/ferrol-aprueba-festivos-locales-enero-marzo/1003744396555_0.html>.
  - Pontevedra (10/2 Mércores de Cinza y 29/3 San Cibrán): Diario de Pontevedra 15/07/2026 <https://www.diariodepontevedra.es/articulo/pontevedra/pontevedra-cambiara-festivos-locales-2027/202607151309351459196.html>. La aprobación plenaria consta en el **extracto de acuerdos del Pleno de 20/07/2026 publicado en BOPPO núm. 141, 27/07/2026** («Determinación dos festivos locais do municipio para o ano 2027 – Aprobado»), pero el extracto no recoge las fechas; por eso la calidad es `prensa`.
- **Autonómicos 2026**: Decreto 46/2025, de 9 de junio, DOG núm. 117, 20/06/2025 <https://www.xunta.gal/dog/Publicados/2025/20250620/AnuncioG0767-120625-0002_es.html>.
- **Autonómicos 2027**: Decreto 68/2026, de 15 de junio, DOG núm. 122, 02/07/2026 <https://www.xunta.gal/dog/Publicados/2026/20260702/AnuncioG0767-250626-0001_es.html>. Coincide con el dataset «Calendario laboral 2027» de Abertos (alta 03/07/2026), que a fecha de hoy solo contiene los 12 festivos autonómicos (sin locales).

### Extremadura
- **Locales 2026 (oficial)**: Resolución de 15/10/2025 de la Dirección General de Trabajo, **DOE núm. 204, 23/10/2025** <https://doe.juntaex.es/pdfs/doe/2025/2040o/25063799.pdf>. Las 21 cabeceras extraídas del PDF con `pdftotext`. La fuente no da nombre de festividad → «Fiesta local».
- **Modificaciones 2026** (revisé los sumarios diarios del DOE del 24/10/2025 al 02/10/2026 buscando «fiestas locales»): Res. 17/11/2025 (DOE 230, 28/11: Trasierra, Navalvillar de Pela, Almaraz); Res. 09/12/2025 (DOE 242, 17/12: Torrejoncillo); Res. 27/01/2026 (DOE 24, 05/02: Ribera del Fresno); Res. 04/03/2026 (DOE 58, 25/03: Alcuéscar); Res. 25/03/2026 (DOE 64, 06/04: Cuacos de Yuste); Res. 07/04/2026 (DOE 68, 10/04: Cuacos de Yuste); **Res. 17/04/2026 (DOE 81, 29/04: DON BENITO → 6 de abril y 11 de septiembre)** <https://doe.juntaex.es/pdfs/doe/2026/810o/26060941.pdf>; Res. 15/05/2026 (DOE 98, 25/05: Salvatierra de Santiago); Res. 15/07/2026 (DOE 141, 23/07: Caminomorisco). Solo Don Benito afecta a una cabecera: `locales.csv` recoge ya las fechas modificadas (no las originales 6/4 y 7/9) y cita el DOE 81.
- **Autonómicos 2026**: Decreto 40/2025, de 13 de mayo, DOE núm. 94, 19/05/2025 <https://doe.juntaex.es/pdfs/doe/2025/940o/25040070.pdf>. Art. 2: los descansos del 1/11 y 6/12 (domingos) se disfrutan el lunes 02/11/2026 y 07/12/2026; en `ccaa.csv` figuran tanto las fechas originales como los lunes.
- **Autonómicos 2027**: Decreto 119/2026, de 2 de junio, DOE núm. 108, 08/06/2026 <https://doe.juntaex.es/pdfs/doe/2026/1080o/26040142.pdf>. Art. 2: el descanso del 15/08/2027 (domingo) se disfruta el **lunes 11/10/2027**; ambas fechas en `ccaa.csv`.

## Cabeceras SIN datos y por qué

### 2027 – Extremadura (21 cabeceras, todas)
La Resolución de fiestas locales 2027 **no está publicada** en el DOE a 02/10/2026 (último DOE revisado). El Decreto 119/2026 fija el 15/09/2026 como plazo para las propuestas municipales; en 2025 la resolución salió el 23/10/2025, así que es previsible a finales de octubre de 2026. Afecta a: Almendralejo, Badajoz, Castuera, Don Benito, Fregenal de la Sierra, Herrera del Duque, Jerez de los Caballeros, Llerena, Montijo, Mérida, Olivenza, Villafranca de los Barros, Villanueva de la Serena, Zafra, Coria, Cáceres, Logrosán, Navalmoral de la Mata, Plasencia, Trujillo, Valencia de Alcántara.

### 2027 – Galicia
La Resolución consolidada del DOG (las cuatro provincias) se publica a finales de octubre/noviembre (en 2025: 30/10). Antes, cada Dirección Territorial publica en su BOP:
- **Provincia de A Coruña (12 cabeceras sin dato oficial)**: el portal del BOP (`bop.dacoruna.gal`) **no responde** desde este Mac ni desde WebFetch (`curl` → 000; `ECONNREFUSED 85.91.67.5:443`), con y sin sandbox, http y https. No he podido comprobar si la Dirección Territorial ya publicó el calendario 2027 (en 2025 fue el BOP de 30/09/2025). Sin dato: Arzúa, Betanzos, Carballo, Corcubión, Muros, Negreira, Noia, Ordes, Ortigueira, Padrón, Ribeira, Santiago de Compostela. A Coruña y Ferrol solo por prensa.
- **Provincia de Ourense (9 cabeceras)**: revisados vía API del BOP (`bop.depourense.es/portalapi/api/boletin/getFecha/AAAAMMDD`) todos los boletines del 24/08/2026 al 02/10/2026: **no publicado** todavía (en 2025 salió el 17/10/2025, edicto «Calendario laboral 2026 de la provincia de Ourense»; el método de rastreo detecta ese edicto de 2025, así que es fiable). Sin dato: A Pobra de Trives, Bande, Celanova, O Barco de Valdeorras, O Carballiño, Ourense, Ribadavia, Verín, Xinzo de Limia.
- **Provincia de Pontevedra (12 cabeceras sin dato oficial)**: revisados los sumarios diarios del BOPPO del 03/08/2026 al 02/10/2026: **no publicado** todavía (en 2025 salió el 01/10/2025 «Calendario laboral 2026», que el rastreo sí detecta). Sin dato: A Estrada, Caldas de Reis, Cambados, Cangas, Lalín, Marín, O Porriño, Ponteareas, Redondela, Tui, Vigo, Vilagarcía de Arousa. Pontevedra capital solo por prensa.

## Dudas y avisos
- Las tres cabeceras 2027 con calidad `prensa` (A Coruña, Ferrol, Pontevedra) son acuerdos municipales ya adoptados, pero pendientes de la publicación por la Xunta en BOP/DOG; conviene reverificar cuando salgan.
- Galicia 2026: no he podido rastrear el DOG en busca de correcciones de errores posteriores a la Resolución de 21/10/2025 (el DOG no ofrece búsqueda textual sencilla y se agotó el cupo de búsquedas web); el dataset de Abertos (actualizado por la Xunta) coincide con el DOG, lo que sugiere que no hay cambios para estas 45 cabeceras.
- Extremadura 2026: rastreo de modificaciones completo (sumarios DOE diarios 24/10/2025–02/10/2026); solo Don Benito afectado entre las cabeceras.
- Nombres de festividad en Galicia están en gallego (tal como los publica la fuente). En Extremadura la fuente no da nombres.
- `2025` no incluido: la fuente 2026 no lo da sin esfuerzo adicional.
- Se agotó el cupo de `WebSearch` de la sesión a mitad del trabajo; el resto se hizo con `curl`/`WebFetch` directos a boletines y portales.

## Comprobaciones
- `locales.csv` carga con `csv.DictReader`; 156 filas; todas las fechas ISO válidas (`datetime.date.fromisoformat`); `ine_municipio` de 5 dígitos tal como viene en `cabeceras.csv`; 2 festivos por cabecera y año.
- `ccaa.csv`: 51 filas (GAL 2026: 12, GAL 2027: 12, EXT 2026: 14, EXT 2027: 13).
