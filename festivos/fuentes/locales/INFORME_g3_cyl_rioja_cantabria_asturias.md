# Informe – festivos locales de las cabeceras de partido judicial (grupo CASTILLA Y LEÓN, LA RIOJA, CANTABRIA y ASTURIAS)

Fecha de elaboración: 03/10/2026. 70 cabeceras (41 CyL, 3 La Rioja, 8 Cantabria, 18 Asturias).
Ficheros: `locales.csv` (328 filas), `ccaa.csv` (96 filas), `build.py` (script que los genera), `raw/` (boletines y textos descargados).

## Recuento

| Año | Cabeceras con datos | Sin datos |
|---|---|---|
| 2025 (solo CyL, de regalo) | 41 / 70 | las 27 cabeceras de La Rioja, Cantabria y Asturias (2025 no buscado) |
| 2026 | 68 / 70 | SAHAGÚN, HARO |
| 2027 | 55 / 70 | ASTORGA, CISTIERNA, VILLABLINO, VALLADOLID, BENAVENTE, PUEBLA DE SANABRIA, TORO (CyL); las 8 de CANTABRIA |

Calidad: 318 filas `oficial`, 10 filas `prensa` (Burgos 2027, Medina del Campo 2026, Logroño/Calahorra/Haro 2027). Ninguna `ayuntamiento`.
Todas las cabeceras con datos tienen exactamente 2 festivos por año; todas las fechas son ISO válidas (`csv.DictReader` + `date.fromisoformat`).

## Fuentes usadas por comunidad

### Castilla y León
- **2025 y 2026 (oficial, datos abiertos):** dataset «Fiestas locales: Calendario de fiestas de carácter local», Junta de Castilla y León, descarga completa (15.871 registros, 2024-2026, última actualización 17/02/2026):
  https://analisis.datosabiertos.jcyl.es/explore/dataset/fiestas-locales-calendario-de-fiestas-de-caracter-local/ (export CSV en `raw/jcyl_fiestas_locales.csv`). No contiene 2027.
  Se han tomado solo las filas de la localidad principal (se descartan pedanías de Cuéllar, Almazán, El Burgo de Osma, Puebla de Sanabria y Villablino). El dataset no trae 2026 para Sahagún, Salamanca, Vitigudino ni Medina del Campo:
  - Salamanca y Vitigudino 2026: **BOP Salamanca núm. 234, 04/12/2025** (relación complementaria de la Oficina Territorial de Trabajo): https://sede.diputaciondesalamanca.gob.es/documentacion/bop/2025/20251204/BOP-SA-20251204-001.pdf (oficial).
  - Medina del Campo 2026: en el BOP Valladolid núm. 179 (19/09/2025) figura «No comunicada». Fechas (13/06 San Antonio y 02/09 San Antolín) tomadas de la crónica del Pleno de 25/09/2025 en La Voz de Medina → `prensa`.
  - Sahagún 2026: no está en la Resolución OTT León de 15/09/2025 (BOP León núm. 177, 17/09/2025) ni en el dataset; el BOP de León (bop.dipuleon.es) devuelve 403 desde esta red. **Sin datos.**
