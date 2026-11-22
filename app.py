import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tablero Ejecutivo — Educación y Territorio",
    layout="wide",
)

CARPETAS_PERIODOS = {
    "2014–2017 (Consolidado)": "outputs/persona3/tablas/2014_2017",
    "2019": "outputs/persona3/tablas/2019",
    "2022": "outputs/persona3/tablas/2022",
}

ETIQUETAS_CUARTILES = [
    "Q1 (Bajo)",
    "Q2 (Medio-Bajo)",
    "Q3 (Medio-Alto)",
    "Q4 (Alto)",
]

ORDEN_CUARTILES = {
    "Q1 (Bajo)": 1,
    "Q2 (Medio-Bajo)": 2,
    "Q3 (Medio-Alto)": 3,
    "Q4 (Alto)": 4,
}


def construir_cuartiles(serie_num):
    """Genera cuartiles con etiquetas descriptivas de forma segura."""
    s = pd.to_numeric(serie_num, errors="coerce")
    if s.notna().sum() < 4:
        return None
    try:
        bins_base = pd.qcut(s, q=4, duplicates="drop")
        n_bins = len(bins_base.cat.categories)
        if n_bins == 0:
            return None
        labels = ETIQUETAS_CUARTILES[:n_bins]
        return pd.qcut(s, q=n_bins, labels=labels, duplicates="drop").astype(str)
    except Exception:
        return None


@st.cache_data
def cargar_base(periodo):
    carpeta = CARPETAS_PERIODOS[periodo]
    if periodo == "2014–2017 (Consolidado)":
        for nombre in ["base_analisis_consolidada.csv", "base_analisis.csv"]:
            try:
                return pd.read_csv(carpeta + "/" + nombre)
            except FileNotFoundError:
                pass
        return pd.DataFrame()
    try:
        return pd.read_csv(carpeta + "/base_analisis.csv")
    except FileNotFoundError:
        return pd.DataFrame()


def detectar_columna(df, pistas, preferidas=None):
    """Detecta la columna más adecuada priorizando nombres esperados y coincidencia parcial."""
    if preferidas:
        columnas_exactas_lower = {c.lower().strip(): c for c in df.columns}
        for pref in preferidas:
            clave = pref.lower().strip()
            if clave in columnas_exactas_lower:
                return columnas_exactas_lower[clave]

    columnas_lower = {c.lower(): c for c in df.columns}
    for pista in pistas:
        for col_l, col_real in columnas_lower.items():
            if pista in col_l:
                return col_real
    return None


def valores_limpios_unicos(serie):
    """Devuelve valores únicos limpios y ordenados, priorizando cuartiles si aplica."""
    serie_valida = serie.dropna()
    valores = []
    for val in serie_valida.astype(str).tolist():
        limpio = val.strip()
        if limpio and limpio.lower() not in {"nan", "none", "null"}:
            valores.append(limpio)
    unicos = list(dict.fromkeys(valores))
    return sorted(unicos, key=lambda v: (ORDEN_CUARTILES.get(v, 99), v))


def preparar_barras_destacadas(serie):
    """Separa el valor máximo en una columna para destacarlo con un color más oscuro."""
    serie_limpia = pd.to_numeric(serie, errors="coerce").dropna()
    if serie_limpia.empty:
        return pd.DataFrame()

    valor_max = serie_limpia.max()
    df_plot = pd.DataFrame(index=serie_limpia.index)
    df_plot["Destacada"] = serie_limpia.where(serie_limpia == valor_max)
    df_plot["Otros"] = serie_limpia.where(serie_limpia < valor_max)
    return df_plot


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #0b1614 0%, #10241e 55%, #0c1722 100%);
        color: #f1f5f9;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp label, .stApp p, .stApp span {
        color: #f1f5f9;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #f8fafc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Encabezado estilo reporte ---
st.markdown("## Desempeño Educativo y Factores Territoriales")
st.caption("Panel interactivo de seguimiento por periodo, departamento y condiciones del entorno")

# --- Barra superior con 3 segmentadores tipo Power BI ---
s1, s2, s3 = st.columns(3)

with s1:
    periodo = st.selectbox(
        "1. Periodo",
        list(CARPETAS_PERIODOS.keys()),
        index=len(CARPETAS_PERIODOS) - 1,
    )

df = cargar_base(periodo)

if df.empty:
    st.warning("No se encontraron datos para el periodo seleccionado.")
    st.stop()

col_depto = detectar_columna(
    df,
    ["departamento", "depto", "nom_depto", "dpto"],
    preferidas=["nom_depto", "departamento", "depto", "dpto"],
)
col_rural = detectar_columna(
    df,
    ["rural", "zona", "urbano"],
    preferidas=["pct_evaluados_rural", "zona", "rural", "urbano"],
)
col_puntaje = detectar_columna(
    df,
    ["puntaje", "global", "icfes", "saber"],
    preferidas=["punt_global_prom", "puntaje_global", "puntaje", "global"],
)
col_internet = detectar_columna(
    df,
    ["internet"],
    preferidas=["pct_internet_hogar", "penetracion_internet_hogares", "penetracion_internet_fijo"],
)
col_cobertura = detectar_columna(
    df,
    ["cobertura"],
    preferidas=["COBERTURA_NETA_MEDIA", "cobertura_neta_media", "cobertura"],
)
col_desercion = detectar_columna(
    df,
    ["desercion", "deserción"],
    preferidas=["DESERCIÓN_MEDIA", "DESERCION_MEDIA", "desercion_media", "desercion"],
)

