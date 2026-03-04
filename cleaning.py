import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import unicodedata
import re

# ──────────────────────────────────────────────
# ARGS
# ──────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Denver Nuggets — limpeza e preparação do CSV"
)
parser.add_argument(
    "--input", "-i", required=True, help="Caminho para denver_nuggets_analysis.csv"
)
parser.add_argument(
    "--output",
    "-o",
    required=True,
    help="Caminho de saída para denver_nuggets_clean.csv",
)
args = parser.parse_args()

INPUT_PATH = args.input
OUTPUT_PATH = args.output

# ──────────────────────────────────────────────
# 1. LEITURA
# ──────────────────────────────────────────────
df = pd.read_csv(INPUT_PATH, encoding="utf-8")
print(f"[1] Carregado: {df.shape[0]} linhas x {df.shape[1]} colunas")


# ──────────────────────────────────────────────
# 2. REMOVER DUPLICATAS
# ──────────────────────────────────────────────
before = len(df)
df = df.drop_duplicates()
print(f"[2] Duplicatas removidas: {before - len(df)}")


# ──────────────────────────────────────────────
# 3. LIMPAR NOMES DE COLUNAS
# ──────────────────────────────────────────────
def clean_col_name(col):
    col = str(col)
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("ascii")
    col = col.lower()
    col = col.replace("%", "_pct").replace("/", "_per_")
    col = re.sub(r"[^a-z0-9_]", "_", col)
    col = re.sub(r"_+", "_", col).strip("_")
    return col


df.columns = [clean_col_name(c) for c in df.columns]
print(f"[3] Colunas renomeadas: {list(df.columns)}")


# ──────────────────────────────────────────────
# 4. LIMPAR TEXTO NAS COLUNAS CATEGÓRICAS
# ──────────────────────────────────────────────
def clean_text(val):
    if pd.isna(val):
        return val
    val = str(val).strip()
    val = unicodedata.normalize("NFKD", val).encode("ascii", "ignore").decode("ascii")
    return val


for col in ["opponent", "home_away", "season_type"]:
    df[col] = df[col].apply(clean_text)

print(f"[4] Texto limpo | opponent: {df['opponent'].unique()[:3]}")


# ──────────────────────────────────────────────
# 5. CONVERTER jokic_mp (MM:SS) → minutos decimais
# ──────────────────────────────────────────────
def mp_to_minutes(val):
    try:
        parts = str(val).split(":")
        return round(int(parts[0]) + int(parts[1]) / 60, 2)
    except:
        return np.nan


df["jokic_mp"] = df["jokic_mp"].apply(mp_to_minutes)
print(f"[5] jokic_mp convertido para minutos decimais")


# ──────────────────────────────────────────────
# 6. TRATAR NULOS
#    - colunas numéricas do Jokic: preenche com mediana
#    - triple_double: preenche com 0 (ausência = não ocorreu)
# ──────────────────────────────────────────────
jokic_num_cols = [c for c in df.columns if c.startswith("jokic_") and c != "jokic_mp"]
jokic_num_cols += ["triple_double"]

for col in jokic_num_cols:
    if col in df.columns:
        mediana = df[col].median()
        nulls = df[col].isnull().sum()
        df[col] = df[col].fillna(mediana)
        if nulls > 0:
            print(f"[6] '{col}': {nulls} nulos preenchidos com mediana ({mediana})")

# triple_double garantido como inteiro
df["triple_double"] = df["triple_double"].astype(int)


# ──────────────────────────────────────────────
# 7. GARANTIR TIPOS CORRETOS
# ──────────────────────────────────────────────
int_cols = [
    "game_num",
    "team_pts",
    "opp_pts",
    "wins",
    "losses",
    "win",
    "point_diff",
    "triple_double",
]
float_cols = [c for c in df.columns if df[c].dtype == "float64"]
str_cols = ["opponent", "home_away", "season_type"]

for c in int_cols:
    if c in df.columns:
        df[c] = df[c].astype(int)

for c in float_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce").round(4)

print(f"[7] Tipos ajustados")


# ──────────────────────────────────────────────
# 8. REORDENAR COLUNAS (identificação primeiro)
# ──────────────────────────────────────────────
priority = [
    "game_num",
    "season_type",
    "opponent",
    "home_away",
    "win",
    "team_pts",
    "opp_pts",
    "point_diff",
    "wins",
    "losses",
]
rest = [c for c in df.columns if c not in priority]
df = df[priority + rest]


# ──────────────────────────────────────────────
# 9. SALVAR
# ──────────────────────────────────────────────
df.to_csv(
    OUTPUT_PATH, index=False, encoding="utf-8-sig"
)  # utf-8-sig = compatível com Excel/PowerBI
print(f"\n✅ Arquivo salvo em: {OUTPUT_PATH}")
print(f"   Shape final: {df.shape[0]} linhas x {df.shape[1]} colunas")
print(f"\n📋 Colunas finais:\n{list(df.columns)}")
