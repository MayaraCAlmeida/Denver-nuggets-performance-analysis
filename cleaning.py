# Denver Nuggets — Data Cleaning Pipeline


import argparse
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


# HELPERS
def clean_col_name(col: str) -> str:
    col = (
        unicodedata.normalize("NFKD", str(col))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    col = col.lower().replace("%", "_pct").replace("/", "_per_")
    col = re.sub(r"[^a-z0-9_]", "_", col)
    col = re.sub(r"_+", "_", col).strip("_")
    return col


def clean_text(val) -> str:
    if pd.isna(val):
        return val
    return (
        unicodedata.normalize("NFKD", str(val).strip())
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def mp_to_minutes(val) -> float:
    try:
        parts = str(val).split(":")
        return round(int(parts[0]) + int(parts[1]) / 60, 2)
    except Exception:
        return np.nan


# PIPELINE
def run(input_path: Path, output_path: Path) -> None:

    # 1. Leitura
    df = pd.read_csv(input_path, encoding="utf-8")
    print(f"[1] Carregado: {df.shape[0]} linhas × {df.shape[1]} colunas")

    # 2. Duplicatas
    before = len(df)
    df = df.drop_duplicates()
    print(f"[2] Duplicatas removidas: {before - len(df)}")

    # 3. Nomes de colunas
    df.columns = [clean_col_name(c) for c in df.columns]
    print(f"[3] Colunas renomeadas: {list(df.columns)}")

    # 4. Texto categórico
    for col in ["opponent", "home_away", "season_type"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    print(f"[4] Texto limpo | opponent sample: {df['opponent'].unique()[:3]}")

    # 5. jokic_mp: MM:SS → minutos decimais
    if "jokic_mp" in df.columns:
        df["jokic_mp"] = df["jokic_mp"].apply(mp_to_minutes)
        print("[5] jokic_mp convertido para minutos decimais")

    # 6. Nulos — preenche com mediana
    jokic_num_cols = [
        c for c in df.columns if c.startswith("jokic_") and c != "jokic_mp"
    ]
    jokic_num_cols += ["triple_double"]
    for col in jokic_num_cols:
        if col in df.columns:
            mediana = df[col].median()
            nulls = df[col].isnull().sum()
            df[col] = df[col].fillna(mediana)
            if nulls > 0:
                print(f"[6] '{col}': {nulls} nulos → mediana ({mediana})")

    if "triple_double" in df.columns:
        df["triple_double"] = df["triple_double"].astype(int)

    # 7. Tipos
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
    for c in int_cols:
        if c in df.columns:
            df[c] = df[c].astype(int)

    float_cols = [c for c in df.columns if df[c].dtype == "float64"]
    for c in float_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").round(4)

    print("[7] Tipos ajustados")

    # 8. Reordenar colunas
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
    df = df[[c for c in priority if c in df.columns] + rest]

    # 9. Salvar
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n✅  Arquivo salvo em: {output_path}")
    print(f"   Shape final: {df.shape[0]} linhas × {df.shape[1]} colunas")
    print(f"\n📋  Colunas finais:\n{list(df.columns)}")


# MAIN
def parse_args():
    parser = argparse.ArgumentParser(description="Denver Nuggets — Data Cleaning")
    parser.add_argument(
        "--input",
        "-i",
        default="denver_nuggets_analysis.csv",
        help="CSV bruto de entrada (padrão: denver_nuggets_analysis.csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="denver_nuggets_clean.csv",
        help="CSV limpo de saída (padrão: denver_nuggets_clean.csv)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"❌  Arquivo não encontrado: {input_path}")
        print("   Passe o caminho com --input <arquivo.csv>")
        sys.exit(1)

    run(input_path, output_path)


if __name__ == "__main__":
    main()
