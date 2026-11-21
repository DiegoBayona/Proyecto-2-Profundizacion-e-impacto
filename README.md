# Proyecto 2 - Relación entre resultados de SABER 11 y condiciones territoriales por municipio

Proyecto para preparar y analizar datos educativos y territoriales de Colombia a nivel municipal.

## Datos de entrada (`data/`)
- **MEN**: estadísticas de educación en preescolar, básica y media por municipio (`MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR,_BÁSICA_Y_MEDIA_POR_MUNICIPIO_20261120.csv`).  
  Fuente: [datos.gov.co - MEN estadísticas en educación](https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/nudc-7mev/about_data)
- **Resultados Saber 11**: resultados por estudiante (`Resultados_únicos_Saber_11_20261120.csv`, archivo pesado) o su versión reducida ya procesada.  
  Fuente: [datos.gov.co - Resultados únicos Saber 11](https://www.datos.gov.co/Educaci-n/Resultados-nicos-Saber-11/kgxf-xxbe/about_data)
- **TerriData**:
  - `TerriData_pobreza.txt`
  - `TerriData_servicios.txt`  
  Fuente: [TerriData DNP - Descargas](https://terridata.dnp.gov.co/index-app.html#/descargas)

## Procesamiento realizado
El script [scripts/procesar_datasets.py](scripts/procesar_datasets.py) (solo con `pandas`) hace lo siguiente:
1. **Saber 11 más ligero**: crea o reutiliza una versión agregada por municipio y año (no es obligatorio tener el archivo grande si ya existe la versión reducida).
2. **Limpieza de datasets**: estandariza códigos municipales, convierte porcentajes/valores a numéricos y selecciona variables útiles de MEN y TerriData.
3. **Integración**: genera un dataset integrado por municipio y año.

**Llaves de unión usadas:**
- MEN: `CÓDIGO_MUNICIPIO`
- Saber 11: `COLE_COD_MCPIO_UBICACION`
- TerriData (ambos): `Código Entidad`

## Archivos generados (`data/procesados/`)
- `saber11_reducido_municipio_anio.csv`: Saber 11 agregado por municipio y año.
- `men_limpio.csv`: MEN limpio.
- `terridata_pobreza_limpio.csv`: TerriData de pobreza limpio.
- `terridata_servicios_limpio.csv`: TerriData de servicios limpio.
- `dataset_integrado.csv`: dataset final integrado con variables útiles.

> Los archivos originales en `data/` no se modifican; el procesamiento crea archivos nuevos en `data/procesados/`.

## Cómo ejecutar
Desde la raíz del proyecto:

```bash
python3 scripts/procesar_datasets.py
```

Si ya existe `data/procesados/saber11_reducido_municipio_anio.csv`, el script lo usará directamente sin necesidad del dataset grande de Saber 11.

