# INFORME – Grupo g2 ANDALUCÍA (85 cabeceras de partido judicial)

Fecha de elaboración: 2026-10-03.

## Recuento

| Concepto | Resultado |
|---|---|
| Cabeceras en `cabeceras.csv` | 85 |
| Cabeceras con festivos locales **2026** | **85** (170 filas en `locales.csv`, 2 por cabecera) |
| Cabeceras con festivos locales **2027** | **0** – la Resolución de fiestas locales 2027 **aún no está publicada** (ver abajo) |
| Cabeceras sin datos 2026 | 0 |
| Festivos autonómicos en `ccaa.csv` | 12 de 2026 + 12 de 2027 (calendario completo del Decreto, incluidos los estatales y los trasladados) |

Todas las filas de `locales.csv` llevan `calidad = oficial` (BOJA, contrastado con el dataset de datos abiertos de la Junta).
`festividad` = «Fiesta local» en todas las filas: ni la Resolución del BOJA ni el dataset dan el nombre de la festividad, solo la fecha.

## Fuentes usadas (Andalucía)

### Festivos locales 2026
1. **BOJA núm. 197, 14/10/2025 – Resolución de 6 de octubre de 2025, de la Dirección General de Trabajo, Seguridad y Salud Laboral, por la que se publica la relación de fiestas locales de los municipios de la Comunidad Autónoma de Andalucía para el año 2026.**
   PDF: https://www.juntadeandalucia.es/boja/2025/197/BOJA25-197-00016-13517-01_00327114.pdf (ficha: https://www.juntadeandalucia.es/boja/2025/197/28). Texto extraído con `pdftotext -layout`; 757 municipios parseados del anexo.
2. **BOJA núm. 247, 26/12/2025 – Resolución de 18 de diciembre de 2025** (modifica la anterior): corrige **Coín** (3 de mayo → **4 de mayo**; 1 de junio se mantiene) e incluye municipios comunicados tarde, entre ellos la cabecera **La Carolina** (15 de mayo y 24 de noviembre), que no figuraba en la Resolución de 6/10/2025.
   PDF: https://www.juntadeandalucia.es/boja/2025/247/BOJA25-247-00002-17289-01_00330886.pdf
3. **BOJA núm. 32, 17/02/2026 – Corrección de errores** de la Resolución de 6/10/2025: solo afecta a Guarromán (no es cabecera).
   PDF: https://www.juntadeandalucia.es/boja/2026/32/BOJA26-032-00001-2090-01_00333315.pdf
4. **BOJA núm. 33, 18/02/2026 – Resolución de 12 de febrero de 2026**: modifica **Loja** (segundo festivo 29 de agosto → **4 de septiembre**).
   PDF: https://www.juntadeandalucia.es/boja/2026/33/BOJA26-033-00001-2142-01_00333367.pdf
5. **Datos abiertos de la Junta – «Calendario de días festivos en la Comunidad Autónoma de Andalucía»** (Consejería de Empleo, Empresa y Trabajo Autónomo), API `work-calendar`:
   ficha https://www.juntadeandalucia.es/datosabiertos/portal/dataset/calendario-de-dias-inhabiles-en-la-comunidad-autonoma-de-andalucia ; descarga completa https://datos.juntadeandalucia.es/api/v0/work-calendar/all?format=csv (descargado el 03/10/2026; 5.856 registros, años 2023-2027; 1.548 festivos LOCAL de 2026 para 774 municipios).
   Se usó como **contraste**: para las 85 cabeceras, las fechas del dataset coinciden al 100 % con el BOJA ya consolidado (incluye las modificaciones de Coín, La Carolina y Loja). Sin discrepancias.

   En `locales.csv` la columna `fuente`/`url` apunta a la Resolución del BOJA (y, para Coín, La Carolina y Loja, a la Resolución modificativa correspondiente), por ser la fuente con valor normativo.

   La página de la Consejería que enlaza todo lo anterior: https://www.juntadeandalucia.es/organismos/empleoempresaytrabajoautonomo/areas/relaciones-laborales/calendario-fiestas.html (consultada el 03/10/2026).

### Festivos autonómicos
- **2026**: BOJA núm. 93, 19/05/2025 – **Decreto 101/2025, de 14 de mayo**. PDF: https://www.juntadeandalucia.es/boja/2025/93/BOJA25-093-00002-6889-01_00320489.pdf. Traslados fijados por la Junta: Todos los Santos → lunes 2/11/2026; Constitución → lunes 7/12/2026. El 28/02/2026 (sábado) y el 15/08/2026 (sábado) se mantienen en sábado.
- **2027**: BOJA núm. 84, 05/05/2026 – **Decreto 84/2026, de 29 de abril**. PDF: https://www.juntadeandalucia.es/boja/2026/84/BOJA26-084-00002-5812-01_00337048.pdf. Traslados fijados por la Junta: Día de Andalucía (domingo 28/02) → lunes **1/03/2027**; Asunción (domingo 15/08) → lunes **16/08/2027**. El 1/05/2027 y el 25/12/2027 caen en sábado y no se trasladan.
- Ambos calendarios coinciden exactamente con los 12 registros `LABORAL` de cada año en el dataset de datos abiertos.

