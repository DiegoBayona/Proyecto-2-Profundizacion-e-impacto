from pathlib import Path
import pandas as pd


# Rutas de entrada y salida

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SALIDA = DATA / "procesados"
SALIDA.mkdir(parents=True, exist_ok=True)

RUTA_MEN = DATA / "MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR,_BÁSICA_Y_MEDIA_POR_MUNICIPIO_20261120.csv"
RUTA_SABER11 = DATA / "Resultados_únicos_Saber_11_20261120.csv"
RUTA_SABER11_REDUCIDO = SALIDA / "saber11_reducido_municipio_anio.csv"
RUTA_TERRI_POBREZA = DATA / "TerriData_pobreza.txt"
RUTA_TERRI_SERVICIOS = DATA / "TerriData_servicios.txt"



# Funciones auxiliares

def estandarizar_codigo_municipio(serie):
    """Pasa el código de municipio/entidad a formato DIVIPOLA de 5 dígitos.

    Deja por fuera códigos inválidos y agregados nacionales/departamentales.
    """
    numerico = pd.to_numeric(serie, errors="coerce")
    # Mantener solo códigos municipales válidos (municipios en Colombia >= 05001)
    numerico = numerico.where(numerico >= 5001)
    codigo = numerico.dropna().astype("int64").astype(str).str.zfill(5)
    # Excluir agregados departamentales/nacionales representados como XXX000
    codigo = codigo.where(~codigo.str.endswith("000"))
    # Reindexar para conservar alineación con la serie original
    return codigo.reindex(serie.index)


def limpiar_porcentaje(serie):
    """Convierte valores con % o coma decimal a número (float)."""
    texto = serie.astype(str).str.strip()
    texto = texto.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NA": pd.NA})
    texto = texto.str.replace("%", "", regex=False)
    texto = texto.str.replace(",", ".", regex=False)
    return pd.to_numeric(texto, errors="coerce")



# 1) Dataset más ligero para Resultados Saber 11

