# Limitaciones (Etapa 3)

Estas son las limitaciones que veo para leer los hallazgos con cuidado. Los filtros y exclusiones que apliqué están anotados en `docs/persona3/registro_decisiones.md` y `outputs/persona3/registro_decisiones.csv`.

## Por hallazgo

### H1. Ruralidad y puntaje
- **Qué mide la ruralidad:** `pct_evaluados_rural` es el % de evaluados en zona rural (ICFES), no la ruralidad “real” o demográfica de todo el municipio.
- **Quién rinde la prueba:** solo vemos a quienes presentan Saber 11, y ese grupo puede cambiar según el contexto.
- **Grupos pequeños:** en 2022 el grupo Rural (>80%) tiene 53 municipios (vs 359 en Urbano), así que el promedio se mueve más fácil con pocos casos.

### H2. Internet (ICFES) y puntaje
- **Fuente:** `pct_internet_hogar` viene del contexto de los evaluados, no de una medición de todo el municipio.
- **Posibles confusores:** puede ir junto con condiciones socioeconómicas u otras cosas que no incluí en este análisis.
- **No es causal:** que haya correlación no significa que mejorar internet, por sí solo, suba el puntaje.

### H3. Cobertura neta en media y puntaje
- **Calidad del dato:** la cobertura puede tener valores raros; saqué >100 del análisis principal porque no cuadran bien como porcentaje.
- **Ceros/extremos:** en 2022 hay municipios con cobertura neta media en 0 en la base con flags (`outputs/persona3/tablas/2022/base_2022_con_flags_calidad.csv`); los dejé según la regla, pero vale revisarlos caso a caso.
- **Nivel del análisis:** es una relación a nivel municipio-año, no por estudiante o colegio.

### H4. Deserción media y puntaje
- **Sesgo de supervivencia:** si alguien deserta puede no presentar Saber 11, entonces el puntaje no refleja todo ese efecto.
- **Valores sospechosos:** hay ceros y valores altos; excluí deserción >100 y traté ceros como sospechosos según lo documentado.
- **Cambia en el tiempo:** la relación negativa es más débil en 2014-2017 que en 2022, así que no conviene afirmarla igual para todos los años.

### H5. Brechas entre departamentos y cruce ruralidad × internet
- **Pocos municipios en algunos casos:** hay departamentos con muy pocos municipios en la base 2022 (p. ej. Amazonas n=6, Guaviare n=3, Guainía n=2, Vaupés n=1), y eso vuelve el promedio más inestable.
- **Cruce descriptivo:** la tabla ruralidad × cuartil de internet no controla otras variables y las celdas no tienen el mismo tamaño (ver `comparacion_cruzada_ruralidad_x_internet_n.csv`).
- **Promedio esconde diferencias:** dentro de un mismo departamento puede haber municipios muy distintos.

## Limitaciones de los datos

- **Saber 11:** en 2022 quedaron fuera **9 municipios sin puntaje global** (ver `outputs/persona3/tablas/2022/excluidos_y_motivos.csv`) y en otros cortes también faltan puntajes; no todos los municipios aparecen igual cada año.
- **Valores raros:** hay ceros, >100 y posibles inconsistencias. Para eso están `base_2022_con_flags_calidad.csv` y las exclusiones del análisis principal.
- **Municipios con pocos evaluados:** saqué del análisis principal los que tienen `total_evaluados < 30` porque el dato es muy ruidoso; si se cambia ese umbral, los resultados pueden variar.
- **IPM e internet TerriData:** en `dataset_integrado.csv` ya hay columnas como `ipm_municipal` y variables de internet TerriData cuando existen, pero si Persona 2 actualiza esas fuentes hay que volver a correr `scripts/analisis_exploratorio.py` y revisar hallazgos/limitaciones/recomendaciones.
- **Disponibilidad por año:** no todas las variables externas están para todos los años o municipios.

## Limitaciones del análisis

- **No causalidad:** todo lo que reporto es descriptivo y a nivel municipio-año.
- **Falacia ecológica:** lo que pasa a nivel municipal no se puede trasladar directo a cada estudiante.
- **Sin controles multivariados:** no hice modelos que controlen todo a la vez; varias variables pueden moverse juntas.
- **Sesgo de supervivencia:** el puntaje solo incluye a quienes presentan la prueba.
- **Ruido muestral:** con pocos evaluados o pocos municipios los promedios bailan más.
- **Sensibilidad a filtros:** cambiar el umbral de evaluados o el trato de ceros/>100 puede mover los resultados; por eso dejé excluidos y bases con flags.
- **Comparar años no es perfecto:** repliqué lo esencial en 2019 y 2014-2017, pero las pruebas y el contexto cambian con el tiempo.
