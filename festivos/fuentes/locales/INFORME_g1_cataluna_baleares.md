# Grupo g1 – CATALUÑA e ILLES BALEARS: festivos locales de las 55 cabeceras de partido judicial

Fecha de elaboración: 03/10/2026. Ficheros: `locales.csv` (234 filas), `ccaa.csv` (50 filas). Documentos fuente descargados en `raw/` (PDF + texto extraído) y script reproducible `build.py`.

## Recuento

| | Cabeceras | Con 2026 | Con 2027 | Con 2025 (extra) |
|---|---|---|---|---|
| Cataluña | 49 | 48 (oficial) | 9 (0 oficial; 7 ayuntamiento, 2 prensa) | 48 (oficial) |
| Illes Balears | 6 | 6 (oficial) | 6 (oficial) | 0 |
| **Total** | **55** | **54** | **15** | **48** |

Festivos autonómicos (`ccaa.csv`): Cataluña 2026 (12 + Festa d'Aran) y 2027 (12 + Festa d'Aran); Illes Balears 2026 (12) y 2027 (12).

## Fuentes usadas

### Cataluña

1. **Festivos locales 2025 y 2026 (oficial)** – Portal de datos abiertos de la Generalitat, dataset Socrata «Calendari de festes locals a Catalunya» (id `b4eh-r8up`, actualizado 10/04/2026).
   URL: https://analisi.transparenciacatalunya.cat/Treball/Calendari-de-festes-locals-a-Catalunya/b4eh-r8up
   Descarga usada: `https://analisi.transparenciacatalunya.cat/resource/b4eh-r8up.csv?$where=any_calendari in (2025,2026,2027)&$limit=50000` (17.923 filas; el dataset **no contiene 2027**, años disponibles 2012-2026).
   - Filtrado: `festiu = 'Festiu local'`, núcleo principal (`pedania = 000`). Para **Vielha e Mijaran** el dataset no tiene núcleo `000` (sólo pueblos del municipio): se ha tomado el núcleo **Vielha** (pedania 011): 08/09/2026 y 08/10/2026. Para Puigcerdà, Cervera, Lleida, Tortosa y Valls se han descartado las pedanías (Age, Raimat, Sucs, Bítem, Campredó, Picamoixons…).
   - **Contraste con el DOGC**: se descargó la *Ordre EMT/208/2025, d'11 de desembre* (festes locals 2026; DOGC núm. 9565, 17/12/2025; PDF `raw/dogc_emt208_2025_locals2026.pdf`, URL https://portaldogc.gencat.cat/utilsEADOP/AppJava/PdfProviderServlet?documentId=1032232&type=01&language=ca_ES) y la *Ordre EMT/3/2026, de 14 de gener* de modificación (DOGC núm. 9586, 20/01/2026; documentId=1034587). Las 48 cabeceras con datos coinciden exactamente entre dataset y DOGC. La modificación de enero afecta a Cardona, Viladecans, Sant Joan Despí, Castelldefels, Sitges, Tordera, Balenyà, Tavèrnoles, Torà y Polinyà: ninguna cabecera.
   - Los datos de **2025** del dataset vienen mezclados con filas basura («C. A. de Catalunya», «null», festivos autonómicos); se han filtrado y se han incluido sólo las cabeceras que quedaban con exactamente 2 fechas (las 48). No se han contrastado con la Ordre de festes locals 2025 del DOGC.
