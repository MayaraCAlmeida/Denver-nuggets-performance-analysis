# Denver Nuggets — Exportar queries PostgreSQL → CSV/Excel

# Precisa que no arquivo .env na raiz do projeto tenha:

#    DATABASE_URL=postgresql://postgres:senhalocalhost:5432/DenverNuggets

# Só consegui rodar assim

import os
import sys
import argparse
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


# QUERIES
queries = {
    "q01_ofensiva_vs_defensiva": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(ortg)::NUMERIC, 1)         AS ortg_medio,
            ROUND(AVG(drtg)::NUMERIC, 1)         AS drtg_medio,
            ROUND(AVG(ortg - drtg)::NUMERIC, 1)  AS net_rating,
            COUNT(*)                             AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q02_media_pontos": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(team_pts)::NUMERIC, 1)   AS denver_pts,
            ROUND(AVG(opp_pts)::NUMERIC, 1)    AS adversario_pts,
            ROUND(AVG(point_diff)::NUMERIC, 1) AS diferenca_media,
            COUNT(*)                           AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q03_efg_eficiencia": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(off_efg_pct)::NUMERIC, 4)  AS efg_ofensivo,
            ROUND(AVG(def_efg_pct)::NUMERIC, 4)  AS efg_defensivo,
            ROUND(AVG(off_tov_pct)::NUMERIC, 2)  AS tov_ofensivo,
            ROUND(AVG(ts_pct)::NUMERIC, 4)       AS ts_pct,
            ROUND(AVG("3par")::NUMERIC, 4)       AS taxa_3pts_tentativas
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q04_turnovers_coletivos": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(off_tov_pct)::NUMERIC, 2)  AS tov_pct_medio,
            ROUND(MIN(off_tov_pct)::NUMERIC, 2)  AS tov_pct_min,
            ROUND(MAX(off_tov_pct)::NUMERIC, 2)  AS tov_pct_max,
            COUNT(*)                             AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q05_casa_vs_fora": """
        SELECT
            home_away,
            COUNT(*)                                      AS jogos,
            SUM(win)                                      AS vitorias,
            COUNT(*) - SUM(win)                           AS derrotas,
            ROUND(AVG(win::NUMERIC) * 100, 1)             AS win_rate_pct,
            ROUND(AVG(team_pts)::NUMERIC, 1)              AS pts_media,
            ROUND(AVG(ortg)::NUMERIC, 1)                  AS ortg_medio,
            ROUND(AVG(drtg)::NUMERIC, 1)                  AS drtg_medio
        FROM denver_nuggets
        GROUP BY home_away
        ORDER BY home_away
    """,
    "q06_jokic_carga": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(jokic_pts)::NUMERIC, 1)          AS pts_medio,
            ROUND(AVG(jokic_ast)::NUMERIC, 1)          AS ast_medio,
            ROUND(AVG(jokic_trb)::NUMERIC, 1)          AS trb_medio,
            ROUND(AVG(jokic_fga)::NUMERIC, 1)          AS fga_medio,
            ROUND(AVG(jokic_plus_minus)::NUMERIC, 1)   AS plus_minus_medio,
            ROUND(AVG(jokic_gmsc)::NUMERIC, 1)         AS game_score_medio,
            COUNT(*)                                   AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q07_jokic_eficiencia": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(jokic_efg_pct)::NUMERIC, 4)  AS efg_pct,
            ROUND(AVG(jokic_fg_pct)::NUMERIC, 4)   AS fg_pct,
            ROUND(AVG(jokic_3p_pct)::NUMERIC, 4)   AS tres_p_pct,
            ROUND(AVG(jokic_ft_pct)::NUMERIC, 4)   AS ft_pct
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q08_ast_faixas": """
        SELECT
            CASE
                WHEN jokic_ast BETWEEN 0  AND 6  THEN '1. Baixa (1-6)'
                WHEN jokic_ast BETWEEN 7  AND 10 THEN '2. Média (7-10)'
                WHEN jokic_ast BETWEEN 11 AND 15 THEN '3. Alta (11-15)'
                ELSE '4. Elite (15+)'
            END AS faixa_ast,
            COUNT(*)                              AS jogos,
            SUM(win)                              AS vitorias,
            ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct
        FROM denver_nuggets
        GROUP BY faixa_ast
        ORDER BY faixa_ast
    """,
    "q09_jokic_tov": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(jokic_tov)::NUMERIC, 2)   AS tov_medio,
            ROUND(MIN(jokic_tov)::NUMERIC, 0)   AS tov_min,
            ROUND(MAX(jokic_tov)::NUMERIC, 0)   AS tov_max,
            COUNT(*)                            AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q10_triplo_duplo": """
        SELECT
            CASE WHEN triple_double = 1 THEN 'Com Triplo-Duplo' ELSE 'Sem Triplo-Duplo' END AS td,
            COUNT(*)                              AS jogos,
            SUM(win)                              AS vitorias,
            ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct,
            ROUND(AVG(jokic_pts)::NUMERIC, 1)     AS pts_medio,
            ROUND(AVG(jokic_ast)::NUMERIC, 1)     AS ast_medio,
            ROUND(AVG(jokic_trb)::NUMERIC, 1)     AS trb_medio
        FROM denver_nuggets
        GROUP BY triple_double
        ORDER BY triple_double DESC
    """,
    "q11_playoffs_vs_regular": """
        SELECT
            season_type,
            COUNT(*)                                      AS jogos,
            SUM(win)                                      AS vitorias,
            ROUND(AVG(win::NUMERIC) * 100, 1)             AS win_rate_pct,
            ROUND(AVG(jokic_pts)::NUMERIC, 1)             AS jokic_pts,
            ROUND(AVG(jokic_ast)::NUMERIC, 1)             AS jokic_ast,
            ROUND(AVG(jokic_trb)::NUMERIC, 1)             AS jokic_trb,
            ROUND(AVG(jokic_plus_minus)::NUMERIC, 1)      AS plus_minus,
            ROUND(AVG(ortg)::NUMERIC, 1)                  AS ortg,
            ROUND(AVG(drtg)::NUMERIC, 1)                  AS drtg,
            ROUND(AVG(off_efg_pct)::NUMERIC, 4)           AS off_efg_pct
        FROM denver_nuggets
        GROUP BY season_type
        ORDER BY season_type
    """,
    "q12_top_metricas": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(ortg)::NUMERIC, 1)                              AS ortg,
            ROUND(AVG(drtg)::NUMERIC, 1)                              AS drtg,
            ROUND(AVG(off_efg_pct)::NUMERIC, 4)                       AS off_efg_pct,
            ROUND(AVG(def_efg_pct)::NUMERIC, 4)                       AS def_efg_pct,
            ROUND(AVG("3par")::NUMERIC, 4)                            AS taxa_3pts,
            ROUND(AVG(jokic_pts)::NUMERIC, 1)                         AS jokic_pts,
            ROUND(AVG(jokic_plus_minus)::NUMERIC, 1)                  AS jokic_pm,
            ROUND(AVG(triple_double::NUMERIC) * 100, 1)               AS pct_triplo_duplo
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
    "q13_usg_calculado": """
        SELECT
            CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
            ROUND(AVG(jokic_fga)::NUMERIC, 1)                                          AS fga_medio,
            ROUND(AVG(jokic_3pa)::NUMERIC, 1)                                          AS fta_estimado,
            ROUND(AVG(jokic_fga + 0.44 * jokic_3pa + jokic_tov)::NUMERIC, 1)          AS usg_numerador,
            ROUND(AVG((jokic_fga + 0.44 * jokic_3pa + jokic_tov)
                / NULLIF(jokic_mp, 0) * 36)::NUMERIC, 2)                               AS usg_proxy,
            COUNT(*)                                                                    AS jogos
        FROM denver_nuggets
        GROUP BY win
        ORDER BY win DESC
    """,
}


# MAIN
def main():
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("❌  DATABASE_URL não encontrada.")
        print("    Crie um arquivo .env com:")
        print(
            "    DATABASE_URL=postgresql://postgres:SUASENHA@localhost:5432/DenverNuggets"
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Denver Nuggets — exportar queries")
    parser.add_argument(
        "--output", "-o", default=".", help="Diretório de saída (padrão: pasta atual)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    engine = create_engine(db_url)

    print("=" * 55)
    print("  DENVER NUGGETS — Exportando queries")
    print("=" * 55)

    results = {}
    with engine.connect() as conn:
        for name, sql in queries.items():
            try:
                df = pd.read_sql(text(sql), conn)
                results[name] = df
                csv_path = output_dir / f"{name}.csv"
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                print(f"✅  {name}.csv  ({len(df)} linhas)")
            except Exception as e:
                print(f"❌  {name} — erro: {e}")

    # Excel com todas as queries em abas separadas
    excel_path = output_dir / "denver_nuggets_analise.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for name, df in results.items():
            sheet = name[4:][:31]  # remove prefixo "q01_" e limita a 31 chars
            df.to_excel(writer, sheet_name=sheet, index=False)

    print(f"\n📊  Excel salvo em: {excel_path}")
    print("\n🏀  Exportação completa!")


if __name__ == "__main__":
    main()