- **2027 (oficial, BOP provinciales):** en CyL las fiestas locales las fija cada Oficina Territorial de Trabajo y se publican en el BOP de la provincia, no en el BOCYL. La Junta enlaza los nueve BOP en https://trabajoyprevencion.jcyl.es/web/es/relaciones-laborales/calendario-laboral.html. Usados:
  - Ávila: BOP núm. 129, 08/07/2026, Anuncio 1448/26 (acuerdo 02/07/2026) – https://www.diputacionavila.es/bops/2026/08-07-2026/08-07-2026_144826.pdf
  - Burgos: BOP núm. 145, 04/08/2026, BOPBUR-2026-03251 – http://bopbur.diputaciondeburgos.es/sites/default/files/private/publicado/bopbur-2026-145/bopbur-2026-145-anuncio-202603251.pdf (PDF con fuentes no extraíbles: se ha OCRizado con ocrmypdf/tesseract; `raw/jcyl/burgos_ocr.txt`). **Burgos capital no figura en el anexo**; sus dos fiestas 2027 (04/06 Curpillos y 29/06 San Pedro y San Pablo) las aprobó la Junta de Gobierno Local el 10/09/2026 (BurgosConecta) → `prensa`, pendiente de resolución complementaria en BOP.
  - León: BOP núm. 144, 31/07/2026, Resolución 20/07/2026 (BOP-LE-2026-144033) – copia de la Junta: https://trabajoyprevencion.jcyl.es/web/jcyl/binarios/388/708/RESOLUCION%20Y%20LISTADO%20-%20BOP%20144-%20de%2031-07-2026.pdf (también OCRizado; `raw/jcyl/leon_ocr.txt`). **Astorga, Cistierna y Villablino no aparecen en el anexo** (municipios que no comunicaron en plazo); bop.dipuleon.es (403) impide comprobar si hay resolución complementaria posterior. Sin datos 2027.
  - Palencia: BOP núm. 83, 13/07/2026, Acuerdo 07/07/2026 – https://www.diputaciondepalencia.es/system/files/bop/2026/20260713-bop-83-Ordinario.pdf (la tabla no da nombre de festividad → «Fiesta local»).
  - Salamanca: BOP núm. 129, 08/07/2026, Acuerdo 01/07/2026 – https://sede.diputaciondesalamanca.gob.es/documentacion/bop/2026/20260708/BOP-SA-20260708-001.pdf (sin nombres).
  - Segovia: BOP núm. 80, 06/07/2026, Resolución 30/06/2026 – https://www.dipsegovia.es/documents/39512/c83b1c0d-fe99-3d65-c3ec-b1e5f998b3b6
  - Soria: BOP núm. 81, 15/07/2026 (BOPSO-81-15072026) – bop.dipsoria.es devuelve 403; usado el PDF idéntico alojado por la Junta: https://trabajoyprevencion.jcyl.es/web/jcyl/binarios/704/771/BOP%20n.%C2%BA%2081.pdf (sin nombres).
  - Valladolid: BOP núm. 129, 09/07/2026, Resolución 06/07/2026 (BOPVA-A-2026-02051) – https://trabajoyprevencion.jcyl.es/web/jcyl/binarios/569/674/Fiestas%20BOPVA-A-2026-02051.pdf. **Valladolid capital: «No comunicada»**; no se ha localizado resolución complementaria ni acuerdo municipal publicado (valladolid.es y sede.valladolid.es devuelven 403). Sin datos 2027.
  - Zamora: BOP núm. 88, 31/07/2026, corrección de errores con publicación íntegra (el original, BOP núm. 87 de 27/07/2026, tenía errores) – https://www.diputaciondezamora.es/opencms/export/sites/dipu-zamora/servicios/BOP/.Archivos/documentos/BOP/anuncios/2026/88/202601897.pdf. **Benavente, Puebla de Sanabria y Toro no figuran** en ninguna de las dos publicaciones. Sin datos 2027.
