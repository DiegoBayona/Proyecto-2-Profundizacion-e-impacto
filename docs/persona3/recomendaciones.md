# Recomendaciones (Etapa 4)

Estas recomendaciones salen de lo que documenté en `docs/persona3/hallazgos.md`. Las planteo con cuidado (sin hablar de causalidad): la idea es ayudar a priorizar revisiones y seguimiento con lo que muestran los datos.

## R1. Revisar con más detalle municipios con alta ruralidad de evaluados y puntajes bajos

- **Se apoya en:** H1 (gradiente por ruralidad) y H5 (brechas territoriales).
- **Evidencia:** En 2022 el promedio pasa de 245,01 (urbano <=20% rural) a 225,76 (rural >80%); el cuartil Q4 de ruralidad promedia 228,50 vs 246,28 en Q1. También hay diferencias grandes entre departamentos.
  - `outputs/persona3/tablas/2022/comparacion_por_ruralidad.csv`
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_evaluados_rural.csv`
  - `outputs/persona3/tablas/2022/comparacion_por_departamento.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png`
- **Para quién puede servir:** Secretarías de educación (departamental/municipal) y equipos de planeación o acompañamiento territorial.
- **Para qué decisión ayuda:** Priorizar dónde revisar apoyos pedagógicos, permanencia y condiciones de acceso en municipios/grupos con más evaluados rurales y promedios bajos, mirando también cuántos evaluados hay y su composición.
- **Precaución:** Esto no significa que la ruralidad “cause” el resultado; la variable es sobre evaluados y puede estar mezclada con otros factores.

## R2. Mirar brechas de conectividad/contexto digital donde el acceso a internet de evaluados es bajo

- **Se apoya en:** H2 (asociación positiva internet-puntaje) y H5 (diferencias dentro de grupos de ruralidad según internet).
- **Evidencia:** En 2022, Q1 de `pct_internet_hogar` promedia 223,41 vs 254,10 en Q4 (Pearson 0,570). En el cruce ruralidad × internet, los cuartiles altos de internet muestran mayores promedios dentro de varios grupos de ruralidad.
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_internet_hogar.csv`
  - `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_media.csv`
  - `outputs/persona3/tablas/2022/correlaciones_pearson.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png`
- **Para quién puede servir:** Equipos de política educativa y conectividad (MEN/secretarías), programas de acceso digital y seguimiento territorial.
- **Para qué decisión ayuda:** Priorizar diagnósticos de brecha digital educativa en municipios donde poco acceso a internet en hogares de evaluados coincide con promedios más bajos, contrastando con evidencia local.
- **Precaución:** Es una medida de evaluados ICFES y puede reflejar condiciones socioeconómicas; cuando Persona 2 actualice internet TerriData, conviene complementar y volver a correr el análisis.

## R3. Hacer seguimiento conjunto de cobertura neta en media y deserción, y revisar calidad de los datos

- **Se apoya en:** H3 (cobertura y puntaje), H4 (deserción y puntaje) y las limitaciones de calidad/sesgo de supervivencia.
- **Evidencia:** En 2022, Q1 de cobertura neta media promedia 222,48 vs 249,84 en Q4 (Pearson 0,544); Q4 de deserción media promedia 229,76 vs 243,57 en Q1 (Pearson -0,277). La dirección se mantiene en 2019 y 2014-2017.
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_cobertura_neta_media.csv`
  - `outputs/persona3/tablas/2022/comparacion_cuartiles_desercion_media.csv`
  - `outputs/persona3/resumen_hallazgos_base.csv`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png`
  - `outputs/persona3/figuras/2022/puntaje_por_cuartiles_desercion_media.png`
- **Para quién puede servir:** Secretarías de educación, equipos de permanencia escolar y quienes revisan calidad de información educativa.
- **Para qué decisión ayuda:** Priorizar la revisión de municipios con baja cobertura y/o alta deserción junto con sus resultados Saber 11, y al mismo tiempo validar registros con valores sospechosos (ceros, extremos, inconsistencias) antes de tomar decisiones operativas.
- **Precaución:** No es una relación causal y puede haber sesgo de supervivencia. Si se actualizan IPM/internet TerriData u otros insumos, toca re-ejecutar el análisis.