## Festivos locales 2027: NO publicados (verificado)

- El Decreto 84/2026 (BOJA 05/05/2026) da a los ayuntamientos 2 meses (hasta ~5/07/2026) para comunicar sus propuestas; la Dirección General de Trabajo publica después la Resolución con la relación completa. En 2025 esa Resolución (para 2026) se firmó el 6/10 y se publicó el **14/10/2025**; en 2024 (para 2025) fue la Resolución de 4/10/2024. Es previsible que la de 2027 aparezca en el BOJA a **mediados de octubre de 2026**, con una Resolución modificativa (municipios rezagados y correcciones) en diciembre de 2026 / febrero de 2027.
- Comprobaciones hechas el 03/10/2026:
  - El dataset de datos abiertos (`option-values/years`) tiene 2027 con **solo 12 registros**, todos `LABORAL`; **0 registros `LOCAL`** de 2027.
  - La página de la Consejería «Calendario laboral y fiestas locales» solo enlaza, para 2027, el Decreto 84/2026; ninguna Resolución de fiestas locales.
  - Sumarios BOJA 2026 núms. 180-192 (últimos publicados, hasta el 28-30/09/2026; el 193 devuelve 404): sin referencias a «fiestas locales» (los sumarios HTML del portal cargan parcialmente, así que esta comprobación es solo indicativa).
  - Búsquedas web: ninguna referencia a una Resolución de fiestas locales 2027 de Andalucía.
- **Qué hacer cuando salga**: la URL de la ficha será `https://www.juntadeandalucia.es/boja/2026/<núm>/<orden>` y el dataset `work-calendar/all?format=csv` se actualizará con `type=LOCAL, year=2027`. El script `src/build.py` de esta carpeta puede reutilizarse: basta añadir el nuevo PDF al parser (`src/parse2026.py`) o leer directamente el CSV del dataset.

## Cabeceras SIN datos

- 2026: ninguna.
- 2027: las 85 (por no estar publicada la fuente oficial; no se ha recurrido a webs municipales ni prensa para 2027 porque los plenos solo han aprobado propuestas pendientes de ratificación por la autoridad laboral, y el encargo pide no inventar).

## Dudas y avisos

- **Nombres**: `cabeceras.csv` trae «LORA DEL RIO» (sin tilde) y formas con artículo delante («EL EJIDO», «LA LÍNEA DE LA CONCEPCIÓN», «EL PUERTO DE SANTA MARÍA», «LA CAROLINA», «LA PALMA DEL CONDADO»); el BOJA usa «LORA DEL RÍO», «EJIDO, EL», «CAROLINA, LA», etc., y «VÉLEZ RUBIO» sin guion. El cruce se hizo normalizando (acentos, guiones, artículo pospuesto) y se comprobó que las 85 cabeceras casan de forma única. En `locales.csv` se conserva el nombre tal como viene en `cabeceras.csv`.
- **Festivos locales que caen en sábado en 2026** (se incluyen igualmente, como pide el encargo): Almería 29/08, Córdoba 24/10, Puente Genil 25/04, Loja 25/04, Valverde del Camino 12/09, Ronda 24/01, Lebrija 12/09. Ninguno cae en domingo. No se ha filtrado nada.
- **Coincidencias con festivos estatales/autonómicos**: ninguna cabecera tiene festivo local coincidente con los 12 del Decreto 101/2025 según el cruce, pero no se ha filtrado nada en todo caso.
- **2025**: el dataset de datos abiertos contiene también los locales de 2025 (1.530 registros), pero no se han volcado a `locales.csv` porque el encargo prioriza 2026/2027; están en `src/work_calendar_all.csv` por si se quieren.
- Red: `https://www.juntadeandalucia.es/boja/2026/84/1` devolvió `000` dentro del sandbox; con `dangerouslyDisableSandbox` funcionó. `WebFetch` a `boja/2026/192/index.html` dio ECONNRESET (irrelevante para el resultado).

## Archivos de trabajo (`src/`)

- `locales2026_res.pdf/.txt`, `locales2026_mod1.*`, `locales2026_corr.*`, `locales2026_mod2.*`: BOJA descargados y texto extraído.
- `decreto2026.*`, `decreto2027.*`: Decretos de fiestas laborales.
- `work_calendar_all.csv`: volcado completo del dataset de datos abiertos (03/10/2026); `work_calendar_openapi.json`: especificación de la API.
- `parse2026.py` (anexo BOJA → `locales2026_boja.json`, con modificaciones aplicadas) y `build.py` (cruce con cabeceras, generación de `locales.csv` y `ccaa.csv`, contraste con dataset).