- **Autonómicos:** Decreto 9/2025, de 29 de mayo (BOCYL núm. 103, 02/06/2025; https://bocyl.jcyl.es/eli/es-cl/d/2025/05/29/9) y Decreto 7/2026, de 26 de marzo (BOCYL núm. 61, 30/03/2026; https://bocyl.jcyl.es/eli/es-cl/d/2026/03/26/7; el PDF del BOCYL daba error 500, texto obtenido por OCR de la copia de la Junta). 2026: 1 nov → lunes 2 nov, 6 dic → lunes 7 dic. 2027: 15 ago → lunes 16 ago.

### La Rioja
- **2026 (oficial):** Resolución de 14/08/2025 de la Dirección General de Trabajo y Salud Laboral, BOR núm. 159, 19/08/2025. Texto íntegro obtenido de dos reproducciones (laboral-social.com y circular FER) coincidentes; el portal del BOR (web.larioja.org, ias1.larioja.org) **no responde desde esta red** (timeout / conexión rechazada, también desde WebFetch). **Haro no figura en esa resolución**; existe un anuncio posterior del BOR (anu-571537, resolución complementaria 2026) que no se ha podido abrir → Haro 2026 sin datos.
- **2027 (prensa):** la resolución de fiestas locales 2027 está en BOR núm. 160, 21/08/2026 (enlace oficial: https://ias1.larioja.org/boletin/Bor_Boletin_visor_Servlet?referencia=41863576-1-PDF-579228, inaccesible desde esta red). Fechas de Logroño, Calahorra y Haro tomadas de nuevecuatrouno.com (21/08/2026), leído directamente → `prensa`. Conviene revalidar contra el BOR.
- **Autonómicos:** Resolución 164/2025 (BOR 12/05/2025) y Resolución 186/2026 (BOR núm. 86, 08/05/2026); listas comprobadas en https://www.larioja.org/relaciones-laborales/es/calendario-festivos-laborales-2027 (accesible solo vía navegador) y en las reproducciones de laboral-social.com.

### Cantabria
- **2026 (oficial):** Resolución de 02/12/2025 de la DG de Trabajo, Economía Social y Empleo Autónomo, BOC núm. 238, 11/12/2025 (CVE-2025-10276), con fiestas nacionales, autonómicas y locales de todos los municipios: https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob=428192. En el anexo el nombre del municipio va centrado entre sus dos filas (se ha comprobado con casos conocidos: Castro Urdiales San Pelayo/San Andrés, Reinosa San Sebastián/San Mateo).
- **2027:** la Orden IND/29/2026 (BOC núm. 135, 15/07/2026) dio a los ayuntamientos un mes para proponer; la resolución con las fiestas locales 2027 **aún no se ha publicado** (en 2025 salió el 11 de diciembre). Las 8 cabeceras cántabras quedan sin 2027.
- **Autonómicos:** Orden IND/37/2025 (BOC núm. 147, 01/08/2025, idAnuBlob=423185) y Orden IND/29/2026 (BOC núm. 135, 15/07/2026, idAnuBlob=438006). 2026: 6 dic → lunes 7 dic. 2027: 25 jul (domingo) sustituido por 28 jul; 15 ago sustituido por 15 sep (La Bien Aparecida).

### Asturias
- **2026 (oficial):** Resolución de 03/06/2025 (BOPA núm. 114, 16/06/2025, Cód. 2025-04744). **2027 (oficial):** Resolución de 22/05/2026 (BOPA núm. 110, 10/06/2026, Cód. 2026-04656). Los servidores del Principado (miprincipado.asturias.es, sede.asturias.es) **no responden desde esta red**; se han usado copias íntegras del PDF del BOPA alojadas por SPJ-USO (`raw/bopa_locales_2026_spj.pdf`, `raw/bopa_locales_2027_spj.pdf`), que conservan cabecera, paginación y código del BOPA. En el anexo el nombre del concejo va centrado entre sus filas; para concejos con festivos por parroquias (Llanes, Mieres, Piloña, Siero, Tineo, Valdés) se han tomado los dos días de ámbito general / de la capital del concejo y se indica el alcance en `festividad`.
- **Autonómicos 2026:** el Principado solo publica el decreto de sustitución (Decreto 35/2025, BOPA 24/03/2025: 8 de septiembre); la lista completa se ha tomado de la relación remitida por el Principado al Ministerio y publicada en BOE núm. 259, 28/10/2025 (BOE-A-2025-21667): incluye 2 nov y 7 dic (lunes siguientes).
- **Autonómicos 2027:** solo existe el Decreto 7/2026, de 16 de febrero (BOPA 26/02/2026: 8 de septiembre). La lista completa 2027 **no está publicada** ni por el Principado ni en el BOE (revisados los sumarios BOE 21/09–03/10/2026). En `ccaa.csv` se incluye una lista DERIVADA (nacionales + Jueves Santo + 8 sep) marcada como tal; el traslado del 15 de agosto (domingo) al lunes 16 está señalado como PENDIENTE DE CONFIRMACIÓN. Revalidar cuando salga la Resolución del BOE (habitualmente octubre-noviembre).

## Cabeceras sin datos y motivo

| Cabecera | Año | Motivo |
|---|---|---|
| Sahagún | 2026 | No está en el dataset JCyL ni en la Resolución OTT León 15/09/2025; BOP León inaccesible (403) para buscar complementaria |
| Haro | 2026 | No figura en BOR 19/08/2025; la resolución complementaria (BOR anu-571537) es inaccesible desde esta red |
| Astorga, Cistierna, Villablino | 2027 | No figuran en el anexo del BOP León 144 (31/07/2026); BOP León inaccesible para comprobar complementaria |
| Valladolid | 2027 | «No comunicada» en BOP Valladolid 129 (09/07/2026); sin publicación posterior localizada |
| Benavente, Puebla de Sanabria, Toro | 2027 | No figuran en BOP Zamora 87 ni en la corrección íntegra del BOP 88 |
| Castro-Urdiales, Laredo, Medio Cudeyo, Reinosa, San Vicente de la Barquera, Santander, Santoña, Torrelavega | 2027 | Cantabria aún no ha publicado la resolución de fiestas locales 2027 (prevista ~diciembre 2026) |

## Dudas / avisos
- Filas `prensa` (10): Burgos 2027, Medina del Campo 2026, Logroño/Calahorra/Haro 2027. Son fechas leídas directamente en el medio citado, no en boletín.
- Soria 2027: el PDF usado es la copia que la Junta aloja del BOP núm. 81; no se ha podido abrir el original en bop.dipsoria.es (403). Se marca `oficial` por ser el propio boletín.
- Piedrahíta 2027: el BOP Ávila dice «17 de mayo y 13 de septiembre. FIESTA DE LA VEGA»; se ha asignado «Fiesta de la Vega» al 17 de mayo (la romería de la Vega es en mayo, como en 2026) y «Fiesta local» al 13 de septiembre.
- Palencia, Salamanca, Soria, Valladolid 2027: los anexos no indican el nombre de la festividad → «Fiesta local».
- Castropol 2026: el BOPA no da nombre (27/07 y 07/09).
- Dataset JCyL 2026: Ávila figura 02/05/2026 (San Segundo cae en sábado 2 de mayo); Cuéllar 13/04 y 25/09.
- Castilla y León 2025: se incluyen tal cual los festivos del dataset JCyL para las 41 cabeceras de la comunidad (fuente oficial, sin contraste con BOP).
- URL inaccesibles desde esta red (documentadas): web.larioja.org, ias1.larioja.org (timeout/ECONNREFUSED), miprincipado.asturias.es, sede.asturias.es, www.asturias.es (sin respuesta), bop.dipuleon.es (403), bop.dipsoria.es (403), valladolid.es y sede.valladolid.es (403), larioja.org (403 a curl/WebFetch; accesible desde el panel de navegador), nuevecuatrouno.com (403 a curl; accesible desde el navegador), bocyl.jcyl.es PDFs de disposiciones (error 500; ELI accesible).
