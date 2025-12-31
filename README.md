# ⚖️ Calculadora de Plazos Legales Umerez

Herramienta especializada para el cómputo de plazos procesales y administrativos en España.

## 🚀 Lógica Jurídica Específica de Agosto

La aplicación gestiona de forma diferenciada las notificaciones recibidas en el mes de agosto (periodo inhábil procesal) según el tipo de unidad de tiempo:

### 1. Plazo Procesal / Contencioso (Reglas LEC)
* **Cómputo por DÍAS:** Si la notificación se recibe en cualquier día de agosto, el plazo **comienza a contar el primer día hábil de septiembre**. Agosto actúa como un bloque de tiempo inhábil que retrasa el inicio del contador.
* **Cómputo por MESES:** El cómputo se realiza de **fecha a fecha**, comenzando desde el día de la notificación en agosto. 
    * *Ejemplo:* Una notificación del 10 de agosto para un plazo de un mes vencería el 10 de septiembre. Si el 10 de septiembre fuera sábado, domingo o festivo, se prorrogaría al siguiente lunes o día hábil.

### 2. Interposición de Recurso Contencioso (Reglas LJCA)
Para la interposición del recurso (normalmente 2 meses), se aplica una regla más restrictiva:
* **Agosto no corre:** El mes de agosto se excluye totalmente del cómputo de los meses (Art. 128.2 LJCA).
* **Inicio en agosto:** Si la notificación es en agosto, el cómputo de los meses comienza a contar desde el **primer día hábil de septiembre**.

---

## 🛠️ Instrucciones de Uso

1.  **Provincia:** Selecciona la ubicación para cargar festivos locales.
2.  **Modo:** * *Procesal:* Para plazos dentro de juicios (LEC).
    * *Interposición:* Para el recurso inicial contra la administración.
3.  **Fecha de Inicio:** Introduce la fecha en la que recibiste la notificación.
4.  **Cálculo:** Obtén el vencimiento y consulta el desglose para entender cómo se ha aplicado el "salto de agosto" o la prórroga de festivos.

---

## ✒️ Autoría y Aviso Legal
**Autor:** Esteban Umerez ([umerez.eu](https://umerez.eu)) con asistencia de IA (ChatGPT y Gemini).

**Aviso Legal:** Esta herramienta es informativa. Se recomienda contrastar los resultados con los calendarios oficiales de las sedes judiciales correspondientes. El autor no se responsabiliza de errores en el cálculo o decisiones legales derivadas de su uso.