def crear_saber11_ligero():
    """Carga el resumen de Saber 11 por municipio y año.

    Si ya existe el archivo reducido en data/procesados lo reutiliza; si no,
    lo genera desde el archivo original leyéndolo por bloques.
    """
    if RUTA_SABER11_REDUCIDO.exists():
        print(f"Usando dataset reducido de Saber 11 existente: {RUTA_SABER11_REDUCIDO}")
        saber11 = pd.read_csv(RUTA_SABER11_REDUCIDO)
        # Asegurar tipos consistentes para la integración
        saber11["codigo_municipio"] = estandarizar_codigo_municipio(saber11["codigo_municipio"])
        saber11 = saber11.dropna(subset=["codigo_municipio", "anio"])
        saber11["anio"] = pd.to_numeric(saber11["anio"], errors="coerce").astype(int)
        return saber11

    if not RUTA_SABER11.exists():
        raise FileNotFoundError(
            "No se encontró la versión reducida de Saber 11 ni el archivo original grande. "
            f"Esperado reducido en: {RUTA_SABER11_REDUCIDO} o original en: {RUTA_SABER11}"
        )

    print("Creando dataset ligero de Saber 11 desde el archivo original...")

    columnas_utiles = [
        "PERIODO",
        "COLE_COD_MCPIO_UBICACION",  # llave de unión en Saber 11
        "COLE_AREA_UBICACION",
        "FAMI_TIENEINTERNET",
        "PUNT_GLOBAL",
        "PUNT_MATEMATICAS",
        "PUNT_LECTURA_CRITICA",
        "PUNT_INGLES",
    ]

    partes = []
    tam_bloque = 300000

    for bloque in pd.read_csv(RUTA_SABER11, usecols=columnas_utiles, chunksize=tam_bloque, low_memory=False):
        # Año a partir del periodo (ej. 20224 -> 2022)
        bloque["anio"] = pd.to_numeric(bloque["PERIODO"].astype(str).str[:4], errors="coerce")
        bloque = bloque.dropna(subset=["anio"])
        bloque["anio"] = bloque["anio"].astype(int)

        # Llave de unión estandarizada (5 dígitos)
        bloque["codigo_municipio"] = estandarizar_codigo_municipio(bloque["COLE_COD_MCPIO_UBICACION"])

        # Puntajes numéricos
        cols_puntaje = ["PUNT_GLOBAL", "PUNT_MATEMATICAS", "PUNT_LECTURA_CRITICA", "PUNT_INGLES"]
        for col in cols_puntaje:
            bloque[col] = pd.to_numeric(bloque[col], errors="coerce")

        # Filtrar registros válidos para agregación
        bloque = bloque.dropna(subset=["codigo_municipio", "PUNT_GLOBAL"])

        # Indicadores binarios para porcentajes
        bloque["es_rural"] = bloque["COLE_AREA_UBICACION"].astype(str).str.upper().str.strip().eq("RURAL").astype(int)
        bloque["tiene_internet"] = bloque["FAMI_TIENEINTERNET"].astype(str).str.upper().str.strip().eq("SI").astype(int)

        # Agregación parcial por municipio-año dentro del bloque
        resumen = bloque.groupby(["codigo_municipio", "anio"], as_index=False).agg(
            total_evaluados=("PUNT_GLOBAL", "count"),
            suma_global=("PUNT_GLOBAL", "sum"),
            suma_matematicas=("PUNT_MATEMATICAS", "sum"),
            suma_lectura=("PUNT_LECTURA_CRITICA", "sum"),
            suma_ingles=("PUNT_INGLES", "sum"),
            total_rural=("es_rural", "sum"),
            total_internet=("tiene_internet", "sum"),
        )
        partes.append(resumen)

    # Consolidar todos los bloques
    saber11 = pd.concat(partes, ignore_index=True)
    cols_suma = [
        "total_evaluados", "suma_global", "suma_matematicas",
        "suma_lectura", "suma_ingles", "total_rural", "total_internet",
    ]
    saber11 = saber11.groupby(["codigo_municipio", "anio"], as_index=False)[cols_suma].sum()

    # Promedios y porcentajes municipales
    saber11["punt_global_prom"] = saber11["suma_global"] / saber11["total_evaluados"]
    saber11["punt_matematicas_prom"] = saber11["suma_matematicas"] / saber11["total_evaluados"]
    saber11["punt_lectura_prom"] = saber11["suma_lectura"] / saber11["total_evaluados"]
    saber11["punt_ingles_prom"] = saber11["suma_ingles"] / saber11["total_evaluados"]
    saber11["pct_evaluados_rural"] = (saber11["total_rural"] / saber11["total_evaluados"]) * 100
    saber11["pct_internet_hogar"] = (saber11["total_internet"] / saber11["total_evaluados"]) * 100

    columnas_finales = [
        "codigo_municipio", "anio", "total_evaluados",
        "punt_global_prom", "punt_matematicas_prom", "punt_lectura_prom", "punt_ingles_prom",
        "pct_evaluados_rural", "pct_internet_hogar",
    ]
    saber11 = saber11[columnas_finales].sort_values(["anio", "codigo_municipio"]).reset_index(drop=True)

    ruta_salida = RUTA_SABER11_REDUCIDO
    saber11.to_csv(ruta_salida, index=False)
    print(f"Saber 11 ligero guardado en: {ruta_salida} (filas: {len(saber11)})")
    return saber11



# 2) Limpieza de datasets en data/

