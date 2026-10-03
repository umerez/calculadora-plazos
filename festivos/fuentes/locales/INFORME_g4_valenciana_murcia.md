# INFORME – Grupo 4: COMUNITAT VALENCIANA y REGIÓN DE MURCIA (48 cabeceras de partido judicial)

Fecha del trabajo: 03/10/2026. Salidas: `locales.csv` (126 filas), `ccaa.csv` (48 filas). Script reproducible: `build.py` (+ `cv2027.json`); textos fuente en `raw/`.

Nota sobre `cabeceras.csv`: contiene una fila corrupta `46094,CATARRO4623548000000JA` duplicada de `46094,CATARROJA`. Se ha ignorado la fila corrupta; el recuento se hace sobre 47 cabeceras reales (36 Comunitat Valenciana + 11 Región de Murcia).

## Recuento

| | Cabeceras | Con 2026 | Con 2027 |
|---|---|---|---|
| Comunitat Valenciana | 36 | 36 (oficial, DOGV) | 5 (prensa, acuerdos de pleno; pendiente DOGV) |
| Región de Murcia | 11 | 11 (oficial, BORM) | 11 (oficial, BORM) |
| **Total** | **47** | **47** | **16** |

2025 no se ha incluido (no estaba en las mismas fuentes descargadas y no era prioritario).

## Fuentes usadas

### Región de Murcia (todo `oficial`)
- **Fiestas locales 2026**: BORM núm. 163, 17/07/2025 – Resolución de 7 de julio de 2025 de la Dirección General de Trabajo por la que se publica el calendario de fiestas laborales para el año 2026 (anuncio 3546). https://www.borm.es/services/anuncio/ano/2025/numero/3546/pdf?id=837607
- **Fiestas locales 2027**: BORM núm. 171, 27/07/2026 – Resolución de 13 de julio de 2026 de la Dirección General de Trabajo por la que se publica el calendario de fiestas laborales para el año 2027 (anuncio 3718). https://www.borm.es/services/anuncio/ano/2026/numero/3718/pdf?id=844400
- Las dos resoluciones incluyen también la tabla de 12 festivos de ámbito regional (nacionales + autonómicos), usada para `ccaa.csv`. El BORM nombra la festividad local solo con "1er/2.º festivo"; en `locales.csv` se consigna «Fiesta local».
- La descarga del PDF del BORM exige un User-Agent de navegador (con el UA por defecto de curl devuelve una página captcha de Radware).
- No se usó datosabiertos.regiondemurcia.es: el único dataset «Fiestas» es del Instituto de Turismo (fiestas de interés turístico), no el calendario laboral.

### Comunitat Valenciana
- **Fiestas locales 2026** (`oficial`): DOGV núm. 10238, 14/11/2025 – Resolución de 12 de noviembre de 2025, de la Conselleria de Educación, Cultura, Universidades y Empleo, por la que se aprueba el calendario de fiestas locales 2026. https://dogv.gva.es/datos/2025/11/14/pdf/2025_46326_es.pdf
  - Modificaciones comprobadas: DOGV núm. 10281, 15/01/2026 (Resolución 13/01/2026: Alcosser, Onil, Penáguila, Villamalur, Benissoda) https://dogv.gva.es/datos/2026/01/15/pdf/2026_1043_es.pdf y DOGV núm. 10314, 03/03/2026 (Resolución 27/02/2026: Orba) https://dogv.gva.es/datos/2026/03/03/pdf/2026_6733_es.pdf. **Ninguna afecta a las cabeceras.**
  - Para Dénia se han tomado solo los dos festivos del municipio, no los de las EATIM de La Xara y Jesús Pobre, que el DOGV lista aparte.
