# Registro de decisiones - Persona 3

Cada filtro, criterio y exclusión aplicado en Etapa 1, con su razón.

| Corte | Tema | Decisión | Razón/Detalle | N antes | N después |
|---|---|---|---|---:|---:|
| global | columnas | Resolver nombres de columnas con codificación irregular | {"codigo_municipio": "codigo_municipio", "anio": "anio", "municipio": "MUNICIPIO", "departamento": "DEPARTAMENTO", "punt_global_prom": "punt_global_prom", "total_evaluados": "total_evaluados", "desercion_media": "DESERCIÓN_MEDIA", "cobertura_neta_media": "COBERTURA_NETA_MEDIA", "pct_internet_hogar": "pct_internet_hogar", "pct_evaluados_rural": "pct_evaluados_rural", "ipm_municipal": "ipm_municipal", "penetracion_internet_hogares": "penetracion_internet_hogares", "penetracion_internet_fijo": "penetracion_internet_fijo", "brecha_vs_nacional": "brecha_punt_global_vs_nacional"} |  |  |
| global | pendientes_persona2 | Incorporación pendiente IPM/internet TerriData si Persona 2 actualiza fuente | dataset_integrado ya incluye ipm_municipal y variables TerriData cuando existen; re-ejecutar script tras actualización para incorporarlas al análisis. |  |  |
| 2022 | corte_año | Filtrar año 2022 | Se seleccionan registros con anio==2022. | 15704 | 1121 |
| 2022 | sin_puntaje | Excluir municipios sin puntaje global | Se excluyen 9 registros con punt_global_prom nulo. | 1121 | 1112 |
| 2022 | departamentos | Unificar nombres de departamento | Normalización de nombres/variantes. Departamentos únicos antes/después: 33/33. | 1121 | 1112 |
| 2022 | municipios_pequenos | Excluir municipios con menos de 30 evaluados del análisis principal | Regla por ruido muestral; excluidos conservados para sensibilidad. | 1112 | 1035 |
| 2022 | valores_sospechosos | Excluir >100 en cobertura_neta_media, internet ICFES, ruralidad y deserción | Valores fuera de rango porcentual esperable para comparación principal; ceros de deserción tratados como sospechosos según regla. | 1112 | 1035 |
| 2019 | sin_puntaje | Excluir registros sin puntaje global | Excluidos 10 de 1122. | 1122 | 1112 |
| 2019 | municipios_pequenos | Excluir total_evaluados < 30 | Excluidos 12 de 1112. | 1112 | 1100 |
| 2019 | gt100_cobertura_neta_media | Excluir cobertura_neta_media > 100 | Excluidos 4 registros. | 1100 | 1096 |
| 2014_2017 | sin_puntaje | Excluir registros sin puntaje global | Excluidos 18 de 1122. | 1122 | 1104 |
| 2014_2017 | municipios_pequenos | Excluir total_evaluados < 30 | Excluidos 58 de 1104. | 1104 | 1046 |
| 2014_2017 | sin_puntaje | Excluir registros sin puntaje global | Excluidos 14 de 1122. | 1122 | 1108 |
| 2014_2017 | municipios_pequenos | Excluir total_evaluados < 30 | Excluidos 64 de 1108. | 1108 | 1044 |
| 2014_2017 | sin_puntaje | Excluir registros sin puntaje global | Excluidos 12 de 1122. | 1122 | 1110 |
| 2014_2017 | municipios_pequenos | Excluir total_evaluados < 30 | Excluidos 80 de 1110. | 1110 | 1030 |
| 2014_2017 | gt100_cobertura_neta_media | Excluir cobertura_neta_media > 100 | Excluidos 5 registros. | 1030 | 1025 |
| 2014_2017 | sin_puntaje | Excluir registros sin puntaje global | Excluidos 11 de 1122. | 1122 | 1111 |
| 2014_2017 | municipios_pequenos | Excluir total_evaluados < 30 | Excluidos 70 de 1111. | 1111 | 1041 |
| 2014_2017 | gt100_cobertura_neta_media | Excluir cobertura_neta_media > 100 | Excluidos 4 registros. | 1041 | 1037 |