def limpiar_men():
    """Limpia el archivo del MEN y deja la llave CÓDIGO_MUNICIPIO lista para el cruce."""
    print("Limpiando dataset MEN...")
    men = pd.read_csv(RUTA_MEN, low_memory=False)

    # Llave de unión estandarizada
    men["codigo_municipio"] = estandarizar_codigo_municipio(men["CÓDIGO_MUNICIPIO"])
    men = men.dropna(subset=["codigo_municipio"]).copy()

    # Año y nombres básicos
    men["anio"] = pd.to_numeric(men["AÑO"], errors="coerce")
    men = men.dropna(subset=["anio"])
    men["anio"] = men["anio"].astype(int)

    # Selección de variables útiles (se incluyen solo las que existan)
    columnas_base = ["codigo_municipio", "anio", "MUNICIPIO", "DEPARTAMENTO"]
    columnas_indicadores = [
        "POBLACIÓN_5_16", "TASA_MATRICULACIÓN_5_16",
        "COBERTURA_NETA", "COBERTURA_NETA_MEDIA", "COBERTURA_BRUTA", "COBERTURA_BRUTA_MEDIA",
        "DESERCIÓN", "DESERCIÓN_MEDIA", "APROBACIÓN", "APROBACIÓN_MEDIA",
        "REPROBACIÓN", "REPROBACIÓN_MEDIA", "REPITENCIA", "REPITENCIA_MEDIA",
        "SEDES_CONECTADAS_A_INTERNET",
    ]
    columnas_presentes = columnas_base + [c for c in columnas_indicadores if c in men.columns]
    men = men[columnas_presentes].copy()

    # Conversión de porcentajes/valores a numérico
    for col in men.columns:
        if col in ["codigo_municipio", "anio", "MUNICIPIO", "DEPARTAMENTO"]:
            continue
        men[col] = limpiar_porcentaje(men[col])

    # Eliminar duplicados por municipio-año conservando el primer registro
    men = men.drop_duplicates(subset=["codigo_municipio", "anio"]).sort_values(["anio", "codigo_municipio"])
    men = men.reset_index(drop=True)

    ruta_salida = SALIDA / "men_limpio.csv"
    men.to_csv(ruta_salida, index=False)
    print(f"MEN limpio guardado en: {ruta_salida} (filas: {len(men)})")
    return men


def limpiar_terridata(ruta_entrada, nombre_salida):
    """Limpia un archivo TerriData (txt separado por '|') y guarda una versión nueva."""
    print(f"Limpiando TerriData: {ruta_entrada.name}...")
    df = pd.read_csv(ruta_entrada, sep="|", encoding="utf-8-sig", dtype=str, low_memory=False)

    # Código de entidad como llave municipal
    df["codigo_municipio"] = estandarizar_codigo_municipio(df["Código Entidad"])
    df = df.dropna(subset=["codigo_municipio"]).copy()

    # Año y valor numérico
    df["anio"] = pd.to_numeric(df.get("Año"), errors="coerce")
    df = df.dropna(subset=["anio"])
    df["anio"] = df["anio"].astype(int)

    dato = df.get("Dato Numérico", pd.Series([pd.NA] * len(df)))
    df["dato_numerico"] = limpiar_porcentaje(dato)

    columnas = [
        "codigo_municipio", "Código Entidad", "Entidad", "Departamento",
        "Dimensión", "Subcategoría", "Indicador", "anio", "dato_numerico",
        "Unidad de Medida", "Fuente",
    ]
    columnas_presentes = [c for c in columnas if c in df.columns]
    df = df[columnas_presentes].copy()

    # Quitar filas sin indicador
    if "Indicador" in df.columns:
        df = df[df["Indicador"].notna() & (df["Indicador"].astype(str).str.strip() != "")]

    df = df.sort_values(["codigo_municipio", "anio"]).reset_index(drop=True)
    ruta_salida = SALIDA / nombre_salida
    df.to_csv(ruta_salida, index=False)
    print(f"TerriData limpio guardado en: {ruta_salida} (filas: {len(df)})")
    return df


