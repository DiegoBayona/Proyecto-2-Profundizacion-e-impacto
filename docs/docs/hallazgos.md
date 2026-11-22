# Etapa 2 - Hallazgos

Corte principal analizado: **2022** (base de análisis tras filtros documentados), con contrastes esenciales en **2019** y **2014-2017**. Cada hallazgo distingue **observado**, **hipótesis** e **interpretación**, y se apoya en evidencia trazable de la Etapa 1.

> Evidencia generada por `scripts/analisis_exploratorio.py` en `outputs/persona3/`.

## H1. Gradiente negativo entre ruralidad de los evaluados y puntaje global

- **Observado:** En 2022 (n=1.035 municipios), el puntaje global promedio disminuye a mayor proporción de evaluados en zona rural: Urbano (<=20% rural) **245,01** (n=359), Mixto-bajo (20-50%) **237,10** (n=403), Mixto-alto (50-80%) **230,05** (n=220), Rural (>80%) **225,76** (n=53). Por cuartiles de `% evaluados en zona rural` (`pct_evaluados_rural`), el promedio pasa de **246,28** (Q1, menor ruralidad) a **228,50** (Q4, mayor ruralidad). La correlación con el puntaje es negativa (Pearson **-0,306**; Spearman **-0,307**). El patrón mantiene signo negativo en 2019 (Pearson -0,289) y 2014-2017 consolidado (Pearson -0,192).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_por_ruralidad.csv`, `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_evaluados_rural.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figura `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png`, figura `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_evaluados_rural.png`, figura `outputs/persona3/figuras/2022/dispersion_ruralidad_vs_puntaje.png`.
- **Hipótesis (no causal):** Los municipios donde una mayor proporción de evaluados proviene de zona rural enfrentan condiciones educativas y territoriales que podrían asociarse con menores resultados promedio en Saber 11.
- **Interpretación:** Existe una brecha territorial observable según ruralidad de los evaluados; el tamaño de la diferencia entre grupos extremos en 2022 es cercano a 19 puntos promedio, lo que sugiere heterogeneidad relevante para priorización territorial.
- **Limitación asociada:** La ruralidad se mide como `% de evaluados en zona rural` (ICFES), no como ruralidad estructural del municipio; puede reflejar composición de quienes presentan la prueba y estar afectada por sesgo de supervivencia/selección.

## H2. Asociación positiva entre acceso a internet en hogares de evaluados (ICFES) y puntaje global

- **Observado:** En 2022, `pct_internet_hogar` (internet del ICFES) muestra la correlación positiva más alta con el puntaje entre las variables analizadas (Pearson **0,570**; Spearman **0,550**, n=1.035). Por cuartiles de internet, el puntaje promedio aumenta de **223,41** (Q1) a **232,66** (Q2), **240,90** (Q3) y **254,10** (Q4). El signo positivo se observa también en 2019 (Pearson 0,406) y 2014-2017 (Pearson 0,462).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_internet_hogar.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/tablas/2022/correlaciones_spearman.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figura `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png`, figura `outputs/persona3/figuras/2022/dispersion_internet_icfes_vs_puntaje.png`.
- **Hipótesis (no causal):** Mayor acceso a internet en los hogares de los evaluados podría estar asociado con mejores condiciones de apoyo al aprendizaje o con otras ventajas socioeconómicas no observadas.
- **Interpretación:** El acceso a internet reportado por evaluados es una de las señales más consistentes asociadas a mayores promedios municipales en 2022 y en cortes previos; puede ser útil como indicador de contexto, no como explicación única.
- **Limitación asociada:** Es una medida autorreportada en la población que presenta Saber 11 (no cobertura territorial total). Correlación no implica causalidad; puede estar confundida con nivel socioeconómico, oferta educativa u otras condiciones.

## H3. Asociación positiva entre cobertura neta en media y puntaje global

- **Observado:** En 2022, la cobertura neta media (`COBERTURA_NETA_MEDIA`) se asocia positivamente con el puntaje (Pearson **0,544**; Spearman **0,500**, n=1.035). Por cuartiles, el promedio pasa de **222,48** (Q1) a **236,16** (Q2), **242,59** (Q3) y **249,84** (Q4). El signo positivo se mantiene en 2019 (Pearson 0,539) y 2014-2017 (Pearson 0,409).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_cobertura_neta_media.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figura `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png`, figura `outputs/persona3/figuras/2022/dispersion_cobertura_vs_puntaje.png`.
- **Hipótesis (no causal):** Municipios con mayor cobertura neta en media podrían contar con trayectorias educativas más continuas o condiciones institucionales asociadas a mejores desempeños promedio.
- **Interpretación:** La cobertura neta media aparece como un factor educativo estructural relacionado con el desempeño promedio municipal, con gradiente claro por cuartiles.
- **Limitación asociada:** Existen valores atípicos/sospechosos en cobertura en algunos años (incluidos registros >100 en bases originales; el análisis principal excluye >100 en esta variable). La relación es ecológica (municipal) y no identifica mecanismos causales.

