# Etapa 3 - Limitaciones

Limitaciones asociadas a los hallazgos de la Etapa 2 y consideraciones generales para lectura del dashboard/análisis. Las decisiones de filtrado y exclusión están registradas en `docs/persona3/registro_decisiones.md` y `outputs/persona3/registro_decisiones.csv`.

## Limitaciones asociadas a cada hallazgo

### H1. Ruralidad y puntaje global
- **Medición de ruralidad:** `pct_evaluados_rural` mide la proporción de evaluados Saber 11 en zona rural, no la ruralidad estructural/demográfica del municipio.
- **Sesgo de selección/supervivencia:** Solo se observan estudiantes que presentan la prueba; la composición de evaluados puede diferir entre municipios más rurales y más urbanos.
- **Ruido en grupos pequeños:** El grupo Rural (>80%) en 2022 tiene 53 municipios (frente a 359 en Urbano), por lo que sus promedios son más sensibles a casos particulares.

### H2. Internet en hogares de evaluados (ICFES) y puntaje global
- **Fuente y población:** `pct_internet_hogar` proviene del cuestionario/contexto de evaluados ICFES, no de una medición universal de conectividad del municipio.
- **Confusión potencial:** Puede correlacionar con condiciones socioeconómicas, capital educativo u oferta escolar no incluidas en el modelo descriptivo.
- **No causalidad:** Asociación estadística no permite afirmar que aumentar internet cause incrementos en puntaje.

### H3. Cobertura neta media y puntaje global
- **Calidad de indicadores administrativos:** La cobertura neta media puede presentar valores atípicos o inconsistencias de reporte; en el análisis principal se excluyeron valores >100 por ser sospechosos para comparación porcentual.
- **Ceros y valores extremos:** En 2022 se observaron municipios con cobertura neta media igual a 0 en la base con flags (`outputs/persona3/tablas/2022/base_2022_con_flags_calidad.csv`); se conservaron salvo reglas explícitas, pero requieren revisión caso a caso.
- **Nivel ecológico:** Relación observada a nivel municipio-año, no a nivel de estudiante o institución.

### H4. Deserción media y puntaje global
- **Sesgo de supervivencia:** La deserción puede reducir la presencia de ciertos estudiantes en Saber 11; el puntaje observado puede subestimar problemas en contextos con mayor abandono.
- **Valores sospechosos:** Se registran ceros y valores altos atípicos en deserción; el criterio aplicado excluyó deserción >100 del análisis principal y trató ceros como sospechosos según regla documentada.
- **Magnitud variable en el tiempo:** La asociación negativa es más débil en 2014-2017 que en 2022, lo que limita afirmaciones fuertes sin análisis adicional.

### H5. Brechas departamentales y comparación cruzada
- **Tamaño de muestra departamental:** Algunos promedios departamentales se calculan con pocos municipios (p. ej. Amazonas n=6, Guaviare n=3, Guainía n=2, Vaupés n=1 en la base 2022 analizada), aumentando volatilidad.
- **Comparación cruzada descriptiva:** La tabla ruralidad × cuartil de internet no controla otras variables ni garantiza tamaños de celda homogéneos (ver `comparacion_cruzada_ruralidad_x_internet_n.csv`).
- **Heterogeneidad interna:** El promedio departamental oculta diferencias entre municipios.

## Limitaciones generales de los datos

- **Cobertura de Saber 11:** En 2022 se excluyeron **9 municipios sin puntaje global** (ver `outputs/persona3/tablas/2022/excluidos_y_motivos.csv`), además de registros sin puntaje en otros cortes; no todos los municipios tienen medición comparable cada año.
- **Valores sospechosos:** Presencia de ceros, valores superiores a 100 y posibles inconsistencias en indicadores porcentuales/administrativos. El script genera `base_2022_con_flags_calidad.csv` y aplica exclusiones documentadas para el análisis principal.
- **Municipios con pocos evaluados:** Se excluyeron del análisis principal municipios con `total_evaluados < 30` por ruido muestral; esto reduce cobertura pero mejora estabilidad descriptiva. Los resultados pueden cambiar con otro umbral.
- **IPM e internet TerriData (pendiente de actualización externa):** `dataset_integrado.csv` ya incluye `ipm_municipal` y variables TerriData cuando existen, pero la instrucción de trabajo indica que IPM e internet de TerriData podían estar pendientes de resolución por Persona 2. Si Persona 2 actualiza fuentes/limpieza, debe re-ejecutarse `scripts/analisis_exploratorio.py` e incorporarse su lectura en Etapas 2-4.
- **Disponibilidad temporal de variables:** No todas las variables externas (p. ej. penetración de internet en hogares de TerriData) están disponibles para todos los años/municipios en el dataset integrado.

## Limitaciones generales del análisis

- **Correlación no implica causalidad:** Todas las relaciones reportadas son descriptivas/ecológicas (municipio-año).
- **Falacia ecológica:** Patrones a nivel municipal no deben interpretarse como efectos individuales sobre estudiantes.
- **Confusión no controlada:** No se estimaron modelos multivariados ni controles simultáneos; variables como ruralidad, internet, cobertura y deserción pueden estar correlacionadas entre sí.
- **Sesgo de supervivencia:** El puntaje solo refleja a quienes presentan Saber 11.
- **Ruido muestral:** Municipios pequeños o con pocos evaluados son más volátiles; la exclusión por umbral y los filtros de calidad afectan el conjunto analizado.
- **Sensibilidad a filtros:** Cambios en umbral de evaluados, tratamiento de ceros/>100 o inclusión de excluidos pueden modificar magnitudes (y ocasionalmente conclusiones de detalle). El archivo de excluidos y las bases con flags permiten análisis de sensibilidad.
- **Comparabilidad temporal limitada:** Se replicó lo esencial en 2019 y 2014-2017, pero cambios en pruebas, contextos, cobertura y calidad de registros pueden afectar comparaciones entre años.
