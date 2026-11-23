# Coordinación y pendientes

## Qué dejé listo (Etapa 1)

- **Script (corre completo):** `scripts/analisis_exploratorio.py`
- **Tablas:** `outputs/persona3/tablas/` (`2022/`, `2019/`, `2014_2017/`). En `2022/` está el detalle completo; en `2019/` y `2014_2017/` dejé tablas esenciales para comparar.
- **Figuras:** `outputs/persona3/figuras/` (`2022/`, `2019/`, `2014_2017/`)
- **Control de calidad 2022:** `outputs/persona3/tablas/2022/base_analisis.csv`, `base_2022_con_flags_calidad.csv`, `excluidos_y_motivos.csv`
- **Registro de decisiones:** `docs/persona3/registro_decisiones.md`, `outputs/persona3/registro_decisiones.csv`
- **Resumen base para hallazgos:** `outputs/persona3/resumen_hallazgos_base.csv`
- **Documentos:** `docs/persona3/hallazgos.md`, `docs/persona3/limitaciones.md`, `docs/persona3/recomendaciones.md`

## Para coordinar con Persona 4 (dashboard)

Carpeta propuesta para que el dashboard tome los insumos: **`outputs/persona3/`** (`tablas/` y `figuras/`).

Gráficos de 2022 que pueden servir:
- `outputs/persona3/figuras/2022/distribucion_puntaje_global.png` (distribución general)
- `outputs/persona3/figuras/2022/puntaje_por_ruralidad.png` (por grupos de ruralidad)
- `outputs/persona3/figuras/2022/top15_departamentos_puntaje.png` (contexto territorial; conviene mirar el n en la tabla)
- `outputs/persona3/figuras/2022/puntaje_por_cuartiles_pct_internet_hogar.png` (gradiente por internet ICFES)
- `outputs/persona3/figuras/2022/puntaje_por_cuartiles_cobertura_neta_media.png` (gradiente por cobertura neta media)
- `outputs/persona3/figuras/2022/dispersion_internet_icfes_vs_puntaje.png` y/o `dispersion_ruralidad_vs_puntaje.png` (relación bivariada)

Tablas útiles en `tablas/2022/`: `comparacion_por_departamento.csv`, `comparacion_por_ruralidad.csv`, `comparacion_cuartiles_*.csv`, `comparacion_cruzada_ruralidad_x_internet_media.csv`, `descriptiva_variables_clave.csv` y `excluidos_y_motivos.csv`. Para comparar en el tiempo: `tablas/2019/`, `tablas/2014_2017/` y `outputs/persona3/resumen_hallazgos_base.csv`.

> Vale la pena confirmar con Persona 4 si necesita otros nombres, rutas o algún corte adicional.

## Pendientes de Persona 2

- Queda pendiente lo de **IPM** e **internet de TerriData** según la consigna.
- En `data/procesados/dataset_integrado.csv` ya se ven columnas como `ipm_municipal`, `penetracion_internet_hogares`, `penetracion_internet_fijo`, pero la disponibilidad cambia por año (toca revisar al re-ejecutar).
- Si Persona 2 actualiza eso: correr `python scripts/analisis_exploratorio.py`, revisar `outputs/persona3/resumen_hallazgos_base.csv` y ajustar `docs/persona3/hallazgos.md`, `limitaciones.md` y `recomendaciones.md` si algo cambia.

## Resumen rápido de decisiones

- **2022:** saqué 9 municipios sin puntaje global; excluí `total_evaluados < 30` y valores >100 en variables porcentuales clave del análisis principal; unifiqué nombres de departamento; dejé excluidos y flags en archivos aparte.
- **2019 y 2014-2017:** repliqué lo esencial (periodo 2014-2017 consolidado) con los mismos criterios principales.
- Detalle completo en `docs/persona3/registro_decisiones.md`.
