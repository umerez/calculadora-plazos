# Revisión de octubre (3-10-2026, tarde): festivos 2027 pendientes

Primera pasada de la «actualización de octubre» (tarea programada `festivos-2027-octubre`), ejecutada el 3-10-2026
por la tarde. Material de trabajo de cada comprobación (boletines descargados, scripts de barrido reutilizables e
`INFORME.md` por comunidad) en `/Users/umerez/Proyectos/calculadora_plazos/fuentes-brutas/revision-2026-10-03/`.

## Resultado: ningún boletín de los esperados ha salido todavía

| Objetivo | Comprobado | Estado a 3-10-2026 | Previsión |
|---|---|---|---|
| Andalucía, Resolución DG Trabajo fiestas locales 2027 (BOJA) | Dataset work-calendar (0 registros LOCAL 2027); sumarios BOJA 190-192 (30/09-02/10); eBOJA; página de la Consejería | **No publicada** (0/85) | 2.ª quincena de octubre (precedentes: BOJA 197 de 14/10/2025, 198 de 11/10/2024) |
| Galicia, Resolución consolidada (DOG) | Sumarios DOG 165-188 (01/09-02/10); dataset Abertos 0699 (solo 12 autonómicos) | **No publicada** | finales de octubre / noviembre (DOG 210 de 30/10/2025) |
| Galicia, BOP A Coruña | `bop.dacoruna.gal` sin respuesta (timeout / ECONNREFUSED) con y sin sandbox, WebFetch y navegador | **Inaccesible**. La prensa (El Correo Gallego, 30/09/2026) indica que ya está publicada | reintentar desde otra red; cargaría 14 cabeceras |
| Galicia, BOP Ourense | API `getFecha` 28/09-03/10 (método validado con el edicto de 17/10/2025) | **No publicada** | mediados de octubre |
| Galicia, BOPPO Pontevedra | sumarios hasta el núm. 190 (02/10) | **No publicada** | 1.ª quincena de octubre |
| Extremadura, Resolución fiestas locales 2027 (DOE) | Sumarios DOE 190-191 (01-02/10); buscador avanzado validado; datos.gob.es | **No publicada** (0/21) | 2.ª quincena de octubre (DOE 204 de 23/10/2025) |
| Araba, resolución Delegación Territorial (BOTHA) | Sumarios BOTHA 55-113 (15/05-02/10); buscador avanzado | **No publicada**. Ojo: la de 2026 salió en julio (BOTHA 82, 21/07/2025); en 2026 la Delegación pidió propuestas el 2/07 | octubre-noviembre |
| Ceuta, calendario 2027 (BOCCE) | BOCCE 6.648-6.657 y extraordinarios 42-44 | **No publicado** | 2.ª quincena de octubre (en 2025, 22 días después del Pleno) |
| BOE, Resolución fiestas laborales 2027 | API de sumarios 20/09-03/10, todas las secciones | **No publicada** | 14-28 de octubre (BOE-A-2025-21667 salió el 28/10/2025) |
| Aragón (BOA / opendata) y Navarra (BON) | buscadores con control positivo; sumarios BON 168-196 | **No publicadas** (esperado) | Aragón 2.ª quincena de noviembre; Navarra 1.ª quincena de diciembre |

## Cambios aplicados en el repo

- `fuentes/araba_municipios_2027.csv`: la fila de Vitoria-Gasteiz (5-8-2027, La Blanca) pasa de prensa a
  **[ayuntamiento]** (acta oficial del Pleno de 24/07/2026, Acta 10899, vitoria-gasteiz.org) y queda marcada como
  provisional, con lo que `COBERTURA.md` ya la cuenta como tal. Amurrio 2027 sigue sin dato (su propuesta no pasa por el
  Pleno; nada publicado).
- Ninguna fila `[prensa]` sustituida; ninguna cifra de cobertura cambia.

## Comprobaciones y hallazgos sin cambio de datos

- **Ceuta, discrepancia resuelta**: el acta del Consejo de Gobierno de 08/09/2026 (ceuta.es) transcribe el proyecto de
  Decreto del calendario 2027: el 5-8 (Ntra. Sra. de África) y el 17-5 (Eidul Adha) son sustituciones autonómicas; las dos
  locales son el 10-3 (Eid al-Fitr) y el 2-9 (Día de Ceuta). Lo cargado es correcto; sigue en calidad `prensa` hasta el BOCCE.
- **Amurrio 2026**: el BOTHA 82/2025 da el 17-8-2026, que es lo que está cargado (desde el ICS de Open Data Euskadi).
- **Andalucía 2026**: la Resolución de 20/04/2026 (BOJA 79) cambió festivos de seis municipios por las elecciones del
  17/05/2026; ninguno es cabecera. Las 170 filas 2026 coinciden al 100 % con el dataset. Calendario autonómico 2027 =
  Decreto 84/2026 = 12 registros LABORAL del dataset.
- **Extremadura 2026**: sin modificaciones nuevas del anexo desde el DOE 141 (23/07/2026). Acuerdos municipales 2027 en
  prensa (Mérida 13/05 y 10/12; Cáceres 23/04 y 28/05): documentados en el informe, no cargados.
- **Galicia 2027 por prensa**: nada contradice A Coruña 9/2 y 24/6, Ferrol 7/1 y 29/3, Pontevedra 10/2 y 29/3.
- Referencias BOE verificadas por XML: 2026 → BOE-A-2025-21667 (28/10/2025); 2025 → BOE-A-2024-21316 (18/10/2024).

## Qué repetir en la siguiente pasada (a partir del 20-10-2026)

Los diez objetivos de la tabla, con los scripts de barrido de `fuentes-brutas/revision-2026-10-03/*/src/`
(`scan_sumarios.py` BOE, `check_doe_2027.py`, `dog_sweep.py`, `botha_busqueda.py`, `descarga_bocce.sh`). Para Andalucía,
recontar `type=LOCAL, year=2027` en el dataset y reutilizar `build_2026_referencia.py`.
