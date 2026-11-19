# Revisión de noviembre de 2026 (19-11-2026)

Fuentes brutas y scripts: `fuentes-brutas/locales-2026-11-19/<grupo>/` (INFORME.md en cada una). Todo lo cargado es `oficial`.

## Cargado
- **Andalucía:** 84/85 cabeceras, BOJA 210 (29-10-2026, Resolución 23-10-2026); autonómicos Decreto 84/2026. Falta Arcos de la Frontera (no figura en el BOJA ni en el dataset de la Junta).
- **Galicia:** 45/45, DOG 204 (26-10-2026, Resolución 15-10-2026); autonómicos Decreto 68/2026. Cangas: el DOG da 19/3 y 30/8 (el dataset Abertos solo el 30/8; prevalece el DOG). Sustituidas 6 filas [prensa] (A Coruña, Ferrol, Pontevedra; mismas fechas).
- **Extremadura:** 21/21, DOE 207 (27-10-2026, Resolución 15-10-2026); autonómicos Decreto 119/2026.
- **Araba:** Vitoria-Gasteiz y Amurrio, BOTHA 116 (9-10-2026); vía `araba_municipios_2027.csv`.
- **Ceuta:** BOCCE 6.666 (3-11-2026) locales 10/3 y 2/9; BOCCE 6.668 (10-11) calendario 2027 de 14 festivos. Sustituidas las filas de prensa (mismas fechas).
- **Castilla y León (BOP, no hay orden del BOCYL):** Valladolid 13/5 y 8/9 (BOP Valladolid 204, 23-10); Astorga 23/7 y 23/8 y Cistierna 28/5 y 8/9 y Villablino 17/8 (BOP León 207, 30-10); Benavente 5/4 y 26/5 y Puebla de Sanabria 8/9 y 9/9 (BOP Zamora 130, 6-11); Burgos 4/6 y 29/6 (BOP Burgos 202, 23-10; sustituye [prensa], mismas fechas); Sahagún 2026 12/6 y 2/7 (BOP León 8, 14-1-2026).
- **La Rioja:** BOR 160 (21-8-2026): Logroño 11/6 y 21/9, Calahorra 3/3 y 31/8, Haro 25/6 y 8/9 (sustituyen [prensa], mismas fechas); autonómicos BOR 86 (Resolución 186/2026), idénticos.
- **Asturias:** autonómicos 2027 oficiales (BOE-A-2026-21254 y Decreto 7/2026); sustituyen la lista DERIVADO; traslado del 15-8 al lunes 16-8-2027 confirmado. Locales 2027 sin correcciones.

## No publicado / pendiente
- **Comunitat Valenciana:** DOGV hasta el nº 10497 (19-11) sin resolución de fiestas locales 2027 ni dataset en dadesobertes. Siguen [prensa]: Alcoy, Alicante, Novelda, Castelló, València.
- **Aragón:** Decreto 163/2026 (BOA 180, 16-9-2026) ya cargado, sin cambios; la resolución de locales 2027 no ha salido (barrido BOA 15-10 a 19-11; dataset opendata 2027 inexistente). En 2025 salió el 20-11.
- **Navarra:** resolución de locales 2027 no publicada (último BON 231; en 2025 salió el 2-12). Las 5 cabeceras solo tienen el 3-12.
- **Toro 2027:** en ningún BOP de Zamora; **Villablino 2027:** solo 17/8 (falta el segundo festivo; en 2025-2026 tenía el 4/12); **Haro 2026:** sin dato (BOR 159 no da fechas).

## Cambios al repo
Test `sin_2026` ajustado (Sahagún ya tiene 2026).
