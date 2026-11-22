# Etapa 4 - Recomendaciones (Persona 3)

Recomendaciones trazables a hallazgos de `docs/persona3/hallazgos.md`. Se formulan con cautela para no afirmar causalidad: priorizan revisión, focalización y seguimiento con base en evidencia descriptiva.

## R1. Priorizar la revisión focalizada de municipios con alta ruralidad de evaluados y bajo puntaje observado

- **Hallazgo que la respalda:** H1 (gradiente negativo por ruralidad de evaluados) y H5 (brechas territoriales amplias).
- **Evidencia base:** En 2022, el promedio pasa de 245,01 (urbano <=20% rural) a 225,76 (rural >80%); cuartil Q4 de ruralidad promedia 228,50 vs 246,28 en Q1. Departamentos con promedios bajos concentran contextos heterogéneos que requieren lectura territorial.
  - `outputs/persona3/tablas/2022/comparacion_por_ruralidad.csv`
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_evaluados_rural.csv`
  - `outputs/persona3/tablas/2022/comparacion_por_departamento.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png`
- **A quién va dirigida:** Secretarías de educación departamentales/municipales, equipos de planeación educativa territorial y actores que definan estrategias de acompañamiento en zonas con mayor ruralidad de evaluados.
- **Qué decisión apoya:** Priorizar la revisión y focalización territorial de apoyos pedagógicos, permanencia y condiciones de acceso educativo en municipios/grupos con mayor proporción de evaluados rurales y resultados promedio persistentemente bajos, contrastando con la composición y tamaño de la población evaluada.
- **Precaución:** No implica que la ruralidad por sí sola cause el resultado; la variable mide ruralidad de evaluados y puede estar asociada a otros factores.

## R2. Priorizar el análisis de brechas de conectividad educativa y contexto digital en municipios con menor acceso a internet de evaluados

- **Hallazgo que la respalda:** H2 (asociación positiva internet ICFES-puntaje) y H5 (diferencias dentro de grupos de ruralidad según cuartil de internet).
- **Evidencia base:** En 2022, Q1 de `pct_internet_hogar` promedia 223,41 vs 254,10 en Q4 (Pearson 0,570). En la comparación cruzada ruralidad × internet, los cuartiles altos de internet muestran mayores promedios dentro de varios grupos de ruralidad.
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_internet_hogar.csv`
  - `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_media.csv`
  - `outputs/persona3/tablas/2022/correlaciones_pearson.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png`
- **A quién va dirigida:** Equipos de política educativa y conectividad (MEN/secretarías), programas de dotación y acceso digital, y equipos de seguimiento territorial.
- **Qué decisión apoya:** Priorizar la revisión de municipios donde el bajo acceso a internet en hogares de evaluados coincide con menores promedios, para orientar diagnósticos de brecha digital educativa y coordinar intervenciones con evidencia local (sin asumir efecto automático).
- **Precaución:** La medida es de evaluados ICFES y puede reflejar condiciones socioeconómicas más amplias; se recomienda complementar con indicadores TerriData de internet cuando Persona 2 consolide/actualice la fuente.

## R3. Fortalecer el seguimiento conjunto de cobertura neta en media y deserción en municipios con señales de rezago, incorporando revisión de calidad de datos

- **Hallazgo que la respalda:** H3 (asociación positiva cobertura-puntaje), H4 (asociación negativa deserción-puntaje) y limitaciones de calidad/supervivencia.
- **Evidencia base:** En 2022, Q1 de cobertura neta media promedia 222,48 vs 249,84 en Q4 (Pearson 0,544); Q4 de deserción media promedia 229,76 vs 243,57 en Q1 (Pearson -0,277). La dirección de estas asociaciones se mantiene en 2019 y 2014-2017.
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_cobertura_neta_media.csv`
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_desercion_media.csv`
  - `outputs/persona3/resumen_hallazgos_base.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_desercion_media.png`
- **A quién va dirigida:** Secretarías de educación, equipos de permanencia escolar y analistas de calidad de información educativa.
- **Qué decisión apoya:** Priorizar la revisión de municipios con baja cobertura neta media y/o alta deserción junto con sus resultados Saber 11, para identificar alertas de trayectoria educativa y, en paralelo, validar registros con valores sospechosos (ceros, extremos, inconsistencias) antes de usarlos para decisiones operativas.
- **Precaución:** La relación no es causal y puede estar afectada por sesgo de supervivencia; las recomendaciones deben leerse como apoyo a priorización y verificación, no como atribución de causa. Re-ejecutar el análisis si se actualizan IPM/internet TerriData u otros insumos de Persona 2.
