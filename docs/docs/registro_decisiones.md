# Registro de decisiones

Acá dejo los filtros y criterios que usé en la Etapa 1, con el porqué y cómo cambió el número de filas.

| Corte | Tema | Decisión | Razón/Detalle | N antes | N después |
|---|---|---|---|---:|---:|
| global | columnas | Ajuste de nombres de columnas (encoding raro) | {"codigo_municipio": "codigo_municipio", "anio": "anio", "municipio": "MUNICIPIO", "departamento": "DEPARTAMENTO", "punt_global_prom": "punt_global_prom", "total_evaluados": "total_evaluados", "desercion_media": "DESERCIÓN_MEDIA", "cobertura_neta_media": "COBERTURA_NETA_MEDIA", "pct_internet_hogar": "pct_internet_hogar", "pct_evaluados_rural": "pct_evaluados_rural", "ipm_municipal": "ipm_municipal", "penetracion_internet_hogares": "penetracion_internet_hogares", "penetracion_internet_fijo": "penetracion_internet_fijo", "brecha_vs_nacional": "brecha_punt_global_vs_nacional"} |  |  |
| global | pendientes_persona2 | Pendiente: IPM/internet TerriData si Persona 2 actualiza la fuente | Si cambian esos datos, toca volver a correr el script para que entren en las tablas/gráficos. |  |  |
| 2022 | corte_año | Filtrar año 2022 | Me quedo solo con filas de 2022. | 15704 | 1121 |
| 2022 | sin_puntaje | Sacar municipios sin puntaje global | Se sacan 9 filas sin punt_global_prom. | 1121 | 1112 |
| 2022 | departamentos | Unificar nombres de departamento | Ajuste de nombres/variantes para que no queden duplicados raros. Únicos antes/después: 33/33. | 1121 | 1112 |
| 2022 | municipios_pequenos | Sacar del análisis principal municipios con menos de 30 evaluados | Con pocos evaluados el dato baila mucho; los dejo guardados aparte por si toca revisar sensibilidad. | 1112 | 1035 |
| 2022 | valores_sospechosos | Sacar valores >100 en cobertura, internet ICFES, ruralidad y deserción | Porcentajes por encima de 100 no tienen mucho sentido aquí; los ceros de deserción los traté como sospechosos según la regla definida arriba. | 1112 | 1035 |
| 2019 | sin_puntaje | Quitar filas sin puntaje global | Quité 10 de 1122. | 1122 | 1112 |
| 2019 | municipios_pequenos | Quitar municipios con menos de 30 evaluados | Quité 12 de 1112. | 1112 | 1100 |
| 2019 | gt100_cobertura_neta_media | Quitar cobertura_neta_media > 100 | Quité 4 filas. | 1100 | 1096 |
| 2014_2017 | sin_puntaje | Quitar filas sin puntaje global | Quité 18 de 1122. | 1122 | 1104 |
| 2014_2017 | municipios_pequenos | Quitar municipios con menos de 30 evaluados | Quité 58 de 1104. | 1104 | 1046 |
| 2014_2017 | sin_puntaje | Quitar filas sin puntaje global | Quité 14 de 1122. | 1122 | 1108 |
| 2014_2017 | municipios_pequenos | Quitar municipios con menos de 30 evaluados | Quité 64 de 1108. | 1108 | 1044 |
| 2014_2017 | sin_puntaje | Quitar filas sin puntaje global | Quité 12 de 1122. | 1122 | 1110 |
| 2014_2017 | municipios_pequenos | Quitar municipios con menos de 30 evaluados | Quité 80 de 1110. | 1110 | 1030 |
| 2014_2017 | gt100_cobertura_neta_media | Quitar cobertura_neta_media > 100 | Quité 5 filas. | 1030 | 1025 |
| 2014_2017 | sin_puntaje | Quitar filas sin puntaje global | Quité 11 de 1122. | 1122 | 1111 |
| 2014_2017 | municipios_pequenos | Quitar municipios con menos de 30 evaluados | Quité 70 de 1111. | 1111 | 1041 |
| 2014_2017 | gt100_cobertura_neta_media | Quitar cobertura_neta_media > 100 | Quité 4 filas. | 1041 | 1037 |
