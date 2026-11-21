import pandas as pd
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parent.parent


# Función para dejar todos los códigos municipales con 5 dígitos (ej. '05001')
def limpiar_codigo(columna):
    nums = pd.to_numeric(columna, errors='coerce')
    nums = nums.where(nums >= 5001)  # Quita códigos de país (0) o departamento (5, 8, etc.)
    return nums.dropna().astype(int).astype(str).str.zfill(5)

ruta_icfes = raiz_proyecto / 'data' / 'Resultados_únicos_Saber_11_20261120.csv'

columnas = [
    'PERIODO',
    'COLE_COD_MCPIO_UBICACION',
    'COLE_AREA_UBICACION',
    'FAMI_TIENEINTERNET',
    'PUNT_GLOBAL',
    'PUNT_MATEMATICAS',
    'PUNT_LECTURA_CRITICA'
]

partes = []

# Leemos de a 300.000 filas para no saturar la memoria RAM
for bloque in pd.read_csv(ruta_icfes, usecols=columnas, chunksize=300000, low_memory=False):
    # Nos quedamos solo con los exámenes de 2022 (periodos 20221 y 20224)
    bloque = bloque[bloque['PERIODO'].astype(str).str.startswith('2022')].copy()
    
    if bloque.empty:
        continue

    bloque['codigo_divipola'] = limpiar_codigo(bloque['COLE_COD_MCPIO_UBICACION'])
    bloque = bloque.dropna(subset=['codigo_divipola', 'PUNT_GLOBAL'])

    # Convertimos texto a 1 y 0 para poder sumar y sacar porcentajes
    bloque['es_rural'] = (bloque['COLE_AREA_UBICACION'] == 'RURAL').astype(int)
    bloque['tiene_internet'] = (bloque['FAMI_TIENEINTERNET'] == 'Si').astype(int)

    # Agrupamos este bloque por municipio
    resumen = bloque.groupby('codigo_divipola', as_index=False).agg(
        total_evaluados=('PUNT_GLOBAL', 'count'),
        suma_global=('PUNT_GLOBAL', 'sum'),
        suma_matematicas=('PUNT_MATEMATICAS', 'sum'),
        suma_lectura=('PUNT_LECTURA_CRITICA', 'sum'),
        total_rural=('es_rural', 'sum'),
        total_internet=('tiene_internet', 'sum')
    )
    partes.append(resumen)

# Unimos todas las partes y calculamos los promedios finales por municipio
icfes = pd.concat(partes, ignore_index=True)
icfes = icfes.groupby('codigo_divipola', as_index=False).sum()

icfes['punt_global_prom'] = icfes['suma_global'] / icfes['total_evaluados']
icfes['punt_matematicas_prom'] = icfes['suma_matematicas'] / icfes['total_evaluados']
icfes['punt_lectura_prom'] = icfes['suma_lectura'] / icfes['total_evaluados']
icfes['pct_evaluados_rural'] = (icfes['total_rural'] / icfes['total_evaluados']) * 100
icfes['pct_internet_hogar'] = (icfes['total_internet'] / icfes['total_evaluados']) * 100

# Nos quedamos solo con las columnas finales y guardamos
columnas_finales = [
    'codigo_divipola', 'total_evaluados', 'punt_global_prom',
    'punt_matematicas_prom', 'punt_lectura_prom',
    'pct_evaluados_rural', 'pct_internet_hogar'
]
icfes = icfes[columnas_finales]
icfes.to_csv('../data/icfes_2022_limpio.csv', index=False)

print("Municipios guardados:", len(icfes))