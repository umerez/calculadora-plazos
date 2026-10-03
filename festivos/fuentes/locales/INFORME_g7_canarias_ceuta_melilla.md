# INFORME – Grupo 7: CANARIAS, CEUTA y MELILLA (21 cabeceras de partido judicial)

Fecha de elaboración: 03/10/2026. Ficheros: `locales.csv` (84 filas), `ccaa.csv` (92 filas). Textos fuente descargados en `raw/`.

## Recuento

| | Cabeceras con 2026 | Cabeceras con 2027 | Sin datos |
|---|---|---|---|
| CANARIAS (19) | 19 | 19 | 0 |
| CEUTA (1) | 1 | 1 (calidad `prensa`, ver abajo) | 0 |
| MELILLA (1) | 1 | 1 | 0 |
| **Total (21)** | **21** | **21** | **0** |

Todas las filas son `oficial` salvo las 2 de CEUTA 2027 (`prensa`). 2025 no se ha incluido (no lo daba la misma fuente sin trabajo adicional).

## Fuentes por comunidad

### CANARIAS
Fuente 2 (boletín oficial). No existe dataset de fiestas locales en datos.canarias.es / opendata.gobiernodecanarias.org (buscado; solo hay «Agenda cultural»).

- **Fiestas locales 2026**: ORDEN de 6 de agosto de 2025, por la que se determinan las fiestas locales propias de cada municipio de la CAC para el año 2026. BOC núm. 165, jueves 21/08/2025, anuncio 3029 (BOC-A-2025-165-3029). <https://www.gobiernodecanarias.org/boc/2025/165/3029.html>
- **Fiestas locales 2027**: ORDEN de 7 de agosto de 2026 (fiestas locales 2027). BOC núm. 168, viernes 21/08/2026, anuncio 3035 (BOC-A-2026-168-3035). <https://www.gobiernodecanarias.org/boc/2026/168/3035.html>
- **Calendario autonómico 2026**: DECRETO 61/2025, de 28 de abril. BOC núm. 88, 05/05/2025, anuncio 1659. <https://www.gobiernodecanarias.org/boc/2025/088/1659.html>
- **Calendario autonómico 2027**: DECRETO 115/2026, de 29 de junio. BOC núm. 133, 03/07/2026, anuncio 2334. <https://www.gobiernodecanarias.org/boc/2026/133/2334.html>

Se ha trabajado sobre la versión HTML del BOC (el propio BOC advierte que la versión oficial es el PDF con el mismo código BOC-A-…; el contenido es idéntico). Los anexos se han parseado con script (`build.py`) y se han extraído las 19 cabeceras; todos los nombres de festividad son los literales del BOC.

Festivos insulares (en `ccaa.csv`, con el nombre de la isla en `festividad`): El Hierro 24/09; Fuerteventura 18/09/2026 y 17/09/2027; Gran Canaria 08/09; La Gomera 05/10/2026 y 04/10/2027; La Palma 05/08; Lanzarote y La Graciosa 15/09; Tenerife 02/02. Sustituyen a Santiago Apóstol (25 de julio). Isla de cada cabecera: Arrecife = Lanzarote; Puerto del Rosario = Fuerteventura; Arucas, Las Palmas de GC, San Bartolomé de Tirajana, Santa María de Guía, Telde = Gran Canaria; Arona, Granadilla, Güímar, Icod, La Orotava, Puerto de la Cruz, La Laguna, Santa Cruz de Tenerife = Tenerife; Los Llanos de Aridane, Santa Cruz de La Palma = La Palma; San Sebastián de la Gomera = La Gomera; Valverde = El Hierro.

Observaciones Canarias:
- 2026: el Decreto 61/2025 fija el 30 de mayo (Día de Canarias) en sustitución del descanso del lunes 7 de diciembre (6/12 cae en domingo); Todos los Santos se traslada al lunes 2 de noviembre. 2027: el 16 de agosto es descanso por caer la Asunción en domingo.
- Santa María de Guía aparece en el anexo 2026 como «SANTA MARÍA DE GUÍA» y en 2027 como «SANTA MARÍA DE GUÍA DE GRAN CANARIA»; se ha mapeado al INE 35023.
- Santa Cruz de Tenerife e Icod de los Vinos fijan en 2027 el Martes de Carnaval el 23 de febrero (no el 9), tal como publica el BOC; se respeta el literal.
- Puerto de la Cruz 2026: 13 y 14 de julio (Gran Poder de Dios y Virgen del Carmen), según BOC.

