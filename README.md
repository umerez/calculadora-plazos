# ⚖️ Calculadora de Plazos Legales Umerez

Esta aplicación es una herramienta especializada para el **cómputo automatizado de plazos procesales y administrativos** en el ámbito jurídico español. Ha sido diseñada para ofrecer a profesionales del derecho y ciudadanos un cálculo preciso basado en la normativa vigente.

## 🚀 Funcionamiento y Lógica Jurídica

La aplicación integra las reglas de cómputo establecidas en las principales leyes procesales y administrativas de España:

* **Ley 39/2015 (LPAC):** Para plazos administrativos.
* **Ley de Enjuiciamiento Civil (LEC):** Para plazos procesales civiles.
* **Ley de la Jurisdicción Contencioso-Administrativa (LJCA):** Para plazos en la vía contenciosa.

### 📌 El caso especial: Interposición de Recurso Contencioso

En esta modalidad, la aplicación aplica la regla específica para el plazo de **dos meses** de interposición del recurso contencioso-administrativo:

* **Agosto como paréntesis:** Según el art. 128.2 de la LJCA, durante el mes de agosto no corre el plazo para interponer el recurso contencioso-administrativo.
* **Cómputo:** Si el plazo comienza antes de agosto, el contador se "congela" el 31 de julio y se reanuda el 1 de septiembre. La aplicación realiza este salto automáticamente para asegurar que el vencimiento sea exacto.

---

## 🗂️ Calendarios de festivos: modelo por capas

Desde octubre de 2026 los festivos viven en la carpeta `festivos/` y se **componen por capas**:

```
calendario(lugar) = nacional ∪ ccaa/<comunidad> ∪ territorial/<provincia> ∪ local/<municipio>
```

| Carpeta / fichero | Contenido | Fuente |
|---|---|---|
| `festivos/nacional.csv` | Festivos estatales (2025–2027) | Art. 37.2 ET; resolución anual del BOE |
| `festivos/ccaa/pv.csv` | Festivos autonómicos de Euskadi | Decretos del Gobierno Vasco (BOPV) |
| `festivos/territorial/{araba,bizkaia,gipuzkoa}.csv` | San Prudencio, San Ignacio | BOPV, BOB, BOG |
| `festivos/local/<municipio>.csv` | Festivos locales de los ~280 municipios vascos | Open Data Euskadi (2026), BOB y BOG (2027) |
| `festivos/provincia/<provincia>.csv` | Calendario plano heredado del resto de provincias (estatal + autonómico + locales de la capital) | calendarioslaborales.com |
| `festivos/lugares.json` | Índice de lugares seleccionables: las **431 cabeceras de partido judicial** de España (incluidas las 52 capitales de provincia) y las capas de cada una | Censo Judicial del Ministerio de Justicia (planta Ley 38/1988, nomenclátor 30/12/2025) |
| `festivos/fuentes/` | Documentos de origen: partidos judiciales y municipios del Censo Judicial, ICS de Open Data Euskadi, listas extraídas de los boletines | — |

Cada CSV tiene columnas `Fecha,Festividad,Fuente`. El módulo `festivos.py` resuelve nombres (`festivos.buscar("Donostia")`)
y compone el calendario (`festivos.fechas("getxo")`). Los CSV planos de la raíz (`bizkaia.csv`, `madrid.csv`…) se mantienen
por compatibilidad y, en el caso de Euskadi, se regeneran desde las capas con `herramientas/generar_planos.py`.

**¿Por qué por municipio?** En los plazos procesales son inhábiles los festivos de la localidad donde tiene su sede el órgano
judicial (art. 182 LOPJ), de modo que el calendario correcto es el de la cabeza de partido judicial, no el de la provincia.

### Actualización anual

