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

## 🛠️ Instrucciones de Uso Paso a Paso

### 1. Configuración del Calendario y Procedimiento

* **Selecciona Provincia:** Elige la provincia correspondiente para cargar los festivos locales.
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

## 4. Lógica Jurídica Específica de Agosto

La aplicación gestiona de forma diferenciada las notificaciones recibidas en el mes de agosto (periodo inhábil procesal) según el tipo de unidad de tiempo:

### 4.1. Plazo Procesal / Contencioso (Reglas LEC)
* **Cómputo por DÍAS:** Si la notificación se recibe en cualquier día de agosto, el plazo **comienza a contar el primer día hábil de septiembre**. Agosto actúa como un bloque de tiempo inhábil que retrasa el inicio del contador.
* **Cómputo por MESES:** El cómputo se realiza de **fecha a fecha**, comenzando desde el día de la notificación en agosto. 
    * *Ejemplo:* Una notificación del 10 de agosto para un plazo de un mes vencería el 10 de septiembre. Si el 10 de septiembre fuera sábado, domingo o festivo, se prorrogaría al siguiente lunes o día hábil.

### 4.2. Interposición de Recurso Contencioso (Reglas LJCA)
Para la interposición del recurso (normalmente 2 meses), se aplica una regla más restrictiva:
* **Agosto no corre:** El mes de agosto se excluye totalmente del cómputo de los meses (Art. 128.2 LJCA).
* **Inicio en agosto:** Si la notificación es en agosto, el cómputo de los meses comienza a contar desde el **primer día hábil de septiembre**.


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