### CEUTA
- **2026 (oficial)**: BOCCE núm. 6.551, viernes 26/09/2025, anuncio 591: relación de festivos 2026 conforme al Decreto de la Presidencia de 29/08/2025 (calendario de fiestas laborales 2026) y a la Resolución de 15/09/2025 de la Delegación del Gobierno en Ceuta (fiestas locales 2026). PDF: <https://www.ceuta.es/ceuta/component/jdownloads/finish/1960-septiembre/22934-bocce-6551-26-09-2025?Itemid=0>. El BOCCE publica los 14 festivos sin separar los locales; la identificación de los dos locales (20/03 Eidul Fitr y 13/06 San Antonio) procede de la nota oficial de la Ciudad sobre el Pleno de la Asamblea de 04/09/2025: <https://www.ceuta.es/gobiernodeceuta/index.php/noticia/42-presidencia/13794-el-pleno-de-la-asamblea-aprueba-el-calendario-laboral-para-2026-recuperando-como-festivo-el-dia-de-ceuta>.
- **2027 (prensa, NO verificado en boletín)**: el Pleno de la Asamblea aprobó el 29/09/2026 las dos fiestas locales 2027: 10 de marzo (Eid al-Fitr) y 2 de septiembre (Día de Ceuta). A 03/10/2026 NO está publicado en el BOCCE: revisados BOCCE 6.656 (29/09/2026) y 6.657 (02/10/2026), sin el decreto/relación de festivos 2027. Fuentes de prensa coincidentes: RTVCE <https://www.rtvce.es/actualidad/politica/dia-ceuta-volvera-ser-laborable-2027/20260929114256103472.html>, Ceuta al Día <https://www.ceutaldia.com/articulo/administracion/pleno-aprueba-festivos-locales-asi-queda-configurado-calendario-laboral-2027/20260929082712321772.html>, Ceuta Ahora <https://ceutaahora.com/art/23072/...>. **Discrepancia**: El Faro de Ceuta (<https://elfarodeceuta.es/aprobado-calendario-laboral-2027-ceuta/>) dice que los locales son 5 de agosto y 2 de septiembre; las otras tres fuentes (incluida la televisión pública RTVCE, que cita literalmente el acuerdo) dicen 10 de marzo y 2 de septiembre, coherente con el esquema de 2026 (Eid al-Fitr como local; Ntra. Sra. de África y Eidul Adha como sustituciones autonómicas de San José y del lunes posterior a la Asunción). Se ha consignado 10/03 y 02/09 con `calidad=prensa`. **Conviene reverificar cuando salga el BOCCE (previsiblemente octubre 2026)**. El calendario completo 2027 de Ceuta en `ccaa.csv` tiene la misma salvedad.
- Nota: no es necesario filtrar: en Ceuta el 13/06/2027 (San Antonio) cae en domingo y no es festivo laboral en 2027.

### MELILLA
- **2026 (oficial)**: BOME núm. 6315, viernes 03/10/2025, artículo 1033: Acuerdo del Consejo de Gobierno de 19/09/2025 relativo al Calendario Laboral 2026. PDF: <https://bomemelilla.es/bome/descargar/BOME-A-2025-1033.pdf>. Locales: 8 de septiembre (Ntra. Sra. Virgen de la Victoria) y 17 de septiembre (Día de Melilla). El 27/05 (Aid Al Adha) sustituye al 19/03 (San José). El 07/12 es lunes siguiente al Día de la Constitución.
- **2027 (oficial)**: BOME Extraordinario núm. 43, miércoles 30/09/2026, artículo 108: Acuerdo del Consejo de Gobierno de 24/09/2026, aprobación del Calendario Laboral 2027. PDF: <https://bomemelilla.es/bome/descargar/BOME-AX-2026-108.pdf>. Locales: 8 y 17 de septiembre. El 17/05 (Aid Al Adha) sustituye al 19/03 (San José). También publicado en <https://www.melilla.es/melillaportal/contenedor.jsp?seccion=s_fact_d4_v1.jsp&contenido=46179&nivel=1400&tipo=2>.

## Cabeceras sin datos
Ninguna. (CEUTA 2027 está incluida pero con `calidad=prensa`; si solo se admiten boletines, excluir esas 2 filas y las 14 de CEUTA 2027 en `ccaa.csv`.)

## Red / incidencias
Sin incidencias: gobiernodecanarias.org, ceuta.es (jdownloads) y bomemelilla.es respondieron desde el sandbox. El buscador de bomemelilla.es no filtra por texto vía GET; se localizó el artículo 2027 a través de la ficha «Calendario Laboral 2027» de melilla.es.

## Comprobaciones
`locales.csv` y `ccaa.csv` cargan con `csv.DictReader`; todas las fechas pasan `datetime.date.fromisoformat`. 21 cabeceras con 2 festivos en 2026 y 2 en 2027 (84 filas).
