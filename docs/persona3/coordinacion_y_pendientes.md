# Coordinación y pendientes - Persona 3

## Entregables generados (Etapa 1)

- **Script ejecutable de principio a fin:** `scripts/analisis_exploratorio.py`
- **Tablas:** `outputs/persona3/tablas/` (subcarpetas `2022/`, `2019/`, `2014_2017/` y `2014_2017/<anio>/`)
- **Figuras:** `outputs/persona3/figuras/` (subcarpetas `2022/`, `2019/`, `2014_2017/` y `2014_2017/<anio>/`)
- **Bases y control de calidad (2022):** `outputs/persona3/tablas/2022/base_analisis.csv`, `base_2022_con_flags_calidad.csv`, `excluidos_y_motivos.csv`
- **Registro de decisiones:** `docs/persona3/registro_decisiones.md`, `outputs/persona3/registro_decisiones.csv`
- **Resumen cuantitativo base para hallazgos:** `outputs/persona3/resumen_hallazgos_base.csv`
- **Documentos analíticos:** `docs/persona3/hallazgos.md`, `docs/persona3/limitaciones.md`, `docs/persona3/recomendaciones.md`

## Coordinación con Persona 4 (dashboard)

Carpeta acordada/propuesta para consumo del dashboard: **`outputs/persona3/`** (tablas en `tablas/`, figuras en `figuras/`).

Gráficos sugeridos para dashboard (corte 2022, claros y trazables):
- `outputs/persona3/figuras/2022/distribucion_puntaje_global.png` — distribución general del puntaje municipal.
- `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png` — comparación por grupos de ruralidad.
- `outputs/persona3/figuras/2022/top15_departamentos_puntaje.png` — contexto territorial (con nota de n por departamento en tabla).
- `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png` — gradiente por internet ICFES.
- `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png` — gradiente por cobertura neta media.
- `outputs/persona3/figuras/2022/dispersion_internet_icfes_vs_puntaje.png` y/o `dispersion_ruralidad_vs_puntaje.png` — relación bivariada (complementarias).

Tablas recomendadas para soporte/filtros en dashboard: `comparacion_por_departamento.csv`, `comparacion_por_ruralidad.csv`, `comparacion_cuartiles_*.csv`, `comparacion_cruzada_ruralidad_x_internet_media.csv`, `descriptiva_variables_clave.csv` y `excluidos_y_motivos.csv` (para transparencia).

> Nota: confirmar con Persona 4 si requiere nombres/rutas específicas o versiones adicionales (p. ej. 2019/2014-2017) para comparabilidad temporal.

## Pendientes de Persona 2 y actualización

- Pendiente indicado en la consigna: resolución/actualización de **IPM** e **internet de TerriData** por Persona 2.
- Estado actual observado en `data/procesados/dataset_integrado.csv`: existen columnas `ipm_municipal`, `penetracion_internet_hogares`, `penetracion_internet_fijo`; su disponibilidad varía por año (revisar al re-ejecutar).
- Acción al recibir actualización: re-ejecutar `python scripts/analisis_exploratorio.py`, revisar `outputs/persona3/resumen_hallazgos_base.csv` y actualizar `docs/persona3/hallazgos.md`, `limitaciones.md` y `recomendaciones.md` si cambian patrones o cobertura.

## Decisiones clave aplicadas (resumen)

- 2022: excluidos 9 municipios sin puntaje global; exclusión de `total_evaluados < 30` y valores >100 en variables porcentuales clave del análisis principal; unificación de nombres de departamento; exclusiones y flags conservados en archivos de control.
- Replicación esencial: 2019 y 2014-2017 con mismos criterios principales de filtrado por puntaje, tamaño muestral y rangos >100.
- Detalle completo: `docs/persona3/registro_decisiones.md`.
