# INFORME – Grupo G6: Comunidad de Madrid, Castilla-La Mancha, Aragón y Navarra (73 cabeceras)

Fecha de elaboración: 03/10/2026. Ficheros generados en esta carpeta: `locales.csv` (293 filas), `ccaa.csv` (122 filas), `build.py` (script reproducible; descargas en `raw/`).

## Recuento

| Año | Cabeceras con festivos locales | Observaciones |
|---|---|---|
| 2025 | 73 / 73 | Completo (Almadén solo con 1 fecha, ver dudas) |
| 2026 | 73 / 73 | Completo, 146 fechas, todas de boletín o datos abiertos (calidad `oficial`) |
| 2027 | 6 / 73 | Solo Madrid capital (calidad `prensa`, acuerdo de Pleno) y las 5 cabeceras navarras con **una sola** de sus dos fiestas locales (3 de diciembre, fijada oficialmente por la Comunidad Foral). Las otras 67 cabeceras: sin publicación oficial todavía |

Festivos autonómicos (`ccaa.csv`): 2027 de las cuatro comunidades (oficial, boletín), 2026 de las cuatro, y 2025 de Madrid y Aragón (los daba la misma fuente).

**Importante sobre 2027:** a 03/10/2026 ninguna de las cuatro comunidades ha publicado la relación de fiestas locales 2027. Los plazos de comunicación de los ayuntamientos están abiertos (Aragón: hasta 15/10/2026 según Decreto 163/2026; Navarra: hasta 15/11/2026 según Resolución 232/2026; Madrid y Castilla-La Mancha publican habitualmente en diciembre: BOCM 12/12/2025 y DOCM 12/12/2025 para 2026). Habrá que repetir la consulta en diciembre de 2026 / enero de 2027.

## Fuentes por comunidad