## H4. Asociación negativa moderada entre deserción media y puntaje global

- **Observado:** En 2022, la deserción media (`DESERCIÓN_MEDIA`) se relaciona negativamente con el puntaje (Pearson **-0,277**; Spearman **-0,284**, n=1.035). Por cuartiles de deserción, el promedio desciende de **243,57** (Q1, menor deserción) a **241,64** (Q2), **236,07** (Q3) y **229,76** (Q4, mayor deserción). El signo negativo se observa en 2019 (Pearson -0,197) y 2014-2017 (Pearson -0,119), con magnitud más débil en años anteriores.
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_desercion_media.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figura `outputs/persona3/figuras/2022/puntaje_por_cuartiles_desercion_media.png`, figura `outputs/persona3/figuras/2022/dispersion_desercion_vs_puntaje.png`.
- **Hipótesis (no causal):** Mayores niveles de deserción media podrían reflejar dificultades de permanencia escolar asociadas a contextos donde el desempeño promedio observado también es menor.
- **Interpretación:** La deserción media aporta una señal negativa consistente en dirección, aunque de menor magnitud que internet o cobertura en 2022; conviene leerla junto con otras condiciones del territorio.
- **Limitación asociada:** Riesgo de sesgo de supervivencia: los estudiantes que desertan pueden no presentar Saber 11, por lo que el puntaje municipal observado no captura totalmente el efecto de la deserción. Además hay valores cero y extremos que requieren cautela.

## H5. Brechas territoriales departamentales amplias y heterogeneidad dentro de contextos similares

- **Observado:** En 2022, el promedio departamental del puntaje global presenta una dispersión amplia en la base analizada: valores altos en Bogotá, D.C. (**270,90**, n=1 municipio en base) y departamentos como Santander (**255,03**, n=74) y Boyacá (**254,82**, n=98), frente a promedios bajos en Chocó (**196,46**, n=29), Amazonas (**197,37**, n=6) y Guainía (**213,84**, n=2). La comparación cruzada ruralidad × cuartil de internet ICFES muestra que, dentro de un mismo grupo de ruralidad, los municipios en cuartiles altos de internet tienden a promedios mayores (p. ej. Mixto-alto: Q1 **219,04** vs Q4 **249,46**; Urbano: Q1 **232,93** vs Q4 **255,33**).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_por_departamento.csv`, `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_media.csv`, `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_n.csv`, figura `outputs/persona3/figuras/2022/top15_departamentos_puntaje.png`.
- **Hipótesis (no causal):** Las diferencias departamentales podrían concentrar combinaciones de condiciones educativas, conectividad y contexto territorial; la conectividad de los evaluados podría diferenciar resultados incluso en niveles similares de ruralidad.
- **Interpretación:** Las brechas no son uniformes: además de diferencias entre departamentos, hay variación interna relevante. Esto respalda análisis focalizados y evita conclusiones únicas para todo el país.
- **Limitación asociada:** Algunos departamentos tienen pocos municipios en la base analizada (especialmente tras filtros), lo que hace más volátiles sus promedios. La comparación cruzada es descriptiva y no controla simultáneamente otras variables.

## Nota de consistencia temporal (apoyo a Etapa 1)

- **Observado:** La dirección de las asociaciones con puntaje se mantiene entre 2019, 2014-2017 y 2022 para las cuatro variables explicativas principales (cobertura e internet positivas; ruralidad y deserción negativas), con cambios en magnitud.
- **Evidencia:** `outputs/persona3/resumen_hallazgos_base.csv`, tablas/figuras en `outputs/persona3/tablas/2019/`, `outputs/persona3/figuras/2019/`, `outputs/persona3/tablas/2014_2017/`, `outputs/persona3/figuras/2014_2017/` y subcarpetas por año.
- **Interpretación:** Los patrones de 2022 no parecen un artefacto aislado de un solo corte, aunque no implican estabilidad causal ni comparabilidad perfecta entre años.