```bash
python3 herramientas/actualizar_festivos.py --anio 2027 --comprobar   # ¿hay calendario oficial publicado?
python3 herramientas/actualizar_festivos.py --anio 2027               # descarga las 49 provincias no vascas
python3 herramientas/migrar_a_capas.py                                # reconstruye festivos/ (Euskadi desde fuentes oficiales)
python3 herramientas/generar_planos.py --swift /Users/umerez/Scripts/plazos   # CSV planos vascos + CSV de los Atajos
python3 herramientas/exportar_swift.py <carpeta del proyecto Xcode>          # festivos_swift.json para la app macOS/iOS
python3 tests/test_plazos.py                                          # casos de referencia
```

Las páginas de calendarioslaborales.com marcadas «Calendario No Oficial» se rechazan. Euskadi no se scrapea: sus capas se
cargan desde el BOPV (comunes), BOB/BOG/BOTHA (locales) y Open Data Euskadi.

---

## 🛠️ Instrucciones de Uso Paso a Paso

### 1. Configuración del Calendario y Procedimiento

* **Selecciona la sede del órgano:** una de las 431 cabeceras de partido judicial (las capitales de provincia aparecen primero). En Euskadi cada cabecera lleva sus festivos locales oficiales; en el resto de España, de momento, se aplican los de la capital de la provincia y la aplicación lo avisa.
* **Tipo de Procedimiento:**
* *Administrativo:* Para trámites ante Ayuntamientos, Hacienda, etc.
* *Procesal Contencioso:* Para plazos dentro de un juicio ya iniciado.
* *Interposición Contencioso:* Específico para presentar el recurso inicial (aplica el salto de agosto en meses).



### 2. Introducción de Datos del Plazo

* **Fecha de Inicio:** Fecha de la notificación o publicación.
* **Unidad del Plazo:** Elige **Días** o **Meses**.
* **Tipo de Días:** Indica si son **Hábiles** (sin fines de semana ni festivos) o **Naturales**.

### 3. Cálculo y Resultados

* Haz clic en **"Calcular Vencimiento"**.
* **Detalle del Cómputo:** Revisa el desglose para ver qué días exactos se han considerado festivos o inhábiles (incluyendo los saltos de agosto o Navidad si procede).

---

## 4. Lógica de Cómputo en Agosto

La aplicación distingue automáticamente entre plazos por días y por meses cuando la notificación ocurre en agosto:

### 4.1. Plazo Procesal Estándar (LEC)
* **Días Hábiles:** Si se notifica en agosto, el plazo **comienza a contar el primer día hábil de septiembre**.
* **Meses:** Se computa de **fecha a fecha** desde el día de la notificación en agosto. (Ej: del 10 de agosto al 10 de septiembre). El resultado se traslada al primer hábil posterior si el día de vencimiento es festivo o fin de semana.

### 4.2. Interposición Contencioso (LJCA)
* **Regla Especial:** El mes de agosto no corre para el cómputo de meses. Si la notificación es en agosto, el cómputo mensual se inicia el **primer día hábil de septiembre**.

## 📅 Visualización de Resultados
Para mayor seguridad del usuario, el resultado final indica explícitamente el **día de la semana** (ej: *Lunes, 15/09/2025*), permitiendo verificar visualmente que el sistema ha evitado correctamente los fines de semana e inhábiles.


---

## ✒️ Autoría y Créditos

Este proyecto ha sido desarrollado por:

* **Esteban Umerez** (Ideación, lógica jurídica y desarrollo principal).
* Web oficial: [umerez.eu](https://umerez.eu)



**Asistencia técnica:**
Para el desarrollo del código y la optimización de la interfaz en Python/Streamlit, se ha contado con la asistencia de los modelos de inteligencia artificial **ChatGPT** (OpenAI) y **Gemini** (Google).

---

## ⚠️ Aviso Legal (Disclaimer)

Esta aplicación se ofrece bajo la modalidad **"as is" (tal cual)**, con una finalidad meramente informativa y de apoyo.

1. **Sin Responsabilidad:** El autor no se hace responsable de los posibles errores técnicos o de cálculo.
2. **Uso bajo cuenta y riesgo:** El autor no se responsabiliza de las decisiones legales adoptadas basándose en este cálculo.
3. **Contraste de datos:** Se recomienda contrastar los resultados con los calendarios oficiales de cada sede judicial o administrativa.