def preparar_terridata_para_integracion(pobreza_limpio, servicios_limpio):
    """Saca de TerriData las variables que se van a usar en el dataset integrado."""
    print("Preparando variables útiles de TerriData para integración...")
    print("Preparando variables útiles de TerriData para integración...")

    # IPM municipal (variable estructural, sin depender de un solo año)
    ipm = pobreza_limpio[pobreza_limpio["Indicador"].astype(str).str.contains(
        "pobreza multidimensional", case=False, na=False
    )].copy()
    ipm_municipal = (
        ipm.dropna(subset=["dato_numerico"])
        .groupby("codigo_municipio", as_index=False)["dato_numerico"]
        .mean()
        .rename(columns={"dato_numerico": "ipm_municipal"})
    )

    # Indicadores de servicios útiles (anuales)
    indicadores_servicios = [
        "Penetración de acceso fijo a Internet",
        "Penetración de internet fijo en los hogares",
        "Cobertura de energía eléctrica rural",
        "Cobertura de acueducto (REC)",
        "Cobertura de alcantarillado (REC)",
    ]
    serv = servicios_limpio[servicios_limpio["Indicador"].isin(indicadores_servicios)].copy()
    serv = serv.dropna(subset=["dato_numerico"])
    serv_wide = serv.pivot_table(
        index=["codigo_municipio", "anio"],
        columns="Indicador",
        values="dato_numerico",
        aggfunc="mean",
    ).reset_index()

    # Renombrar columnas de indicadores a nombres simples
    renombres = {
        "Penetración de acceso fijo a Internet": "penetracion_internet_fijo",
        "Penetración de internet fijo en los hogares": "penetracion_internet_hogares",
        "Cobertura de energía eléctrica rural": "cobertura_energia_rural",
        "Cobertura de acueducto (REC)": "cobertura_acueducto",
        "Cobertura de alcantarillado (REC)": "cobertura_alcantarillado",
    }
    serv_wide = serv_wide.rename(columns=renombres)

    return ipm_municipal, serv_wide



# 3) Integración de datasets

def integrar_datasets(men, saber11, ipm_municipal, terri_servicios_wide):
    """Une MEN, Saber 11 y TerriData por municipio (y año cuando aplica)."""
    print("Integrando datasets...")
    print("Integrando datasets...")

    # Base: registros municipio-año de MEN (cobertura amplia de municipios y años)
    integrado = men.merge(saber11, on=["codigo_municipio", "anio"], how="left")
    integrado = integrado.merge(terri_servicios_wide, on=["codigo_municipio", "anio"], how="left")
    integrado = integrado.merge(ipm_municipal, on="codigo_municipio", how="left")

    # Variable útil adicional: brecha del puntaje global frente al promedio nacional del año
    if "punt_global_prom" in integrado.columns:
        promedio_nacional = integrado.groupby("anio")["punt_global_prom"].transform("mean")
        integrado["brecha_punt_global_vs_nacional"] = integrado["punt_global_prom"] - promedio_nacional

    integrado = integrado.sort_values(["anio", "DEPARTAMENTO", "MUNICIPIO"]).reset_index(drop=True)

    ruta_salida = SALIDA / "dataset_integrado.csv"
    integrado.to_csv(ruta_salida, index=False)

    print(f"Dataset integrado guardado en: {ruta_salida} (filas: {len(integrado)})")
    print("Municipios únicos:", integrado["codigo_municipio"].nunique())
    if "punt_global_prom" in integrado.columns:
        sin_saber11 = integrado["punt_global_prom"].isna().mean() * 100
        print(f"Registros sin cruce con Saber 11: {sin_saber11:.1f}%")
    if "ipm_municipal" in integrado.columns:
        sin_ipm = integrado["ipm_municipal"].isna().mean() * 100
        print(f"Registros sin cruce con IPM: {sin_ipm:.1f}%")

    return integrado



# Ejecución 

def main():
    saber11_ligero = crear_saber11_ligero()
    men_limpio = limpiar_men()
    pobreza_limpio = limpiar_terridata(RUTA_TERRI_POBREZA, "terridata_pobreza_limpio.csv")
    servicios_limpio = limpiar_terridata(RUTA_TERRI_SERVICIOS, "terridata_servicios_limpio.csv")
    ipm_municipal, terri_servicios_wide = preparar_terridata_para_integracion(pobreza_limpio, servicios_limpio)
    integrar_datasets(men_limpio, saber11_ligero, ipm_municipal, terri_servicios_wide)
    print("\nProceso completado. Archivos nuevos disponibles en data/procesados/")


if __name__ == "__main__":
    main()
