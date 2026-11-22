"""
Análisis exploratorio (Etapa 1, Persona 3).

Saca tablas, gráficos y resúmenes para 2022 (principal), 2019 y 2014-2017.
También deja el registro de decisiones y un resumen base para los hallazgos.

Salidas principales en outputs/persona3/ (tablas, figuras, CSV de apoyo) y
docs/persona3/registro_decisiones.md.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent
DATA_PROCESADOS = RAIZ / "data" / "procesados"
RUTA_DATASET = DATA_PROCESADOS / "dataset_integrado.csv"

OUT_ROOT = RAIZ / "outputs" / "persona3"
TABLAS_ROOT = OUT_ROOT / "tablas"
FIGURAS_ROOT = OUT_ROOT / "figuras"
DOCS_ROOT = RAIZ / "docs" / "persona3"

# Reglas del análisis (quedan registradas cuando corre el script)
UMBRAL_MUNICIPIOS_PEQUENOS = 30  # menos de 30 evaluados = muy poco tamaño, se saca del análisis principal
EXCLUIR_CEROS_SOSPECHOSOS = {
    "DESERCION_MEDIA": True,   # hay ceros; en 2022 los trato como sospechosos para el corte principal
    "COBERTURA_NETA_MEDIA": False,  # se ven ceros, pero los dejo
    "pct_internet_hogar": False,     # puede haber ceros; los dejo y se reportan
    "pct_evaluados_rural": False,    # 0 es normal si es urbano
}
EXCLUIR_MAYORES_100 = {
    "COBERTURA_NETA_MEDIA": True,  # >100 no cuadra bien para comparar
    "pct_internet_hogar": True,
    "pct_evaluados_rural": True,
    "DESERCION_MEDIA": True,
}


def asegurar_directorios() -> None:
    for sub in ["2022", "2019", "2014_2017"]:
        (TABLAS_ROOT / sub).mkdir(parents=True, exist_ok=True)
        (FIGURAS_ROOT / sub).mkdir(parents=True, exist_ok=True)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)


def strip_accents(text: str) -> str:
    text = str(text)
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def norm_col(text: str) -> str:
    t = strip_accents(str(text)).upper()
    for ch in [" ", "-", "/", ".", "%", ",", ":", "\ufffd", "�", "\x93", "\x94"]:
        t = t.replace(ch, "_")
    while "__" in t:
        t = t.replace("__", "_")
    return t.strip("_")


def resolver_columna(df: pd.DataFrame, candidatos: Iterable[str]) -> Optional[str]:
    cols = list(df.columns)
    norm_map = {norm_col(c): c for c in cols}
    for cand in candidatos:
        nc = norm_col(cand)
        if nc in norm_map:
            return norm_map[nc]
    # si no matchea exacto, pruebo por coincidencia parcial
    for cand in candidatos:
        nc = norm_col(cand)
        for n, orig in norm_map.items():
            if nc and nc in n:
                return orig
    return None


def leer_dataset() -> Tuple[pd.DataFrame, Dict[str, Optional[str]]]:
    if not RUTA_DATASET.exists():
        raise FileNotFoundError(f"No se encontró {RUTA_DATASET}")
    # el CSV a veces viene con acentos raros; pruebo varios encodings
    last_err = None
    df = None
    for enc in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        try:
            df = pd.read_csv(RUTA_DATASET, dtype={"codigo_municipio": str}, encoding=enc)
            break
        except Exception as e:
            last_err = e
    if df is None:
        raise last_err
    colmap = {
        "codigo_municipio": resolver_columna(df, ["codigo_municipio"]),
        "anio": resolver_columna(df, ["anio", "AÑO", "ANO"]),
        "municipio": resolver_columna(df, ["MUNICIPIO"]),
        "departamento": resolver_columna(df, ["DEPARTAMENTO"]),
        "punt_global_prom": resolver_columna(df, ["punt_global_prom"]),
        "total_evaluados": resolver_columna(df, ["total_evaluados"]),
        "desercion_media": resolver_columna(df, ["DESERCIÓN_MEDIA", "DESERCION_MEDIA", "DESERCI_N_MEDIA"]),
        "cobertura_neta_media": resolver_columna(df, ["COBERTURA_NETA_MEDIA"]),
        "pct_internet_hogar": resolver_columna(df, ["pct_internet_hogar"]),
        "pct_evaluados_rural": resolver_columna(df, ["pct_evaluados_rural"]),
        "ipm_municipal": resolver_columna(df, ["ipm_municipal"]),
        "penetracion_internet_hogares": resolver_columna(df, ["penetracion_internet_hogares"]),
        "penetracion_internet_fijo": resolver_columna(df, ["penetracion_internet_fijo"]),
        "brecha_vs_nacional": resolver_columna(df, ["brecha_punt_global_vs_nacional"]),
    }
    for k in ["anio", "punt_global_prom", "total_evaluados", "desercion_media", "cobertura_neta_media",
              "pct_internet_hogar", "pct_evaluados_rural", "ipm_municipal",
              "penetracion_internet_hogares", "penetracion_internet_fijo", "brecha_vs_nacional"]:
        c = colmap.get(k)
        if c and c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if colmap.get("anio") and colmap["anio"] in df.columns:
        df[colmap["anio"]] = df[colmap["anio"]].astype("Int64")
    return df, colmap


def unificar_departamento(nombre: object) -> object:
    if pd.isna(nombre):
        return nombre
    t = strip_accents(str(nombre)).upper().strip()
    reemplazos = {
        "BOGOTA, D.C.": "BOGOTÁ, D.C.",
        "BOGOTA D.C.": "BOGOTÁ, D.C.",
        "BOGOTA": "BOGOTÁ, D.C.",
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA": "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
        "SAN ANDRES": "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
        "SAN ANDRES Y PROVIDENCIA": "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    }
    if t in reemplazos:
        return reemplazos[t]
    return " ".join(str(nombre).strip().split())


def aplicar_unificacion_departamentos(df: pd.DataFrame, col_dep: Optional[str]) -> pd.DataFrame:
    if not col_dep or col_dep not in df.columns:
        return df
    df = df.copy()
    df[col_dep + "_original"] = df[col_dep]
    df[col_dep] = df[col_dep].apply(unificar_departamento)
    return df


def registrar_decision(decisiones: List[dict], corte: str, tema: str, decision: str, detalle: str, n_antes: int = None, n_despues: int = None) -> None:
    decisiones.append({
        "corte": corte,
        "tema": tema,
        "decision": decision,
        "detalle": detalle,
        "n_antes": n_antes,
        "n_despues": n_despues,
    })


def preparar_corte_2022(df: pd.DataFrame, colmap: Dict[str, Optional[str]], decisiones: List[dict]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Arma el corte de 2022: base principal, excluidos y base con flags."""
    c_anio = colmap["anio"]
    c_punt = colmap["punt_global_prom"]
    c_eval = colmap["total_evaluados"]
    base = df[df[c_anio] == 2022].copy()
    n0 = len(base)
    registrar_decision(decisiones, "2022", "corte_año", "Filtrar año 2022", "Me quedo solo con filas de 2022.", len(df), n0)

    sin_puntaje = base[c_punt].isna() if c_punt in base.columns else pd.Series(False, index=base.index)
    excl_sin_puntaje = base[sin_puntaje].copy()
    excl_sin_puntaje["motivo_exclusion"] = "sin_puntaje_global"
    base = base[~sin_puntaje].copy()
    registrar_decision(decisiones, "2022", "sin_puntaje", "Sacar municipios sin puntaje global", f"Se sacan {int(sin_puntaje.sum())} filas sin punt_global_prom.", n0, len(base))

    antes_deps = base[colmap["departamento"]].nunique() if colmap.get("departamento") in base.columns else None
    base = aplicar_unificacion_departamentos(base, colmap.get("departamento"))
    despues_deps = base[colmap["departamento"]].nunique() if colmap.get("departamento") in base.columns else None
    registrar_decision(decisiones, "2022", "departamentos", "Unificar nombres de departamento", f"Ajuste de nombres/variantes para que no queden duplicados raros. Únicos antes/después: {antes_deps}/{despues_deps}.", n0, len(base))

    flags = pd.DataFrame(index=base.index)
    if c_eval in base.columns:
        flags["flag_municipio_pequeno"] = pd.to_numeric(base[c_eval], errors="coerce") < UMBRAL_MUNICIPIOS_PEQUENOS
    for key, col in [("desercion_media", colmap.get("desercion_media")),
                     ("cobertura_neta_media", colmap.get("cobertura_neta_media")),
                     ("pct_internet_hogar", colmap.get("pct_internet_hogar")),
                     ("pct_evaluados_rural", colmap.get("pct_evaluados_rural"))]:
        if not col or col not in base.columns:
            continue
        s = pd.to_numeric(base[col], errors="coerce")
        flags[f"flag_cero_{key}"] = s == 0
        flags[f"flag_gt100_{key}"] = s > 100
        flags[f"flag_neg_{key}"] = s < 0

    base_flags = pd.concat([base, flags], axis=1)

    n_antes_calidad = len(base)
    mask_excluir = pd.Series(False, index=base.index)
    motivos = pd.Series("", index=base.index, dtype=object)
    if c_eval in base.columns:
        m_peq = pd.to_numeric(base[c_eval], errors="coerce") < UMBRAL_MUNICIPIOS_PEQUENOS
        mask_excluir |= m_peq.fillna(False)
        motivos = np.where(m_peq.fillna(False), np.where(motivos == "", "municipio_pequeno", motivos + ";municipio_pequeno"), motivos)

    for key_const, col_key in [("DESERCION_MEDIA", "desercion_media"), ("COBERTURA_NETA_MEDIA", "cobertura_neta_media"),
                               ("pct_internet_hogar", "pct_internet_hogar"), ("pct_evaluados_rural", "pct_evaluados_rural")]:
        col = colmap.get(col_key)
        if not col or col not in base.columns:
            continue
        s = pd.to_numeric(base[col], errors="coerce")
        if EXCLUIR_MAYORES_100.get(key_const, False):
            m = s > 100
            mask_excluir |= m.fillna(False)
            motivos = np.where(m.fillna(False), np.where(motivos == "", f"gt100_{col_key}", motivos + f";gt100_{col_key}"), motivos)
        if EXCLUIR_CEROS_SOSPECHOSOS.get(key_const, False):
            m = s == 0
            mask_excluir |= m.fillna(False)
            motivos = np.where(m.fillna(False), np.where(motivos == "", f"cero_{col_key}", motivos + f";cero_{col_key}"), motivos)

    excl_calidad = base[mask_excluir].copy()
    excl_calidad["motivo_exclusion"] = pd.Series(motivos, index=base.index)[mask_excluir].values
    base_principal = base[~mask_excluir].copy()

    registrar_decision(decisiones, "2022", "municipios_pequenos", f"Sacar del análisis principal municipios con menos de {UMBRAL_MUNICIPIOS_PEQUENOS} evaluados", "Con pocos evaluados el dato baila mucho; los dejo guardados aparte por si toca revisar sensibilidad.", n_antes_calidad, len(base_principal))
    registrar_decision(decisiones, "2022", "valores_sospechosos", "Sacar valores >100 en cobertura, internet ICFES, ruralidad y deserción", "Porcentajes por encima de 100 no tienen mucho sentido aquí; los ceros de deserción los traté como sospechosos según la regla definida arriba.", n_antes_calidad, len(base_principal))

    excluidos = pd.concat([excl_sin_puntaje, excl_calidad], ignore_index=True, sort=False)
    return base_principal, excluidos, base_flags