- **Festivos autonómicos 2026**: DOGV núm. 10145, 07/07/2025 – Decreto 100/2025, de 1 de julio, del Consell. https://dogv.gva.es/datos/2025/07/07/pdf/2025_24690_es.pdf
- **Festivos autonómicos 2027**: DOGV núm. 10329, 25/03/2026 – Decreto 42/2026, de 20 de marzo, del Consell. https://dogv.gva.es/datos/2026/03/25/pdf/2026_8641_es.pdf (12 festivos; desaparece el 24 de junio y entra el 29 de marzo, Lunes de Pascua; el 6 de diciembre figura como festivo aunque en 2027 cae en lunes).
- Índice oficial de la DG de Trabajo (confirma que a 03/10/2026 el último acto sobre fiestas locales es el de 2026): https://habitatge.gva.es/es/web/dg-trabajo/calendario-laboral
- **Portal dadesobertes.gva.es**: consultado por la API CKAN (`package_search` con festius/festes/fiestas/laboral/calendari y `package_list`, 1.304 datasets). **No existe ningún dataset de fiestas locales**; la pista del encargo no se ha podido confirmar. Fuente utilizada: DOGV.
- **Fiestas locales 2027** (`prensa`): la Resolución anual se publica en el DOGV a mediados de noviembre (2026: 14/11/2025), por lo que **a 03/10/2026 no está publicada**. Para las cabeceras en las que se ha podido verificar el acuerdo del pleno municipal en prensa local (lectura directa del artículo), se incluyen con `calidad=prensa` y la nota «Pendiente de publicación en el DOGV»:
  - ALCOY: 24 y 26 de abril de 2027 (Pleno extraordinario, 16/07/2026; elperiodic.com y COPE Alcoy).
  - ALICANTE: 8 de abril (Santa Faz) y 24 de junio (San Juan) de 2027 (Pleno de julio de 2026; alicanteplaza.es 30/07/2026).
  - NOVELDA: 5 de abril y 22 de julio de 2027 (Pleno de mayo de 2026, unanimidad; noveldadigital.es 07/05/2026).
  - CASTELLÓ DE LA PLANA: 1 de marzo (lunes de la Magdalena) y 29 de junio (San Pedro) de 2027 (Pleno de julio de 2026; elperiodic.com 16/07/2026).
  - VALÈNCIA: 22 de enero y 5 de abril de 2027 (Pleno ordinario de 23/07/2026; valenciaplaza.com 23/07/2026; la nota oficial de valencia.es devuelve HTTP 403 desde este equipo).
  Estas fechas deben contrastarse con el DOGV cuando se publique la Resolución (previsiblemente noviembre de 2026).

## Cabeceras SIN datos 2027 (31, todas de la Comunitat Valenciana) y motivo
Motivo común: la Resolución del DOGV de fiestas locales 2027 aún no está publicada y no se ha localizado (o no se ha podido verificar en la fuente) el acuerdo del pleno. Detalle:
- **Dudosas, excluidas por no poder verificar la fuente**:
  - VILA-REAL: un resumen de búsqueda indicaba 5 de abril y 17 de mayo de 2027 (pleno), pero el artículo de vila-realinformacio.com (03/10/2026) cita 17 de mayo y 26 de diciembre (domingo) y el de elperiodic.com (14/07/2026) solo el 17 de mayo. Contradictorio: no se incluye.
  - VILLAJOYOSA: un resumen de búsqueda indicaba 29 de julio y 29 de septiembre de 2027 aprobados por el pleno, pero el buscador de villajoyosa.com no devuelve ninguna noticia y no se encontró artículo verificable. No se incluye.
  - TORREVIEJA: solo aparece en el portal turístico torrevieja.com (5 de abril y 16 de julio de 2027), no oficial y bloqueado por Cloudflare; no se incluye.
  - SUECA: el pleno de 25/06/2026 aprobó los festivos 2027 según un resumen, pero no se localizó la nota con las fechas.
  - IBI: la Comisión de Fiestas propuso en 2026 cambiar las fechas de septiembre para 2027; sin acuerdo de pleno localizado.
- **Sin información localizada**: BENIDORM, DÉNIA, ELCHE/ELX, ELDA, ORIHUELA, SAN VICENTE DEL RASPEIG, VILLENA, NULES, SEGORBE, VINARÒS, ALZIRA, CARLET, CATARROJA, GANDIA, LLIRIA, MASSAMAGRELL, MISLATA, MONTCADA/MONCADA, ONTINYENT, PATERNA, PICASSENT, QUART DE POBLET, REQUENA, SAGUNTO/SAGUNT, TORRENT, XÀTIVA.
- Se agotó la cuota de WebSearch de la sesión (200 consultas) antes de completar la búsqueda municipio a municipio; con la publicación del DOGV en noviembre estas 31 cabeceras se cubren de una sola vez con el mismo script (`build.py`, bloque CV 2026 parametrizado por año).

## Dudas y observaciones
- Murcia 2026, `ccaa.csv`: el BORM traslada el Día de la Constitución (domingo 6/12/2026) al lunes 7/12/2026; se consigna 2026-12-07. Murcia 2027: el 9 de junio (Día de la Región) sustituye al traslado del 15 de agosto (domingo); el 1 de mayo y el 25 de diciembre de 2027 caen en sábado y figuran igualmente.
- Comunitat Valenciana 2026: Lunes de Pascua 6 de abril y 24 de junio (San Juan) sí son festivos autonómicos; Jueves Santo no lo es en la CV (sí en Murcia).
- Comunitat Valenciana: el 13 de abril de 2026 (lunes de San Vicente Ferrer) es festivo local en muchas cabeceras; en 2027 la fecha equivalente es el 5 de abril.
- Alcoy 2027: 24 de abril es sábado; es la fecha aprobada por el pleno (la Entrada), no un error.
- Webs no accesibles desde este equipo: `documentacion.diputacionalicante.es/fiestas.asp` (timeout, también sin sandbox) y `valencia.es` (403).
