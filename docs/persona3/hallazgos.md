# Hallazgos (Etapa 2)

Me centré en el corte de **2022** (ya con los filtros que dejé en el registro) y lo comparé con **2019** y el periodo **2014-2017** para ver si los patrones se repetían. Abajo separo lo que se ve en los datos, lo que podría estar pasando y cómo lo leería, con la evidencia en `outputs/persona3/` (salida de `scripts/analisis_exploratorio.py`).

## H1. Ruralidad de los evaluados y puntaje

- **Lo que se observa:** En 2022 (n=1.035 municipios) el puntaje global promedio baja cuando aumenta la proporción de evaluados en zona rural: Urbano (<=20% rural) **245,01** (n=359), Mixto-bajo (20-50%) **237,10** (n=403), Mixto-alto (50-80%) **230,05** (n=220), Rural (>80%) **225,76** (n=53). Por cuartiles de `pct_evaluados_rural` pasa de **246,28** (Q1, menos ruralidad) a **228,50** (Q4). La correlación con el puntaje es negativa (Pearson **-0,306**; Spearman **-0,307**). En 2019 y 2014-2017 consolidado también sale negativa (Pearson -0,289 y -0,192).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_por_ruralidad.csv`, `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_evaluados_rural.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, y figuras `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png`, `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_evaluados_rural.png`, `outputs/persona3/figuras/2022/dispersion_ruralidad_vs_puntaje.png`.
- **Hipótesis (no causal):** Donde hay más evaluados de zona rural podrían pesar condiciones educativas o territoriales que se relacionen con promedios más bajos.
- **Cómo lo interpreto:** Sí se nota una brecha según ruralidad de los evaluados (casi 19 puntos entre extremos en 2022), algo útil para mirar prioridades territoriales.
- **Limitación:** Esta ruralidad es `% de evaluados en zona rural` (ICFES), no la ruralidad del municipio completo; también puede influir quiénes presentan la prueba.

## H2. Internet en hogares de evaluados (ICFES) y puntaje

- **Lo que se observa:** En 2022, `pct_internet_hogar` es la variable con correlación positiva más alta frente al puntaje (Pearson **0,570**; Spearman **0,550**, n=1.035). Por cuartiles el promedio sube de **223,41** (Q1) a **232,66** (Q2), **240,90** (Q3) y **254,10** (Q4). El signo se repite en 2019 (Pearson 0,406) y 2014-2017 (Pearson 0,462).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_pct_internet_hogar.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/tablas/2022/correlaciones_spearman.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figuras `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png` y `outputs/persona3/figuras/2022/dispersion_internet_icfes_vs_puntaje.png`.
- **Hipótesis (no causal):** Más acceso a internet en hogares de evaluados podría ir de la mano con mejores apoyos al estudio u otras ventajas que no estamos midiendo.
- **Cómo lo interpreto:** Es una señal bastante consistente de contexto asociada a mayores promedios, pero no la tomaría como única explicación.
- **Limitación:** Es dato reportado por quienes presentan Saber 11 (no cobertura total del municipio) y puede estar mezclado con nivel socioeconómico u otros factores.

## H3. Cobertura neta en media y puntaje

- **Lo que se observa:** En 2022 la cobertura neta media (`COBERTURA_NETA_MEDIA`) se asocia positivamente con el puntaje (Pearson **0,544**; Spearman **0,500**, n=1.035). Por cuartiles sube de **222,48** (Q1) a **236,16** (Q2), **242,59** (Q3) y **249,84** (Q4). En 2019 (Pearson 0,539) y 2014-2017 (Pearson 0,409) también sale positiva.
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_cobertura_neta_media.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figuras `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png` y `outputs/persona3/figuras/2022/dispersion_cobertura_vs_puntaje.png`.
- **Hipótesis (no causal):** Municipios con mayor cobertura en media podrían tener trayectorias más continuas o condiciones escolares que acompañen mejores promedios.
- **Cómo lo interpreto:** Se ve un gradiente claro por cuartiles, así que parece un factor educativo relevante a nivel municipal.
- **Limitación:** Hay valores raros en algunos años (en el análisis principal excluí >100) y la relación es a nivel municipio, no causal.