def resumen_descriptivo(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    rows = []
    for c in cols:
        if c not in df.columns:
            continue
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() == 0:
            rows.append({"variable": c, "n": 0, "n_missing": int(s.isna().sum())})
            continue
        rows.append({
            "variable": c,
            "n": int(s.notna().sum()),
            "n_missing": int(s.isna().sum()),
            "media": s.mean(),
            "mediana": s.median(),
            "desv_std": s.std(ddof=1),
            "min": s.min(),
            "p25": s.quantile(0.25),
            "p75": s.quantile(0.75),
            "max": s.max(),
        })
    return pd.DataFrame(rows)


def corr_segura(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    # Spearman en pandas puede pedir scipy; si no está, uso ranks + Pearson
    data = df.apply(pd.to_numeric, errors="coerce")
    if method == "spearman":
        try:
            return data.corr(method="spearman")
        except Exception:
            ranked = data.rank(method="average")
            return ranked.corr(method="pearson")
    return data.corr(method=method)


def corr_series_segura(a: pd.Series, b: pd.Series, method: str = "pearson"):
    sa = pd.to_numeric(a, errors="coerce")
    sb = pd.to_numeric(b, errors="coerce")
    tmp = pd.concat([sa, sb], axis=1).dropna()
    if len(tmp) < 2:
        return np.nan
    if method == "spearman":
        try:
            return tmp.iloc[:, 0].corr(tmp.iloc[:, 1], method="spearman")
        except Exception:
            return tmp.iloc[:, 0].rank().corr(tmp.iloc[:, 1].rank(), method="pearson")
    return tmp.iloc[:, 0].corr(tmp.iloc[:, 1], method=method)


def guardar_tabla(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def grupo_ruralidad(serie: pd.Series) -> pd.Series:
    bins = [-0.01, 20, 50, 80, 100.01]
    labels = ["Urbano (<=20% rural)", "Mixto-bajo (20-50%)", "Mixto-alto (50-80%)", "Rural (>80%)"]
    return pd.cut(pd.to_numeric(serie, errors="coerce"), bins=bins, labels=labels)


def get_expl_vars(colmap: Dict[str, Optional[str]], df: pd.DataFrame) -> Dict[str, str]:
    expl = {
        "desercion_media": colmap.get("desercion_media"),
        "cobertura_neta_media": colmap.get("cobertura_neta_media"),
        "pct_internet_hogar": colmap.get("pct_internet_hogar"),
        "pct_evaluados_rural": colmap.get("pct_evaluados_rural"),
    }
    return {k: v for k, v in expl.items() if v and v in df.columns}


def comparaciones_2022(df: pd.DataFrame, colmap: Dict[str, Optional[str]], out_tablas: Path, out_figs: Path) -> None:
    dep = colmap.get("departamento")
    mun = colmap.get("municipio")
    punt = colmap.get("punt_global_prom")
    rural = colmap.get("pct_evaluados_rural")
    eval_col = colmap.get("total_evaluados")
    if not punt or punt not in df.columns:
        return
    expl = get_expl_vars(colmap, df)

    # comparación por departamento
    if dep and dep in df.columns:
        agg = {punt: ["mean", "median", "count"]}
        if eval_col and eval_col in df.columns:
            agg[eval_col] = ["sum"]
        if rural and rural in df.columns:
            agg[rural] = ["mean"]
        dep_tab = df.groupby(dep, dropna=False).agg(agg)
        dep_tab.columns = ["_".join([str(a) for a in c if a]) for c in dep_tab.columns.to_flat_index()]
        dep_tab = dep_tab.reset_index().rename(columns={
            f"{punt}_mean": "punt_global_promedio",
            f"{punt}_median": "punt_global_mediana",
            f"{punt}_count": "municipios",
            f"{eval_col}_sum": "evaluados_total" if eval_col else "evaluados_total",
            f"{rural}_mean": "ruralidad_media" if rural else "ruralidad_media",
        })
        for k, c in expl.items():
            dep_tab[f"{k}_media"] = df.groupby(dep, dropna=False)[c].mean().values
        dep_tab = dep_tab.sort_values("punt_global_promedio", ascending=False)
        guardar_tabla(dep_tab, out_tablas / "comparacion_por_departamento.csv")

        top = dep_tab.dropna(subset=["punt_global_promedio"]).head(15)
        if not top.empty:
            plt.figure(figsize=(10, 6))
            plt.barh(top[dep].astype(str)[::-1], top["punt_global_promedio"][::-1], color="#4C72B0")
            plt.xlabel("Puntaje global promedio (Saber 11)")
            plt.title("Top 15 departamentos por puntaje global promedio")
            plt.tight_layout()
            plt.savefig(out_figs / "top15_departamentos_puntaje.png", dpi=150)
            plt.close()

    # por grupos de ruralidad
    if rural and rural in df.columns:
        tmp = df.copy()
        tmp["grupo_ruralidad"] = grupo_ruralidad(tmp[rural])
        agg = {punt: ["mean", "median", "count"]}
        if eval_col and eval_col in df.columns:
            agg[eval_col] = ["sum"]
        rur_tab = tmp.groupby("grupo_ruralidad", dropna=False, observed=False).agg(agg)
        rur_tab.columns = ["_".join([str(a) for a in c if a]) for c in rur_tab.columns.to_flat_index()]
        rur_tab = rur_tab.reset_index().rename(columns={
            f"{punt}_mean": "punt_global_promedio",
            f"{punt}_median": "punt_global_mediana",
            f"{punt}_count": "municipios",
            f"{eval_col}_sum": "evaluados_total" if eval_col else "evaluados_total",
        })
        for k, c in expl.items():
            rur_tab[f"{k}_media"] = tmp.groupby("grupo_ruralidad", observed=False)[c].mean().values
        guardar_tabla(rur_tab, out_tablas / "comparacion_por_ruralidad.csv")

        plot_df = rur_tab.dropna(subset=["grupo_ruralidad"])
        if not plot_df.empty:
            plt.figure(figsize=(8, 4.5))
            plt.bar(plot_df["grupo_ruralidad"].astype(str), plot_df["punt_global_promedio"], color="#55A868")
            plt.ylabel("Puntaje global promedio")
            plt.title("Puntaje global promedio por grupo de ruralidad")
            plt.xticks(rotation=20, ha="right")
            plt.tight_layout()
            plt.savefig(out_figs / "puntaje_por_ruralidad.png", dpi=150)
            plt.close()

    # cuartiles de cada variable explicativa
    for k, c in expl.items():
        cols_need = [punt, c] + ([eval_col] if eval_col and eval_col in df.columns else [])
        tmp = df[cols_need].copy()
        tmp = tmp.dropna(subset=[c, punt])
        if len(tmp) < 8:
            continue
        try:
            tmp[f"cuartil_{k}"] = pd.qcut(tmp[c], 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
        except Exception:
            tmp[f"cuartil_{k}"] = pd.cut(tmp[c], 4, duplicates="drop")
        qtab = tmp.groupby(f"cuartil_{k}", observed=False).agg(
            municipios=(punt, "count"),
            variable_min=(c, "min"),
            variable_max=(c, "max"),
            punt_global_promedio=(punt, "mean"),
            punt_global_mediana=(punt, "median"),
        ).reset_index()
        guardar_tabla(qtab, out_tablas / f"comparacion_cuartiles_{k}.csv")
        if not qtab.empty:
            plt.figure(figsize=(6.5, 4))
            plt.bar(qtab[f"cuartil_{k}"].astype(str), qtab["punt_global_promedio"], color="#C44E52")
            plt.xlabel(f"Cuartil de {k}")
            plt.ylabel("Puntaje global promedio")
            plt.title(f"Puntaje promedio por cuartiles de {k}")
            plt.tight_layout()
            plt.savefig(out_figs / f"puntaje_por_cuartiles_{k}.png", dpi=150)
            plt.close()

    # cruce ruralidad x internet (ICFES)
    if rural and rural in df.columns and expl.get("pct_internet_hogar"):
        c_int = expl["pct_internet_hogar"]
        tmp = df[[punt, rural, c_int]].dropna().copy()
        if len(tmp) >= 20:
            tmp["grupo_ruralidad"] = grupo_ruralidad(tmp[rural])
            try:
                tmp["cuartil_internet"] = pd.qcut(tmp[c_int], 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
            except Exception:
                tmp["cuartil_internet"] = pd.cut(tmp[c_int], 4, duplicates="drop")
            cruzada = tmp.pivot_table(index="grupo_ruralidad", columns="cuartil_internet", values=punt, aggfunc="mean", observed=False)
            cruzada_count = tmp.pivot_table(index="grupo_ruralidad", columns="cuartil_internet", values=punt, aggfunc="count", observed=False)
            cruzada.reset_index().to_csv(out_tablas / "comparacion_cruzada_ruralidad_x_internet_media.csv", index=False, encoding="utf-8-sig")
            cruzada_count.reset_index().to_csv(out_tablas / "comparacion_cruzada_ruralidad_x_internet_n.csv", index=False, encoding="utf-8-sig")

    # correlaciones
    corr_cols = [punt] + [c for c in expl.values() if c in df.columns]
    corr_df = df[corr_cols].apply(pd.to_numeric, errors="coerce")
    corr_segura(corr_df, method="pearson").to_csv(out_tablas / "correlaciones_pearson.csv", encoding="utf-8-sig")
    corr_segura(corr_df, method="spearman").to_csv(out_tablas / "correlaciones_spearman.csv", encoding="utf-8-sig")

    s_punt = pd.to_numeric(df[punt], errors="coerce").dropna()
    if not s_punt.empty:
        plt.figure(figsize=(7, 4))
        plt.hist(s_punt, bins=30, color="#8172B2", edgecolor="white")
        plt.xlabel("Puntaje global promedio municipal")
        plt.ylabel("Número de municipios")
        plt.title("Distribución del puntaje global promedio")
        plt.tight_layout()
        plt.savefig(out_figs / "distribucion_puntaje_global.png", dpi=150)
        plt.close()

    scatter_specs = [
        ("desercion_media", "Deserción media", "dispersion_desercion_vs_puntaje.png"),
        ("cobertura_neta_media", "Cobertura neta media", "dispersion_cobertura_vs_puntaje.png"),
        ("pct_internet_hogar", "% hogares con internet (ICFES)", "dispersion_internet_icfes_vs_puntaje.png"),
        ("pct_evaluados_rural", "% evaluados en zona rural", "dispersion_ruralidad_vs_puntaje.png"),
    ]
    for k, label, fname in scatter_specs:
        c = expl.get(k)
        if not c:
            continue
        tmp = df[[c, punt]].apply(pd.to_numeric, errors="coerce").dropna()
        if tmp.empty:
            continue
        plt.figure(figsize=(6.5, 4.5))
        plt.scatter(tmp[c], tmp[punt], alpha=0.35, s=18, color="#4C72B0")
        if len(tmp) >= 2 and tmp[c].nunique() > 1:
            z = np.polyfit(tmp[c], tmp[punt], 1)
            xs = np.linspace(tmp[c].min(), tmp[c].max(), 100)
            plt.plot(xs, np.polyval(z, xs), color="#C44E52", linewidth=1.5)
        plt.xlabel(label)
        plt.ylabel("Puntaje global promedio")
        plt.title(f"{label} vs puntaje global")
        plt.tight_layout()
        plt.savefig(out_figs / fname, dpi=150)
        plt.close()


def analisis_corte(df: pd.DataFrame, colmap: Dict[str, Optional[str]], nombre_corte: str, mask: pd.Series, decisiones: List[dict]) -> pd.DataFrame:
    out_tablas = TABLAS_ROOT / nombre_corte
    out_figs = FIGURAS_ROOT / nombre_corte
    base = df.loc[mask].copy()
    punt = colmap.get("punt_global_prom")
    n0 = len(base)
    if punt and punt in base.columns:
        sin_punt = base[punt].isna()
        base = base[~sin_punt].copy()
        registrar_decision(decisiones, nombre_corte, "sin_puntaje", "Quitar filas sin puntaje global", f"Quité {int(sin_punt.sum())} de {n0}.", n0, len(base))
    eval_col = colmap.get("total_evaluados")
    if eval_col and eval_col in base.columns:
        n1 = len(base)
        peq = pd.to_numeric(base[eval_col], errors="coerce") < UMBRAL_MUNICIPIOS_PEQUENOS
        base = base[~peq.fillna(False)].copy()
        registrar_decision(decisiones, nombre_corte, "municipios_pequenos", f"Quitar municipios con menos de {UMBRAL_MUNICIPIOS_PEQUENOS} evaluados", f"Quité {int(peq.fillna(False).sum())} de {n1}.", n1, len(base))
    for key in ["cobertura_neta_media", "pct_internet_hogar", "pct_evaluados_rural", "desercion_media"]:
        c = colmap.get(key)
        if c and c in base.columns:
            n1 = len(base)
            m = pd.to_numeric(base[c], errors="coerce") > 100
            base = base[~m.fillna(False)].copy()
            if int(m.fillna(False).sum()) > 0:
                registrar_decision(decisiones, nombre_corte, f"gt100_{key}", f"Quitar {key} > 100", f"Quité {int(m.fillna(False).sum())} filas.", n1, len(base))
    base = aplicar_unificacion_departamentos(base, colmap.get("departamento"))

    cols_desc = [c for c in [punt, colmap.get("desercion_media"), colmap.get("cobertura_neta_media"),
                             colmap.get("pct_internet_hogar"), colmap.get("pct_evaluados_rural"), colmap.get("total_evaluados")] if c and c in base.columns]
    guardar_tabla(resumen_descriptivo(base, cols_desc), out_tablas / "descriptiva_variables_clave.csv")
    comparaciones_2022(base, colmap, out_tablas, out_figs)
    guardar_tabla(base, out_tablas / "base_analisis.csv")
    return base


def construir_resumen_hallazgos(bases: Dict[str, pd.DataFrame], colmap: Dict[str, Optional[str]]) -> pd.DataFrame:
    rows = []
    punt = colmap.get("punt_global_prom")
    if not punt:
        return pd.DataFrame(rows)
    for nombre, df in bases.items():
        if df is None or df.empty or punt not in df.columns:
            continue
        for var_key, label in [
            ("desercion_media", "deserción media"),
            ("cobertura_neta_media", "cobertura neta media"),
            ("pct_internet_hogar", "internet ICFES"),
            ("pct_evaluados_rural", "ruralidad"),
        ]:
            c = colmap.get(var_key)
            if not c or c not in df.columns:
                continue
            tmp = df[[punt, c]].apply(pd.to_numeric, errors="coerce").dropna()
            if len(tmp) < 10:
                continue
            rows.append({
                "corte": nombre,
                "variable": label,
                "n": len(tmp),
                "pearson_con_puntaje": corr_series_segura(tmp[punt], tmp[c], method="pearson"),
                "spearman_con_puntaje": corr_series_segura(tmp[punt], tmp[c], method="spearman"),
                "puntaje_promedio": tmp[punt].mean(),
                "puntaje_mediana": tmp[punt].median(),
            })
    return pd.DataFrame(rows)


def guardar_registro_decisiones_md(decisiones: List[dict], path: Path) -> None:
    lines = [
        "# Registro de decisiones",
        "",
        "Acá dejo los filtros y criterios que usé en la Etapa 1, con el porqué y cómo cambió el número de filas.",
        "",
        "| Corte | Tema | Decisión | Razón/Detalle | N antes | N después |",
        "|---|---|---|---|---:|---:|",
    ]
    for d in decisiones:
        detalle = str(d.get("detalle", "")).replace("|", "/").replace("\n", " ")
        lines.append(
            f"| {d.get('corte','')} | {d.get('tema','')} | {d.get('decision','')} | {detalle} | "
            f"{'' if d.get('n_antes') is None else d.get('n_antes')} | {'' if d.get('n_despues') is None else d.get('n_despues')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    asegurar_directorios()
    df, colmap = leer_dataset()
    decisiones: List[dict] = []

    registrar_decision(decisiones, "global", "columnas", "Ajuste de nombres de columnas (encoding raro)", json.dumps({k: v for k, v in colmap.items()}, ensure_ascii=False), None, None)
    registrar_decision(decisiones, "global", "pendientes_persona2", "Pendiente: IPM/internet TerriData si Persona 2 actualiza la fuente", "Si cambian esos datos, toca volver a correr el script para que entren en las tablas/gráficos.", None, None)

    bases: Dict[str, pd.DataFrame] = {}

    # 2022 (corte principal)
    base_2022, excluidos_2022, base_2022_flags = preparar_corte_2022(df, colmap, decisiones)
    out_2022_t = TABLAS_ROOT / "2022"
    out_2022_f = FIGURAS_ROOT / "2022"
    guardar_tabla(excluidos_2022, out_2022_t / "excluidos_y_motivos.csv")
    guardar_tabla(base_2022_flags, out_2022_t / "base_2022_con_flags_calidad.csv")
    cols_desc_2022 = [c for c in [colmap.get("punt_global_prom"), colmap.get("desercion_media"), colmap.get("cobertura_neta_media"),
                                  colmap.get("pct_internet_hogar"), colmap.get("pct_evaluados_rural"), colmap.get("total_evaluados")]
                      if c and c in base_2022.columns]
    guardar_tabla(resumen_descriptivo(base_2022, cols_desc_2022), out_2022_t / "descriptiva_variables_clave.csv")
    guardar_tabla(base_2022, out_2022_t / "base_analisis.csv")
    comparaciones_2022(base_2022, colmap, out_2022_t, out_2022_f)
    bases["2022"] = base_2022

    # 2019 (lo esencial)
    mask_2019 = df[colmap["anio"]] == 2019 if colmap.get("anio") in df.columns else pd.Series(False, index=df.index)
    bases["2019"] = analisis_corte(df, colmap, "2019", mask_2019, decisiones)

    # 2014-2017: cada año por separado y también consolidado
    bases_1417 = []
    for y in [2014, 2015, 2016, 2017]:
        mask_y = df[colmap["anio"]] == y if colmap.get("anio") in df.columns else pd.Series(False, index=df.index)
        b = analisis_corte(df, colmap, "2014_2017", mask_y, decisiones)
        b = b.copy()
        b["_anio_corte"] = y
        guardar_tabla(b, TABLAS_ROOT / "2014_2017" / f"base_analisis_{y}.csv")
        year_t = TABLAS_ROOT / "2014_2017" / str(y)
        year_f = FIGURAS_ROOT / "2014_2017" / str(y)
        year_t.mkdir(parents=True, exist_ok=True)
        year_f.mkdir(parents=True, exist_ok=True)
        comparaciones_2022(b, colmap, year_t, year_f)
        guardar_tabla(resumen_descriptivo(b, [c for c in cols_desc_2022 if c in b.columns]), year_t / "descriptiva_variables_clave.csv")
        bases_1417.append(b)
    if bases_1417:
        base_1417 = pd.concat(bases_1417, ignore_index=True, sort=False)
        bases["2014_2017"] = base_1417
        guardar_tabla(base_1417, TABLAS_ROOT / "2014_2017" / "base_analisis_consolidada.csv")

    resumen = construir_resumen_hallazgos(bases, colmap)
    guardar_tabla(resumen, OUT_ROOT / "resumen_hallazgos_base.csv")
    guardar_tabla(pd.DataFrame(decisiones), OUT_ROOT / "registro_decisiones.csv")
    guardar_registro_decisiones_md(decisiones, DOCS_ROOT / "registro_decisiones.md")

    print(f"Listo: tablas y figuras en {OUT_ROOT}")
    print(f"Registro de decisiones: {DOCS_ROOT / 'registro_decisiones.md'}")
    print(f"Resumen para hallazgos: {OUT_ROOT / 'resumen_hallazgos_base.csv'}")


if __name__ == "__main__":
    main()