2. **Festivos autonómicos** – *Ordre EMT/66/2025, de 30 d'abril* (2026; DOGC núm. 9406, 06/05/2025) y *Ordre EMT/52/2026, de 25 de març* (2027; DOGC núm. 9637, 01/04/2026). PDFs descargados desde portaldogc (`raw/dogc_emt66_2025_laborals2026.pdf`, `raw/dogc_emt52_2026_laborals2027.pdf`). Las órdenes sólo dan fechas; el nombre de la festividad en `ccaa.csv` es el de uso habitual. Se incluye la Festa d'Aran (17/06) como fila aparte, marcada como sólo Aran (sustituye el 26/12 en 2026 y el 29/03 en 2027). El dataset Socrata de festes laborals (`djxg-4h5w`) devuelve filas vacías por la API; no se usó.
3. **Festivos locales 2027 (NO oficiales todavía)** – La Ordre de festes locals de Cataluña para 2027 **no está publicada** (la de 2026 salió el 17/12/2025; la de 2027 se espera en diciembre de 2026) y el dataset no tiene 2027. Como la vía 1 y 2 fallan, se han buscado acuerdos de los propios ayuntamientos (columna `calidad` = `ayuntamiento`) o, en su defecto, prensa local (`prensa`):
   - Barcelona: Decret d'Alcaldia ANY2026-15675 de 04/06/2026 (Gaseta Municipal), según Guia BCN – 17/05 y 24/09/2027. https://guia.barcelona.cat/ca/detall/festes-estatals-i-autonomiques-a-catalunya-i-locals-a-barcelona-al-2027_99400777767.html
   - Girona: seu electrònica, «Calendari de dies inhàbils 2026 i 2027», acord del Ple de 13/07/2026 – 26/07 (Sant Jaume cae en domingo; se da el lunes) y 29/10/2027. https://seu.girona.cat/portal/girona_ca/ajuntament/calendari/
   - Lleida: La Paeria, «Calendari laboral» – 11/05 y 29/09/2027. https://www.paeria.cat/ca/ciutat/calendaris/calendari-laboral
   - Reus: seu electrònica, acord Junta de Govern Local 26/06/2026 (la propia seu lo marca «pendent d'aprovació i publicació per la Generalitat») – 29/06 y 25/09/2027. https://seu.reus.cat/seu/carpetaCiutadana/tramit/24355
   - Badalona: web municipal, acord JGL 17/07/2026 – 11/05 y 17/05/2027. https://www.badalona.cat/ca/serveis-ajuntament/activitat-economica/comerc-1/actualitzacio-de-la-normativa-dhoraris-comercials/calendari-laboral-i-festes-locals
   - L'Hospitalet de Llobregat: seu electrònica, Ple 29/07/2026 – 17/05 y 24/09/2027. https://seuelectronica.l-h.cat/185914_1.aspx
   - Martorell: cuenta oficial del Ayuntamiento en X (@AjuntaMartorell), Ple de abril de 2026 – 26/04 y 16/08/2027. **Sólo visto como extracto de buscador; no se pudo abrir el post y martorell.cat sólo publica 2026.** Tratar con cautela.
   - Sabadell (`prensa`): Diari de Sabadell 22/06/2026, Ple de 22/06/2026 – 10/05 y 06/09/2027 (coincide con Ràdio Sabadell e iSabadell).
   - Terrassa (`prensa`): Diari de Terrassa 16/06/2026, propuesta dictaminada en comisión **antes** del Ple de 26/06/2026 que debía ratificarla – 25/03 (Dijous Sant) y 05/07/2027. No se ha verificado el acuerdo plenario.

### Illes Balears

1. **Festivos locales 2026 (oficial)** – *Resolució de la consellera de Treball, Funció Pública i Diàleg Social* por la que se hace público el calendario laboral general y local 2026, **BOIB núm. 129, 27/09/2025** (edicte 10694). PDF: https://www.caib.es/eboibfront/pdf/ca/2025/129/1201461 (también en https://www.caib.es/sites/calendarilaboral/f/529360). Correcciones posteriores revisadas (BOIB 139 de 21/10/2025 – Formentera; BOIB 150 de 13/11/2025 – Santa Eulària; BOIB 15 de 31/01/2026 – Lloseta y Llucmajor; BOIB 34 de 17/03/2026 – Santa Eulària): **ninguna afecta a las 6 cabeceras**.
2. **Festivos locales 2027 (oficial)** – *Resolució de la consellera de Treball, Funció Pública i Diàleg Social* por la que se hace público el calendario laboral general y local 2027, **BOIB núm. 122, 29/09/2026** (edicte 9716, firmada 25/09/2026). PDF: https://www.caib.es/eboibfront/pdf/ca/2026/122/1229309 (`raw/boib_122_1229309.pdf`). Localizado recorriendo la Secció III de los BOIB de septiembre de 2026 (la web caib.es/sites/calendarilaboral aún no tiene página `any_2027`). Al ser de hace 4 días, puede haber correcciones de errores posteriores.
3. **Festivos autonómicos** – 2026: anexo 1 de la Resolución del BOIB 129 (Acord del Consell de Govern de 11/04/2025, BOIB núm. 46, 15/04/2025). 2027: *Acord del Consell de Govern de 13 de març de 2026* pel qual s'aprova el calendari de festes per a l'any 2027, **BOIB núm. 33, 14/03/2026** (edicte 2617). PDF: https://www.caib.es/eboibfront/pdf/ca/2026/33/1215085 (`raw/boib_33_1215085.pdf`); coincide con el anexo 1 del BOIB 122.
4. El portal catalegdades.caib.cat devolvió 404 en el catálogo Socrata y en la búsqueda; no se encontró dataset.

Datos Baleares (locales): Ciutadella 2026 17/01 y 24/06 → 2027 24/06 (Sant Joan) y 25/06 (Sant Joanet); Eivissa 2026 05/08 y 08/08 → 2027 07/05 y 05/08 (sin nombre en el BOIB); Inca 30/07 y 20/11/2026 → 30/07 y 19/11/2027; Manacor (núcleo Manacor; Porto Cristo descartado) 17/01 y 25/07/2026 → 30/03 y 07/12/2027 (sin nombre); Maó 17/01 y 08/09/2026 → 08/09 y 09/09/2027; Palma 20/01 y 24/06 ambos años (contrastado además con los PDF «Dies festius 2026/2027 a Palma» de la seu electrònica municipal).

## Cabeceras SIN datos y por qué

- **Cerdanyola del Vallès (08266) – sin 2026 ni 2027.** La Ordre EMT/208/2025 dice literalmente «Cerdanyola del Vallès, proposta no formulada» y la modificación EMT/3/2026 no la incluye; el dataset no tiene filas 2026. La web municipal (cerdanyola.cat, seu.cerdanyola.cat) no muestra calendario de festivos localizable. Sin fuente oficial ni municipal, se deja fuera.
- **40 cabeceras catalanas sin 2027** (todas las demás salvo las 9 listadas arriba): Arenys de Mar, Berga, Cornellà, El Prat, Esplugues, Gavà, Granollers, Igualada, Manresa, Mataró, Mollet, Rubí, Sant Boi, Sant Feliu de Llobregat, Santa Coloma de Gramenet, Vic, Vilafranca, Vilanova i la Geltrú, Blanes, Figueres, La Bisbal, Olot, Puigcerdà, Ripoll, Sant Feliu de Guíxols, Santa Coloma de Farners, Balaguer, Cervera, La Seu d'Urgell, Solsona, Tremp, Vielha e Mijaran, Amposta, El Vendrell, Falset, Gandesa, Tarragona, Tortosa, Valls (más Cerdanyola). Motivo: no existe aún fuente oficial (DOGC/dataset) y las webs consultadas sólo publican 2026 (Mataró, Tarragona, Martorell-web, Manresa 404; Granollers inaccesible desde este Mac, `curl` 000 incluso sin sandbox). **La cuota de WebSearch de la sesión se agotó (200/200)** a mitad de la búsqueda municipal, lo que impidió seguir buscando acuerdos plenarios para el resto. Recomendación: rehacer Cataluña 2027 cuando se publique la Ordre de festes locals 2027 en el DOGC (previsiblemente diciembre de 2026) o reaparezca `any_calendari = 2027` en el dataset `b4eh-r8up`.

## Dudas y advertencias

- Cataluña 2027 (`calidad` ≠ `oficial`): son acuerdos municipales previos a la Ordre de la Generalitat y podrían cambiar. Especial cautela con Martorell (fuente X no abierta) y Terrassa (noticia previa al Ple).
- Nombres de festividad: el dataset catalán no los da («Fiesta local»); el BOIB no da nombre a Eivissa ni a Manacor 2027.
- La Festa d'Aran figura en `ccaa.csv` con etiqueta explícita; sólo aplica en la Val d'Aran (cabecera Vielha e Mijaran), donde sustituye al 26/12/2026 y al 29/03/2027.
- Baleares 2026: el 01/03 (Dia de les Illes Balears) cae en domingo y la comunidad fija el lunes 02/03/2026 («L'endemà del Dia de les Illes Balears»); en 2027 el 15/08 cae en domingo y se sustituye por el Dilluns de Pasqua (29/03). Están así en `ccaa.csv`.
- Las filas de 2025 de Cataluña proceden de una parte del dataset con ruido; se incluyen por comodidad pero no se han contrastado con el DOGC.
- Red: `dogc.gencat.cat` (HTML) no sirve el texto sin JavaScript; se usó el servlet PDF de portaldogc. `catalegdades.caib.cat` 404. `granollers.cat` no responde desde este equipo.

## Comprobaciones

`locales.csv` y `ccaa.csv` se cargan con `csv.DictReader` y todas las fechas pasan `datetime.date.fromisoformat`. Cada cabecera/año incluida tiene exactamente 2 fechas. Verificación integrada al final de `build.py`.