## H4. Deserción media y puntaje

- **Lo que se observa:** En 2022 la deserción media (`DESERCIÓN_MEDIA`) se relaciona negativamente con el puntaje (Pearson **-0,277**; Spearman **-0,284**, n=1.035). Por cuartiles el promedio baja de **243,57** (Q1, menor deserción) a **241,64** (Q2), **236,07** (Q3) y **229,76** (Q4). El signo se mantiene en 2019 (Pearson -0,197) y 2014-2017 (Pearson -0,119), aunque más débil antes.
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_cuartiles_desercion_media.csv`, `outputs/persona3/tablas/2022/correlaciones_pearson.csv`, `outputs/persona3/resumen_hallazgos_base.csv`, figuras `outputs/persona3/figuras/2022/puntaje_por_cuartiles_desercion_media.png` y `outputs/persona3/figuras/2022/dispersion_desercion_vs_puntaje.png`.
- **Hipótesis (no causal):** Más deserción podría reflejar dificultades de permanencia en contextos donde el promedio observado también es menor.
- **Cómo lo interpreto:** La señal va en la dirección esperada, pero en 2022 pesa menos que internet o cobertura; conviene leerla junto con las otras variables.
- **Limitación:** Quienes desertan pueden no presentar Saber 11 (sesgo de supervivencia), y además hay ceros/extremos que piden cuidado.

## H5. Brechas entre departamentos y diferencias dentro de contextos parecidos

- **Lo que se observa:** En 2022 hay bastante dispersión entre departamentos: promedios altos como Bogotá, D.C. (**270,90**, n=1 en la base) y departamentos como Santander (**255,03**, n=74) y Boyacá (**254,82**, n=98), frente a otros bajos como Chocó (**196,46**, n=29), Amazonas (**197,37**, n=6) y Guainía (**213,84**, n=2). En el cruce ruralidad × cuartil de internet ICFES, dentro de un mismo grupo de ruralidad los cuartiles altos de internet suelen tener promedios mayores (p. ej. Mixto-alto: Q1 **219,04** vs Q4 **249,46**; Urbano: Q1 **232,93** vs Q4 **255,33**).
- **Evidencia:** `outputs/persona3/tablas/2022/comparacion_por_departamento.csv`, `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_media.csv`, `outputs/persona3/tablas/2022/comparacion_cruzada_ruralidad_x_internet_n.csv`, figura `outputs/persona3/figuras/2022/top15_departamentos_puntaje.png`.
- **Hipótesis (no causal):** Las diferencias departamentales pueden juntar varias condiciones (educativas, conectividad, territorio); la conectividad de los evaluados parece marcar diferencias incluso con ruralidad similar.
- **Cómo lo interpreto:** No hay un solo patrón para todo el país: hay brechas entre departamentos y también variación interna, así que toca mirar con foco territorial.
- **Limitación:** Algunos departamentos quedan con pocos municipios tras los filtros (promedios más volátiles). El cruce es descriptivo y no controla otras variables.

## Nota rápida sobre 2019 y 2014-2017

- **Lo que se observa:** La dirección de las asociaciones se mantiene entre 2019, 2014-2017 y 2022 en las cuatro variables principales (cobertura e internet positivas; ruralidad y deserción negativas), aunque cambian las magnitudes.
- **Evidencia:** `outputs/persona3/resumen_hallazgos_base.csv` y tablas/figuras en `outputs/persona3/tablas/2019/`, `outputs/persona3/figuras/2019/`, `outputs/persona3/tablas/2014_2017/`, `outputs/persona3/figuras/2014_2017/` (periodo consolidado).
- **Cómo lo interpreto:** 2022 no parece un caso aislado, pero eso no prueba causalidad ni que los años sean totalmente comparables.