### Comunidad de Madrid (21 cabeceras)
- **Locales 2026**: BOCM núm. 296, 12/12/2025 – Resolución de 2 de diciembre de 2025, de la Dirección General de Trabajo, fiestas laborales de ámbito local 2026: https://www.bocm.es/boletin/CM_Orden_BOCM/2025/12/12/BOCM-20251212-34.PDF. Contrastado con el dataset de datos abiertos «Festivos regionales y locales año en curso» (festivos_locales.csv, actualizado 13/01/2026): https://datos.comunidad.madrid/catalogo/dataset/festivos_regionales_locales (coinciden las 20 cabeceras que figuran en ambos).
- **Modificación 2026**: BOCM núm. 309, 29/12/2025 – Resolución de 15 de diciembre de 2025 (modificación parcial): https://www.bocm.es/boletin/CM_Orden_BOCM/2025/12/29/BOCM-20251229-19.PDF. Afecta a dos cabeceras: **Torrelaguna** (figuraba «no comunicado por el Ayuntamiento» el 12/12/2025 y no está en el dataset; se fija 7 y 8 de septiembre) y **Coslada** (pasa de 15 de mayo y 8 de junio a **15 de mayo y 15 de junio**). Ojo: el dataset de datos abiertos NO recoge la modificación de Coslada (sigue con 8 de junio); en `locales.csv` va la fecha del BOCM de 29/12/2025.
- **Locales 2025**: dataset «Festivos regionales y locales histórico» (festivos_locales_historicos.csv, 1998-2025): https://datos.comunidad.madrid/catalogo/dataset/festivos_regionales_locales_historico (Resolución publicada en BOCM 13/12/2024, BOCM-20241213-23, y modificación BOCM 27/12/2024; no se han re-verificado contra el PDF).
- **Locales 2027**: no publicadas. Solo **Madrid capital**: acuerdo del Pleno ordinario de 29/09/2026 (unanimidad), 15 de mayo (San Isidro, sábado) y 9 de noviembre (Almudena, martes). Fuente: eldiario.es 29/09/2026 (https://www.eldiario.es/madrid/somos/ayuntamiento-madrid-aprueba-festivos-locales-2027-caeran-sabado-martes_1_13546052.html) y moncloa.com 30/09/2026; calidad `prensa`. No se ha podido localizar la nota oficial en madrid.es / diario.madrid.es (el servidor devuelve 403 a las consultas automatizadas y la búsqueda del portal no la devolvió). Fuenlabrada 2027 (14 de septiembre y 9 de marzo según madrid365.es 02/10/2026) NO se incluye: el artículo no pudo descargarse (403) y la fecha solo consta en un resumen de buscador.
- **Autonómicos**: 2027 – BOCM núm. 234, 01/10/2026, Decreto 82/2026, de 30 de septiembre (https://www.bocm.es/boletin/CM_Orden_BOCM/2026/10/01/BOCM-20261001-19.PDF). 2026 – BOCM núm. 228, 25/09/2025, Decreto 75/2025 (https://www.bocm.es/boletin/CM_Orden_BOCM/2025/09/25/BOCM-20250925-16.PDF) y dataset festivos_regionales.csv. 2025 – dataset histórico.

### Castilla-La Mancha (31 cabeceras)
- **Locales 2026**: DOCM núm. 240, 12/12/2025 – Anuncio de 04/12/2025 de la DG de Autónomos, Trabajo y Economía Social [2025/9468], relación de fiestas de carácter local 2026: https://docm.jccm.es/docm/descargarArchivo.do?ruta=2025/12/12/pdf/2025_9468.pdf&tipo=rutaDocm (PDF, 10 páginas, extraído con pdftotext; las 31 cabeceras localizadas, 2 fechas cada una). No se ha podido comprobar si existe un anuncio de modificación posterior para 2026 (en 2025 lo hubo: DOCM 19/02/2025 [2025/1159]; se agotó la cuota de búsqueda web antes de comprobarlo para 2026). Ninguna cabecera estaba afectada en la modificación de 2025.
- **Locales 2025**: DOCM núm. 242, 16/12/2024 – Anuncio de 09/12/2024 [2024/9927]: https://docm.jccm.es/docm/descargarArchivo.do?ruta=2024/12/16/pdf/2024_9927.pdf&tipo=rutaDocm; coincide con el XLSX del portal de datos abiertos «Calendario de fiestas de carácter local… 2025» (https://datosabiertos.castillalamancha.es/dataset/calendario-de-fiestas-de-car%C3%A1cter-local-retribuidas-y-no-recuperables-para-el-a%C3%B1o-2025-de). Modificación DOCM 19/02/2025 [2025/1159] revisada: no afecta a cabeceras.
- **Portal de datos abiertos**: la API CKAN no responde en JSON y el buscador devuelve 404; no se encontró dataset de fiestas locales 2026 (solo el de 2025). Se ha usado el DOCM directamente.
- **Locales 2027**: no publicadas (habitualmente en diciembre).
- **Autonómicos**: 2027 – DOCM núm. 131, 13/07/2026, Decreto 34/2026, de 23 de junio [2026/5228] (https://docm.jccm.es/docm/descargarArchivo.do?ruta=2026/07/13/pdf/2026_5228.pdf&tipo=rutaDocm): 27 de mayo (Corpus, sustituye a San José) y 31 de mayo (Día de CLM, sustituye a la Asunción, domingo). 2026 – DOCM núm. 121, 26/06/2025, Decreto 44/2025 [2025/5159].

### Aragón (16 cabeceras)
- **Locales 2026**: dataset opendata.aragon.es «Calendario de festivos en comunidad de Aragón 2026» (festivos_aragon_2026_completo.csv, con código INE; actualizado 05/05/2026): https://opendata.aragon.es/datos/catalogo/dataset/calendario-de-festivos-en-comunidad-de-aragon-2026. El dataset recoge la Resolución de 4/11/2025 del DG de Trabajo (BOA núm. 225, 20/11/2025: https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1421874360606) y la Resolución complementaria de 10/03/2026 (BOA núm. 56, 23/03/2026: https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1440857030505). Las 16 cabeceras verificadas contra el texto del BOA: 15 en la Resolución de noviembre y **Calamocha** solo en la complementaria de marzo (17 y 18 de agosto). Nombres de festividad tomados del dataset cuando constan.
- **Locales 2025**: dataset opendata.aragon.es «Calendario de festivos en comunidad de Aragón 2025» (ficheros provinciales hu/te/za de festivos locales): https://opendata.aragon.es/datos/catalogo/dataset/calendario-de-festivos-en-comunidad-de-aragon-2025. Los XLS de Huesca y Teruel se convirtieron con LibreOffice; no se han contrastado con el BOA de 2024.
- **Locales 2027**: no publicadas (plazo de propuesta de los ayuntamientos hasta 15/10/2026, art. tercero del Decreto 163/2026).
- **Autonómicos**: 2027 – BOA núm. 180, 16/09/2026, Decreto 163/2026, de 9 de septiembre (https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1466225130707): Asunción trasladada al lunes 16 de agosto. 2026 – BOA núm. 135, 16/07/2025, Decreto 70/2025 (https://www.boa.aragon.es/cgi-bin/EBOA/BRSCGI?CMD=VEROBJ&MLKOB=1403827540808) y dataset festivos_aragon_2026_ccaa.csv. 2025 – fichero ar-open-data-festivos-comunidad-2025.xls del dataset 2025.

### Navarra (5 cabeceras)
- Esquema navarro: la Comunidad fija como «fiesta local» común a todo el territorio el 3 de diciembre (San Francisco Javier, art. 46 RD 2001/1983) y cada ayuntamiento propone la otra. Por eso en `locales.csv` cada cabecera navarra lleva, además de su fiesta municipal, una fila con el 3 de diciembre (2026 y 2027) marcada como «fiesta local común a toda Navarra»; el 3 de diciembre figura también en `ccaa.csv` tal como lo publica la Comunidad. Filtrar según convenga.
- **Locales 2026**: BON núm. 241, 02/12/2025 – Resolución 682/2025, de 17 de noviembre, del DG de Economía Social y Trabajo (https://bon.navarra.es/es/anuncio/-/texto/2025/241/12). Modificación: Resolución 765/2025, de 22 de diciembre (BON núm. 1, 02/01/2026, https://bon.navarra.es/es/anuncio/-/texto/2026/1/25): solo afecta a Aranguren y concejos, Bera y Cadreita; ninguna cabecera. Pamplona 30/11/2026 (San Saturnino, 29 de noviembre, cae en domingo y se traslada al lunes) y Tudela 27/07/2026 (Santa Ana, 26, domingo) ya figuran trasladados en el propio BON.
- **Locales 2025**: BON núm. 260, 24/12/2024 – Resolución 901/2024, de 11 de diciembre (https://bon.navarra.es/es/anuncio/-/texto/2024/260/4).
- **Locales 2027**: solo el 3 de diciembre (Resolución 232/2026). La fiesta municipal 2027 se publicará tras el 15/11/2026; la Resolución 232/2026 advierte que, si el ayuntamiento no comunica, se mantendrá la de 2026 (trasladada si cae en domingo/festivo). No se incluye esa previsión en el CSV por no ser aún oficial.
- **Autonómicos**: 2027 – BON núm. 103, 28/05/2026, Resolución 232/2026, de 13 de mayo (https://bon.navarra.es/es/anuncio/-/texto/2026/103/23). 2026 – BON núm. 129, 30/06/2025, Resolución 390/2025, de 5 de junio (https://bon.navarra.es/es/anuncio/-/texto/2025/129/11).
- **Portal de datos abiertos** datos.navarra.es: no resuelve DNS desde este Mac (ni con sandbox desactivado ni vía WebFetch: `getaddrinfo ENOTFOUND datos.navarra.es`); gobiernoabierto.navarra.es devuelve 404 para la ruta probada. Se ha usado el BON directamente, que sí responde.

## Cabeceras sin datos
- **2025 y 2026**: ninguna.
- **2027**: las 67 cabeceras distintas de Madrid capital y de las 5 navarras (y estas últimas solo parcialmente). Motivo: ninguna comunidad ha publicado aún la relación de fiestas locales 2027.

## Dudas y avisos
1. **Almadén 2025**: el DOCM [2024/9927] y el XLSX del portal dicen literalmente «25 de julio y de septiembre» (falta el día de septiembre). Solo se incluye 2025-07-25; la segunda fiesta de 2025 queda sin fecha. En 2026 Almadén tiene 27 de julio y 14 de septiembre.
2. **Coslada 2026**: discrepancia dataset (8 de junio) vs. BOCM 29/12/2025 (15 de junio). Se ha seguido el BOCM.
3. **Madrid capital 2027**: calidad `prensa` (acuerdo plenario confirmado por varios medios, pendiente de Resolución de la DG de Trabajo en BOCM).
4. **Fechas en sábado/domingo**: se dejan tal como las publica la fuente (p. ej. Daroca 07/03/2026 sábado, Barbastro 21/06/2025 sábado, Fuenlabrada 26/12/2026 sábado). El encargo pide la fecha del lunes solo cuando la fuente dice expresamente que se traslada; en Navarra el BON ya publica la fecha trasladada.
5. **Nombres de festividad**: solo Aragón (dataset/BOA) y los casos de Navarra/Madrid 2027 los dan; en el resto se ha puesto «Fiesta local».
6. No se ha comprobado la existencia de un anuncio de modificación del DOCM para las fiestas locales 2026 ni de correcciones de errores en el BOA 2026 posteriores al 23/03/2026 (cuota de búsqueda web agotada). Para las cabeceras, los datos del BOA de marzo de 2026 coinciden con el dataset actualizado el 05/05/2026.
7. Comprobación final: `locales.csv` y `ccaa.csv` cargan con `csv.DictReader` y todas las fechas validan con `datetime.date.fromisoformat` (hecho en `build.py`).
