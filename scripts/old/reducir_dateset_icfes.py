import pandas as pd
import numpy as np
from pathlib import Path

# Detecta automáticamente la raíz del proyecto sin importar desde dónde se ejecute
raiz_proyecto = Path(__file__).resolve().parent.parent


def estandarizar_divipola(serie):
    """Convierte códigos DIVIPOLA (ej. 5001 o 5001.0) a texto de 5 dígitos ('05001')."""
    numerico = pd.to_numeric(serie, errors='coerce')
    return numerico.dropna().astype(int).astype(str).str.zfill(5)

ruta_icfes = raiz_proyecto / 'data' / 'Resultados_únicos_Saber_11_20261120.csv'


# Leer solo las 8 columnas necesarias 
columnas_icfes = [
    'PERIODO',
    'COLE_COD_MCPIO_UBICACION',
    'COLE_AREA_UBICACION',
    'FAMI_TIENEINTERNET',
    'PUNT_GLOBAL',
    'PUNT_MATEMATICAS',
    'PUNT_LECTURA_CRITICA'
]

acumulado_chunks = []

for chunk in pd.read_csv(ruta_icfes, usecols=columnas_icfes, chunksize=250_000, low_memory=False):
    # Extraer año de los primeros 4 dígitos de PERIODO (ej. 20231 -> 2023)
    chunk['anio'] = pd.to_numeric(chunk['PERIODO'].astype(str).str[:4], errors='coerce')
    chunk = chunk[chunk['anio'].between(2020, 2023)].copy()
    chunk['anio'] = chunk['anio'].astype(int)

    if chunk.empty:
        continue

    # Asegurar tipos numéricos en puntajes para evitar errores al agregar
    cols_punt = ['PUNT_GLOBAL', 'PUNT_MATEMATICAS', 'PUNT_LECTURA_CRITICA']
    chunk[cols_punt] = chunk[cols_punt].apply(pd.to_numeric, errors='coerce')

    # Limpiar llave municipal y puntaje global
    chunk = chunk.dropna(subset=['COLE_COD_MCPIO_UBICACION', 'PUNT_GLOBAL']).copy()
    chunk['codigo_divipola'] = estandarizar_divipola(chunk['COLE_COD_MCPIO_UBICACION'])
    chunk = chunk.dropna(subset=['codigo_divipola'])
    
    

    # Crear indicadores binarios (1 o 0) para sacar porcentajes después
    chunk['es_rural'] = chunk['COLE_AREA_UBICACION'].astype(str).str.upper().str.strip().eq('RURAL').astype(int)
    chunk['tiene_internet'] = chunk['FAMI_TIENEINTERNET'].astype(str).str.upper().str.strip().eq('SI').astype(int)

    # Agregar sumas y conteos dentro del bloque
    agg_chunk = chunk.groupby(['codigo_divipola', 'anio'], as_index=False).agg(
        total_evaluados=('PUNT_GLOBAL', 'count'),
        suma_global=('PUNT_GLOBAL', 'sum'),
        suma_matematicas=('PUNT_MATEMATICAS', 'sum'),
        suma_lectura=('PUNT_LECTURA_CRITICA', 'sum'),
        total_rural=('es_rural', 'sum'),
        total_internet=('tiene_internet', 'sum')
    )
    acumulado_chunks.append(agg_chunk)

# Consolidar todos los bloques y calcular los promedios municipales exactos
icfes_mun = pd.concat(acumulado_chunks, ignore_index=True)
cols_num = [
    'total_evaluados',
    'suma_global',
    'suma_matematicas',
    'suma_lectura',
    'total_rural',
    'total_internet',
]
icfes_mun = icfes_mun.groupby(['codigo_divipola', 'anio'], as_index=False)[cols_num].sum()

icfes_mun['punt_global_prom'] = icfes_mun['suma_global'] / icfes_mun['total_evaluados']
icfes_mun['punt_matematicas_prom'] = icfes_mun['suma_matematicas'] / icfes_mun['total_evaluados']
icfes_mun['punt_lectura_prom'] = icfes_mun['suma_lectura'] / icfes_mun['total_evaluados']
icfes_mun['pct_evaluados_rural'] = (icfes_mun['total_rural'] / icfes_mun['total_evaluados']) * 100
icfes_mun['pct_internet_hogar'] = (icfes_mun['total_internet'] / icfes_mun['total_evaluados']) * 100

# Guardar versión ligera 
cols_finales_icfes = [
    'codigo_divipola', 'anio', 'total_evaluados',
    'punt_global_prom', 'punt_matematicas_prom', 'punt_lectura_prom',
    'pct_evaluados_rural', 'pct_internet_hogar'
]
icfes_mun = icfes_mun[cols_finales_icfes]
ruta_salida = raiz_proyecto / 'data' / 'icfes_limpio_2020_2023.csv'
icfes_mun.to_csv(ruta_salida, index=False)

print("Años procesados:", sorted(icfes_mun['anio'].unique()))
print("Filas totales (municipio-año):", len(icfes_mun))
print(icfes_mun.head())