num_cols = df.select_dtypes(include="number").columns.tolist()
if col_puntaje is None and num_cols:
    col_puntaje = num_cols[0]

with s2:
    if col_depto and col_depto in df.columns:
        opciones_depto = ["Todos"] + valores_limpios_unicos(df[col_depto])
        depto_sel = st.selectbox("2. Departamento", opciones_depto)
    else:
        depto_sel = "Todos"
        st.selectbox("2. Departamento", ["No disponible"], disabled=True)

with s3:
    df_work = df.copy()
    opciones_seg3 = []

    if col_rural and col_rural in df_work.columns:
        if pd.api.types.is_numeric_dtype(df_work[col_rural]):
            serie_rural_q = construir_cuartiles(df_work[col_rural])
            if serie_rural_q is not None:
                df_work["_q_ruralidad"] = serie_rural_q
                opciones_seg3.append(("Cuartil Ruralidad", "_q_ruralidad"))
        else:
            cats_rural = valores_limpios_unicos(df_work[col_rural])
            if 1 < len(cats_rural) <= 20:
                opciones_seg3.append(("Ruralidad / Zona", col_rural))

    for label_q, col_orig, alias in [
        ("Cuartil Internet Hogar", col_internet, "_q_internet"),
        ("Cuartil Cobertura", col_cobertura, "_q_cobertura"),
        ("Cuartil Deserción", col_desercion, "_q_desercion"),
    ]:
        if (
            col_orig
            and col_orig in df_work.columns
            and pd.api.types.is_numeric_dtype(df_work[col_orig])
        ):
            serie_q = construir_cuartiles(df_work[col_orig])
            if serie_q is not None:
                df_work[alias] = serie_q
                opciones_seg3.append((label_q, alias))

    if opciones_seg3:
        etiquetas = [x[0] for x in opciones_seg3]
        tipo_seg3 = st.selectbox("3. Segmento temático", etiquetas)
        col_seg3 = dict(opciones_seg3)[tipo_seg3]

        if col_seg3 in df_work.columns:
            if (
                pd.api.types.is_numeric_dtype(df_work[col_seg3])
                and not str(col_seg3).startswith("_q_")
            ):
                q_fallback = construir_cuartiles(df_work[col_seg3])
                if q_fallback is not None:
                    df_work[col_seg3] = q_fallback

            vals_ordenados = valores_limpios_unicos(df_work[col_seg3])
            valores_seg3 = ["Todos"] + vals_ordenados
        else:
            col_seg3 = None
            valores_seg3 = ["Todos"]

        valor_seg3 = st.selectbox("Filtro del segmento", valores_seg3)
    else:
        col_seg3 = None
        valor_seg3 = "Todos"
        st.selectbox("3. Segmento temático", ["No disponible"], disabled=True)

# --- Aplicación dinámica de los 3 segmentadores ---
filtrado = df_work.copy()
if col_depto and col_depto in filtrado.columns and depto_sel != "Todos":
    filtrado = filtrado[filtrado[col_depto].astype(str).str.strip() == str(depto_sel)]
if col_seg3 and col_seg3 in filtrado.columns and valor_seg3 != "Todos":
    filtrado = filtrado[filtrado[col_seg3].astype(str).str.strip() == str(valor_seg3)]

st.divider()

# --- Fila de KPIs reactivos ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Unidades analizadas", f"{len(filtrado):,}")

if col_puntaje and col_puntaje in filtrado.columns and not filtrado.empty:
    serie_puntaje = pd.to_numeric(filtrado[col_puntaje], errors="coerce").dropna()
    k2.metric(
        f"Promedio {col_puntaje}",
        f"{serie_puntaje.mean():.2f}" if not serie_puntaje.empty else "Sin datos",
    )
else:
    k2.metric("Promedio puntaje", "N/A")

candidatos_k3 = [
    col_internet,
    "pct_internet_hogar",
    "penetracion_internet_hogares",
    "penetracion_internet_fijo",
    "SEDES_CONECTADAS_A_INTERNET",
    col_cobertura,
    "COBERTURA_NETA_MEDIA",
    col_rural,
    "pct_evaluados_rural",
]

col_k3 = None
for col in dict.fromkeys([c for c in candidatos_k3 if c]):
    if col in filtrado.columns:
        s = pd.to_numeric(filtrado[col], errors="coerce").dropna()
        if not s.empty:
            col_k3 = col
            break

if col_k3:
    s = pd.to_numeric(filtrado[col_k3], errors="coerce").dropna()
    k3.metric(f"Promedio {col_k3}", f"{s.mean():.1f}%")
else:
    k3.metric("Indicador territorial", "Sin datos")

if col_desercion and col_desercion in filtrado.columns and not filtrado.empty:
    serie_des = pd.to_numeric(filtrado[col_desercion], errors="coerce").dropna()
    if not serie_des.empty:
        k4.metric(f"Promedio {col_desercion}", f"{serie_des.mean():.2f}%")
    else:
        k4.metric(f"Promedio {col_desercion}", "Sin datos")
else:
    k4.metric("Cobertura / Deserción", "N/A")

# --- Gráficos interactivos principales ---
g1, g2 = st.columns(2)

with g1:
    st.subheader("Puntaje promedio por segmento")
    eje_barras = (
        col_seg3
        if (col_seg3 and col_seg3 in filtrado.columns)
        else (col_depto if (col_depto and col_depto in filtrado.columns) else None)
    )

    if eje_barras and col_puntaje and col_puntaje in filtrado.columns and not filtrado.empty:
        df_bar = filtrado.copy()
        df_bar[col_puntaje] = pd.to_numeric(df_bar[col_puntaje], errors="coerce")

        if (
            pd.api.types.is_numeric_dtype(df_bar[eje_barras])
            and not str(eje_barras).startswith("_q_")
        ):
            serie_q_bar = construir_cuartiles(df_bar[eje_barras])
            if serie_q_bar is not None:
                df_bar["_segmento_q"] = serie_q_bar
                eje_barras = "_segmento_q"

        serie_barras = (
            df_bar.dropna(subset=[eje_barras, col_puntaje])
            .groupby(eje_barras, dropna=True)[col_puntaje]
            .mean()
            .sort_values(ascending=False)
            .head(15)
        )
        df_barras_v = preparar_barras_destacadas(serie_barras)
        if not df_barras_v.empty:
            st.bar_chart(
                df_barras_v,
                color=["#1E3A8A", "#93C5FD"],
                height=340,
            )
        else:
            st.info("Sin datos suficientes para graficar barras.")
    else:
        st.info("Sin datos suficientes para graficar barras.")

with g2:
    st.subheader("Relación entre factor territorial y puntaje")
    candidatos_base_x = [
        col_internet,
        "pct_internet_hogar",
        "penetracion_internet_hogares",
        "penetracion_internet_fijo",
        col_desercion,
        "DESERCIÓN_MEDIA",
        col_cobertura,
        "COBERTURA_NETA_MEDIA",
        col_rural,
        "pct_evaluados_rural",
        "SEDES_CONECTADAS_A_INTERNET",
    ] + [c for c in num_cols if c != col_puntaje]

    candidatos_x = []
    for col in dict.fromkeys([c for c in candidatos_base_x if c]):
        if col in filtrado.columns:
            s_x = pd.to_numeric(filtrado[col], errors="coerce").dropna()
            if not s_x.empty:
                candidatos_x.append(col)

    if candidatos_x and col_puntaje and col_puntaje in filtrado.columns and not filtrado.empty:
        variable_x = st.selectbox("Variable en eje X", candidatos_x, key="eje_x_bi")

        df_scatter = filtrado.copy()
        df_scatter[variable_x] = pd.to_numeric(df_scatter[variable_x], errors="coerce")
        df_scatter[col_puntaje] = pd.to_numeric(df_scatter[col_puntaje], errors="coerce")
        df_scatter = df_scatter.dropna(subset=[variable_x, col_puntaje])

        color_col = (
            col_seg3
            if (
                col_seg3
                and col_seg3 in df_scatter.columns
                and (
                    str(col_seg3).startswith("_q_")
                    or not pd.api.types.is_numeric_dtype(df_scatter[col_seg3])
                )
            )
            else None
        )

        if not df_scatter.empty:
            st.scatter_chart(
                df_scatter,
                x=variable_x,
                y=col_puntaje,
                color=color_col,
                height=300,
            )
        else:
            st.info("Sin datos válidos para graficar dispersión.")
    else:
        st.info("Sin variables numéricas suficientes para dispersión.")

# --- Gráfico secundario: Ranking territorial o evolución ---
st.subheader("Comparativa territorial (Top 15)")
if (
    col_depto
    and col_depto in filtrado.columns
    and col_puntaje
    and col_puntaje in filtrado.columns
    and not filtrado.empty
):
    df_h = filtrado.copy()
    df_h[col_puntaje] = pd.to_numeric(df_h[col_puntaje], errors="coerce")

    ranking_depto = (
        df_h.dropna(subset=[col_depto, col_puntaje])
        .groupby(col_depto, dropna=True)[col_puntaje]
        .mean()
        .sort_values(ascending=False)
        .head(15)
    )
    # Invertimos para que el #1 quede arriba en barras horizontales
    df_barras_h = preparar_barras_destacadas(ranking_depto.iloc[::-1])
    if not df_barras_h.empty:
        st.bar_chart(
            df_barras_h,
            color=["#1E3A8A", "#93C5FD"],
            horizontal=True,
            height=360,
        )