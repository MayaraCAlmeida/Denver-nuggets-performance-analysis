<<<<<<< HEAD
"""
=======================================================
 Strategic Performance Analysis – Denver Nuggets
 Script 1: Análise Exploratória em Python
=======================================================

Usage
-----
    python nuggets_analysis.py --input denver_nuggets_clean.csv
    python nuggets_analysis.py --input denver_nuggets_clean.csv --output ./reports
"""

import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings("ignore")

# ── ARGS ──────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Strategic Performance Analysis – Denver Nuggets"
)
parser.add_argument(
    "--input", "-i", required=True, help="Caminho para denver_nuggets_clean.csv"
)
parser.add_argument(
    "--output",
    "-o",
    default=".",
    help="Diretório de saída para o PNG (padrão: pasta atual)",
)
args = parser.parse_args()

INPUT_PATH = args.input
OUTPUT_DIR = Path(args.output)

# ── ESTILO ────────────────────────────────────────────
DENVER_BLUE = "#0E2240"
DENVER_GOLD = "#FEC524"
WIN_COLOR = "#2ecc71"
LOSS_COLOR = "#e74c3c"
=======
# Strategic Performance Analysis – Denver Nuggets

import argparse
import sys
import warnings
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

# ESTILO
DENVER_BLUE = "#0E2240"
DENVER_GOLD = "#FEC524"
WIN_COLOR = "#27ae60"
LOSS_COLOR = "#e74c3c"
GRAY = "#95a5a6"
>>>>>>> 428fafe (script principal com análise estatística)

plt.rcParams.update(
    {
        "figure.facecolor": "#f8f9fa",
        "axes.facecolor": "#ffffff",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "sans-serif",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
    }
)

<<<<<<< HEAD
# ── LEITURA ───────────────────────────────────────────
df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")
print(f"✅ Dataset carregado: {df.shape[0]} jogos x {df.shape[1]} colunas\n")

# ── USG% CALCULADO ────────────────────────────────────
# Fórmula simplificada: (FGA + 0.44 * FTA + TOV) / (mp/40 * team_possessions)
# Versão relativa sem dados de posse do time: (FGA + 0.44*FTA + TOV) / jokic_mp * 36
df["jokic_fta"] = df["jokic_fga"] * (
    1 / df["jokic_fg_pct"].replace(0, np.nan)
)  # estimativa FTA
df["jokic_usg_proxy"] = (
    (df["jokic_fga"] + 0.44 * df["jokic_fta"].fillna(0) + df["jokic_tov"])
    / df["jokic_mp"].replace(0, np.nan)
    * 36
).round(2)

print("=" * 60)
print("  ANÁLISE DENVER NUGGETS – RELATÓRIO COMPLETO")
print("=" * 60)


# ═══════════════════════════════════════════════════════
# 1. OFENSIVA vs DEFENSIVA — causa das derrotas
# ═══════════════════════════════════════════════════════
print("\n[1] Denver perde mais por falha OFENSIVA ou DEFENSIVA?")
print("-" * 55)

ortg_vitoria = df[df["win"] == 1]["ortg"].mean()
ortg_derrota = df[df["win"] == 0]["ortg"].mean()
drtg_vitoria = df[df["win"] == 1]["drtg"].mean()
drtg_derrota = df[df["win"] == 0]["drtg"].mean()

print(
    f"  ORtg médio — Vitórias: {ortg_vitoria:.1f}  |  Derrotas: {ortg_derrota:.1f}  |  Δ = {ortg_vitoria - ortg_derrota:.1f}"
)
print(
    f"  DRtg médio — Vitórias: {drtg_vitoria:.1f}  |  Derrotas: {drtg_derrota:.1f}  |  Δ = {drtg_derrota - drtg_vitoria:.1f}"
)
delta_off = ortg_vitoria - ortg_derrota
delta_def = drtg_derrota - drtg_vitoria
causa = "OFENSIVA" if delta_off > delta_def else "DEFENSIVA"
print(
    f"\n  → A maior diferença está na {causa} (Δ {max(delta_off, delta_def):.1f} pontos)"
)


# ═══════════════════════════════════════════════════════
# 2. MÉDIA DE PONTOS EM VITÓRIAS vs DERROTAS
# ═══════════════════════════════════════════════════════
print("\n[2] Média de pontos — Vitórias vs Derrotas")
print("-" * 55)

pts_vit = df[df["win"] == 1]["team_pts"].mean()
pts_der = df[df["win"] == 0]["team_pts"].mean()
opp_vit = df[df["win"] == 1]["opp_pts"].mean()
opp_der = df[df["win"] == 0]["opp_pts"].mean()

print(f"  Vitórias  → Denver: {pts_vit:.1f}  |  Adversário: {opp_vit:.1f}")
print(f"  Derrotas  → Denver: {pts_der:.1f}  |  Adversário: {opp_der:.1f}")


# ═══════════════════════════════════════════════════════
# 3. eFG% e TOV% COLETIVO
# ═══════════════════════════════════════════════════════
print("\n[3] Eficiência ofensiva coletiva — Vitórias vs Derrotas")
print("-" * 55)

for col, label in [
    ("off_efg_pct", "eFG% ofensivo"),
    ("off_tov_pct", "TOV% ofensivo"),
    ("def_efg_pct", "eFG% defensivo"),
    ("def_tov_pct", "TOV% defensivo"),
]:
    v = df[df["win"] == 1][col].mean()
    d = df[df["win"] == 0][col].mean()
    print(f"  {label:<22} → Vitória: {v:.3f}  | Derrota: {d:.3f}  | Δ = {v - d:.3f}")


# ═══════════════════════════════════════════════════════
# 4. TURNOVERS COLETIVOS
# ═══════════════════════════════════════════════════════
print("\n[4] Turnovers coletivos vs Resultado")
print("-" * 55)

tov_vit = df[df["win"] == 1]["off_tov_pct"].mean()
tov_der = df[df["win"] == 0]["off_tov_pct"].mean()
t_stat, p_val = stats.ttest_ind(
    df[df["win"] == 1]["off_tov_pct"].dropna(),
    df[df["win"] == 0]["off_tov_pct"].dropna(),
)
print(f"  TOV% médio — Vitória: {tov_vit:.2f}  | Derrota: {tov_der:.2f}")
print(
    f"  Teste t: p = {p_val:.4f} {'✅ Estatisticamente significativo' if p_val < 0.05 else '⚠️  Não significativo'}"
)


# ═══════════════════════════════════════════════════════
# 5. CASA vs FORA
# ═══════════════════════════════════════════════════════
print("\n[5] Performance Casa vs Fora")
print("-" * 55)

casa_fora = df.groupby(["home_away", "win"]).size().unstack(fill_value=0)
for loc in ["Home", "Away"]:
    if loc in casa_fora.index:
        total = casa_fora.loc[loc].sum()
        wins = casa_fora.loc[loc].get(1, 0)
        print(f"  {loc}: {wins}V / {total - wins}D  →  Win rate: {wins/total*100:.1f}%")


# ═══════════════════════════════════════════════════════
# 6. JOKIC — CARREGA MAIS EM DERROTAS?
# ═══════════════════════════════════════════════════════
print("\n[6] Jokic — Carrega mais o time em derrotas?")
print("-" * 55)

for col, label in [
    ("jokic_pts", "Pontos"),
    ("jokic_ast", "Assistências"),
    ("jokic_trb", "Rebotes"),
    ("jokic_fga", "Tentativas FG"),
    ("jokic_usg_proxy", "USG% proxy"),
    ("jokic_plus_minus", "+/-"),
]:
    v = df[df["win"] == 1][col].mean()
    d = df[df["win"] == 0][col].mean()
    flag = "↑ MAIS em derrotas" if d > v else "↑ MAIS em vitórias"
    print(f"  {label:<18} → Vitória: {v:.1f}  | Derrota: {d:.1f}  | {flag}")


# ═══════════════════════════════════════════════════════
# 7. EFICIÊNCIA DO JOKIC
# ═══════════════════════════════════════════════════════
print("\n[7] Eficiência do Jokic — Vitórias vs Derrotas")
print("-" * 55)

for col, label in [
    ("jokic_efg_pct", "eFG%"),
    ("jokic_fg_pct", "FG%"),
    ("jokic_3p_pct", "3P%"),
]:
    v = df[df["win"] == 1][col].mean()
    d = df[df["win"] == 0][col].mean()
    print(f"  {label:<8} → Vitória: {v:.3f}  | Derrota: {d:.3f}  | Δ = {v - d:.3f}")


# ═══════════════════════════════════════════════════════
# 8. ASSISTÊNCIAS DO JOKIC vs RESULTADO
# ═══════════════════════════════════════════════════════
print("\n[8] AST do Jokic vs Resultado")
print("-" * 55)

corr, p = stats.pearsonr(
    df["jokic_ast"].dropna(), df.loc[df["jokic_ast"].notna(), "win"]
)
print(f"  Correlação AST × win: r = {corr:.3f}  |  p = {p:.4f}")
print(
    f"  {'✅ Correlação significativa' if p < 0.05 else '⚠️  Sem correlação significativa'}"
)

df["ast_faixa"] = pd.cut(
    df["jokic_ast"], bins=[0, 6, 10, 15, 30], labels=["1-6", "7-10", "11-15", "15+"]
)
ast_win = df.groupby("ast_faixa", observed=False)["win"].mean().round(3)
print(f"\n  Win rate por faixa de AST:\n{ast_win.to_string()}")


# ═══════════════════════════════════════════════════════
# 9. TOV DO JOKIC vs RESULTADO
# ═══════════════════════════════════════════════════════
print("\n[9] TOV do Jokic vs Resultado")
print("-" * 55)

corr_tov, p_tov = stats.pearsonr(
    df["jokic_tov"].dropna(), df.loc[df["jokic_tov"].notna(), "win"]
)
print(f"  Correlação TOV × win: r = {corr_tov:.3f}  |  p = {p_tov:.4f}")

tov_vit = df[df["win"] == 1]["jokic_tov"].mean()
tov_der = df[df["win"] == 0]["jokic_tov"].mean()
print(f"  TOV médio — Vitória: {tov_vit:.1f}  | Derrota: {tov_der:.1f}")


# ═══════════════════════════════════════════════════════
# 10. TRIPLO-DUPLO → TAXA DE VITÓRIA
# ═══════════════════════════════════════════════════════
print("\n[10] Triplo-duplo → Taxa de vitória")
print("-" * 55)

td = df.groupby("triple_double")["win"].agg(["sum", "count", "mean"])
for idx, row in td.iterrows():
    label = "Com TD " if idx == 1 else "Sem TD"
    print(
        f"  {label}: {int(row['sum'])}V / {int(row['count'] - row['sum'])}D  →  Win rate: {row['mean']*100:.1f}%"
    )


# ═══════════════════════════════════════════════════════
# 11. PLAYOFFS vs REGULAR SEASON
# ═══════════════════════════════════════════════════════
print("\n[11] Playoffs vs Regular Season")
print("-" * 55)

comp = (
    df.groupby("season_type")
    .agg(
        jogos=("win", "count"),
        win_rate=("win", "mean"),
        jokic_pts=("jokic_pts", "mean"),
        jokic_ast=("jokic_ast", "mean"),
        jokic_usg=("jokic_usg_proxy", "mean"),
        ortg=("ortg", "mean"),
        drtg=("drtg", "mean"),
    )
    .round(2)
)
print(comp.to_string())


# ═══════════════════════════════════════════════════════
# 12. HIPÓTESE: 3P% COLETIVO É O MAIOR FATOR?
# ═══════════════════════════════════════════════════════
print("\n[12] Correlação de variáveis com vitória")
print("-" * 55)

vars_analise = [
    "ortg",
    "drtg",
    "off_efg_pct",
    "def_efg_pct",
    "off_tov_pct",
    "off_orb_pct",
    "3par",
    "jokic_pts",
    "jokic_ast",
    "jokic_efg_pct",
    "jokic_usg_proxy",
    "jokic_plus_minus",
    "triple_double",
]

correlacoes = {}
for var in vars_analise:
    if var in df.columns:
        subset = df[[var, "win"]].dropna()
        if len(subset) > 10:
            r, p = stats.pearsonr(subset[var], subset["win"])
            correlacoes[var] = {
                "r": round(r, 3),
                "p": round(p, 4),
                "sig": "✅" if p < 0.05 else "⚠️ ",
            }

corr_df = pd.DataFrame(correlacoes).T.sort_values("r", key=abs, ascending=False)
print(corr_df.to_string())

maior_fator = corr_df["r"].abs().idxmax()
print(
    f"\n  → Variável com maior correlação com vitória: '{maior_fator}' (r = {corr_df.loc[maior_fator, 'r']})"
)
print(
    f"  → Hipótese 3PAr como maior fator: {'✅ CONFIRMADA' if maior_fator == '3par' else f'❌ REFUTADA — maior fator é {maior_fator}'}"
)


# ═══════════════════════════════════════════════════════
# GRÁFICOS
# ═══════════════════════════════════════════════════════
print("\n📊 Gerando gráficos...")

from matplotlib.lines import Line2D

# Corrige outliers de percentual antes de plotar
for col in [
    "jokic_efg_pct",
    "jokic_fg_pct",
    "jokic_3p_pct",
    "jokic_ft_pct",
    "off_efg_pct",
    "def_efg_pct",
]:
    df.loc[df[col] > 1.5, col] = np.nan

vit = df[df["win"] == 1]
der = df[df["win"] == 0]

# Recalcula médias com dados limpos
ortg_vitoria = vit["ortg"].mean()
ortg_derrota = der["ortg"].mean()
drtg_vitoria = vit["drtg"].mean()
drtg_derrota = der["drtg"].mean()
pts_vit = vit["team_pts"].mean()
pts_der = der["team_pts"].mean()
opp_vit = vit["opp_pts"].mean()
opp_der = der["opp_pts"].mean()
tov_vit = vit["jokic_tov"].mean()
tov_der = der["jokic_tov"].mean()
home_wr = df[df["home_away"] == "Home"]["win"].mean() * 100
away_wr = df[df["home_away"] == "Away"]["win"].mean() * 100
td_wr = df[df["triple_double"] == 1]["win"].mean() * 100
notd_wr = df[df["triple_double"] == 0]["win"].mean() * 100
home_n = df[df["home_away"] == "Home"]["win"].count()
away_n = df[df["home_away"] == "Away"]["win"].count()
td_n = df[df["triple_double"] == 1]["win"].count()
ntd_n = df[df["triple_double"] == 0]["win"].count()

df["ast_faixa"] = pd.cut(
    df["jokic_ast"], bins=[0, 6, 10, 15, 30], labels=["1-6", "7-10", "11-15", "15+"]
)
ast_win = df.groupby("ast_faixa", observed=False)["win"].mean() * 100

# Correlações para o gráfico
labels_map = {
    "ortg": "ORtg",
    "drtg": "DRtg",
    "off_efg_pct": "eFG% Off",
    "def_efg_pct": "eFG% Def",
    "off_tov_pct": "TOV% Off",
    "jokic_pts": "Jokic PTS",
    "jokic_ast": "Jokic AST",
    "jokic_efg_pct": "Jokic eFG%",
    "jokic_plus_minus": "Jokic +/-",
    "triple_double": "Triplo-Duplo",
}
corr_vals = {}
for var in labels_map:
    if var in df.columns:
        subset = df[[var, "win"]].dropna()
        if len(subset) > 10:
            r, _ = stats.pearsonr(subset[var], subset["win"])
            corr_vals[labels_map[var]] = round(r, 3)
corr_s = pd.Series(corr_vals).sort_values(key=abs, ascending=False)

# ── Layout ──────────────────────────────────────────────
fig = plt.figure(figsize=(22, 28), facecolor="#F0F4F8")
fig.suptitle(
    "Strategic Performance Analysis – Denver Nuggets",
    fontsize=22,
    fontweight="bold",
    color=DENVER_BLUE,
    y=0.985,
)
gs = gridspec.GridSpec(
    4,
    3,
    figure=fig,
    hspace=0.55,
    wspace=0.38,
    top=0.95,
    bottom=0.04,
    left=0.07,
    right=0.97,
)


def style_ax(ax, title):
=======

# HELPERS
def style_ax(ax, title: str) -> None:
    """Aplica estilo padrão Denver num eixo."""
>>>>>>> 428fafe (script principal com análise estatística)
    ax.set_title(title, fontsize=12, fontweight="bold", color=DENVER_BLUE, pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)


<<<<<<< HEAD
GREEN = "#27ae60"
RED = "#e74c3c"
GRAY = "#95a5a6"
w = 0.32

# ── G1: ORtg vs DRtg ──────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
cats = ["ORtg\nVitória", "ORtg\nDerrota", "DRtg\nVitória", "DRtg\nDerrota"]
vals = [ortg_vitoria, ortg_derrota, drtg_vitoria, drtg_derrota]
clrs = [GREEN, RED, GREEN, RED]
bars = ax1.bar(cats, vals, color=clrs, edgecolor="white", linewidth=1.5, width=0.55)
ax1.set_ylim(90, 145)
for bar, val in zip(bars, vals):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.4,
        f"{val:.1f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax1.set_ylabel("Rating", fontsize=9)
style_ax(ax1, "ORtg vs DRtg por Resultado")

# ── G2: Pontos ────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
x2 = np.arange(2)
b1 = ax2.bar(
    x2 - w / 2,
    [pts_vit, pts_der],
    w,
    label="Denver",
    color=DENVER_BLUE,
    edgecolor="white",
)
b2 = ax2.bar(
    x2 + w / 2,
    [opp_vit, opp_der],
    w,
    label="Adversário",
    color=DENVER_GOLD,
    edgecolor="white",
)
ax2.set_xticks(x2)
ax2.set_xticklabels(["Vitória", "Derrota"])
ax2.set_ylim(90, 130)
for bar in list(b1) + list(b2):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{bar.get_height():.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax2.legend(fontsize=9)
ax2.set_ylabel("Pontos", fontsize=9)
style_ax(ax2, "Pontos — Vitória vs Derrota")

# ── G3: Correlações ───────────────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
bar_clrs = [GREEN if v > 0 else RED for v in corr_s.values]
ax3.barh(
    corr_s.index[::-1],
    corr_s.values[::-1],
    color=bar_clrs[::-1],
    edgecolor="white",
    height=0.6,
)
ax3.axvline(0, color="black", linewidth=0.8)
ax3.set_xlabel("r de Pearson", fontsize=9)
ax3.tick_params(axis="y", labelsize=8)
style_ax(ax3, "Correlação com Vitória")

# ── G4: Casa vs Fora ──────────────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
bars4 = ax4.bar(
    ["Casa", "Fora"],
    [home_wr, away_wr],
    color=[DENVER_BLUE, DENVER_GOLD],
    edgecolor="white",
    width=0.5,
)
ax4.set_ylim(0, 110)
for bar, val, n in zip(bars4, [home_wr, away_wr], [home_n, away_n]):
    ax4.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.5,
        f"{val:.1f}%\n({n} jogos)",
        ha="center",
        fontsize=9,
        fontweight="bold",
    )
ax4.set_ylabel("Win Rate (%)", fontsize=9)
style_ax(ax4, "Win Rate — Casa vs Fora")

# ── G5: Jokic stats ───────────────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
s_cols = ["jokic_pts", "jokic_ast", "jokic_trb"]
s_labels = ["Pontos", "Assistências", "Rebotes"]
vit_vals = [vit[c].mean() for c in s_cols]
der_vals = [der[c].mean() for c in s_cols]
x5 = np.arange(3)
bv = ax5.bar(
    x5 - w / 2, vit_vals, w * 1.1, label="Vitória", color=GREEN, edgecolor="white"
)
bd = ax5.bar(
    x5 + w / 2, der_vals, w * 1.1, label="Derrota", color=RED, edgecolor="white"
)
ax5.set_xticks(x5)
ax5.set_xticklabels(s_labels, fontsize=9)
for bar in list(bv) + list(bd):
    ax5.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        f"{bar.get_height():.1f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )
ax5.legend(fontsize=9)
style_ax(ax5, "Jokic — Stats por Resultado")

# ── G6: Triplo-duplo ──────────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
bars6 = ax6.bar(
    ["Com\nTriplo-Duplo", "Sem\nTriplo-Duplo"],
    [td_wr, notd_wr],
    color=[DENVER_BLUE, GRAY],
    edgecolor="white",
    width=0.5,
)
ax6.set_ylim(0, 110)
for bar, val, n in zip(bars6, [td_wr, notd_wr], [td_n, ntd_n]):
    ax6.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.5,
        f"{val:.1f}%\n({n} jogos)",
        ha="center",
        fontsize=9,
        fontweight="bold",
    )
ax6.set_ylabel("Win Rate (%)", fontsize=9)
style_ax(ax6, "Win Rate — Triplo-Duplo")

# ── G7: AST faixas ────────────────────────────────────
ax7 = fig.add_subplot(gs[2, 0])
bars7 = ax7.bar(
    ast_win.index.astype(str),
    ast_win.values,
    color=DENVER_BLUE,
    edgecolor="white",
    width=0.5,
)
ax7.set_ylim(0, 110)
for bar, val in zip(bars7, ast_win.values):
    if not np.isnan(val):
        ax7.text(
            bar.get_x() + bar.get_width() / 2,
            val + 1.5,
            f"{val:.0f}%",
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=DENVER_BLUE,
        )
ax7.set_xlabel("Assistências do Jokic", fontsize=9)
ax7.set_ylabel("Win Rate (%)", fontsize=9)
style_ax(ax7, "Win Rate por Faixa de AST")

# ── G8: eFG% histograma ───────────────────────────────
ax8 = fig.add_subplot(gs[2, 1])
efg_v = vit["off_efg_pct"].dropna()
efg_d = der["off_efg_pct"].dropna()
ax8.hist(
    efg_v,
    bins=12,
    alpha=0.75,
    color=GREEN,
    label=f"Vitória (μ={efg_v.mean():.3f})",
    edgecolor="white",
)
ax8.hist(
    efg_d,
    bins=12,
    alpha=0.75,
    color=RED,
    label=f"Derrota (μ={efg_d.mean():.3f})",
    edgecolor="white",
)
ax8.axvline(efg_v.mean(), color=GREEN, linestyle="--", linewidth=1.5)
ax8.axvline(efg_d.mean(), color=RED, linestyle="--", linewidth=1.5)
ax8.set_xlabel("eFG% Ofensivo", fontsize=9)
ax8.set_ylabel("Frequência", fontsize=9)
ax8.legend(fontsize=8)
style_ax(ax8, "Distribuição eFG% Ofensivo")

# ── G9: USG% boxplot ──────────────────────────────────
ax9 = fig.add_subplot(gs[2, 2])
reg_usg = df[df["season_type"] == "Regular"]["jokic_usg_proxy"].dropna()
ply_usg = df[df["season_type"] == "Playoffs"]["jokic_usg_proxy"].dropna()
ax9.boxplot(
    [reg_usg, ply_usg],
    labels=["Regular\nSeason", "Playoffs"],
    patch_artist=True,
    widths=0.45,
    boxprops=dict(facecolor=DENVER_BLUE, color=DENVER_BLUE, alpha=0.8),
    medianprops=dict(color=DENVER_GOLD, linewidth=2.5),
    whiskerprops=dict(color=DENVER_BLUE),
    capprops=dict(color=DENVER_BLUE),
    flierprops=dict(marker="o", color=GRAY, markersize=4),
)
ax9.set_ylabel("USG% (proxy)", fontsize=9)
style_ax(ax9, "USG% Jokic — Regular vs Playoffs")

# ── G10: +/- boxplot ──────────────────────────────────
ax10 = fig.add_subplot(gs[3, 0])
pm_vit = vit["jokic_plus_minus"].dropna()
pm_der = der["jokic_plus_minus"].dropna()
ax10.boxplot(
    [pm_vit, pm_der],
    labels=["Vitória", "Derrota"],
    patch_artist=True,
    widths=0.45,
    boxprops=dict(facecolor=GREEN, alpha=0.8),
    medianprops=dict(color="white", linewidth=2.5),
    whiskerprops=dict(color="#555"),
    capprops=dict(color="#555"),
    flierprops=dict(marker="o", color=GRAY, markersize=4),
)
ax10.axhline(0, color=RED, linestyle="--", linewidth=1.2)
ax10.set_ylabel("+/-", fontsize=9)
style_ax(ax10, "+/- Jokic por Resultado")

# ── G11: ORtg vs DRtg scatter ─────────────────────────
ax11 = fig.add_subplot(gs[3, 1])
ax11.scatter(
    vit["ortg"],
    vit["drtg"],
    c=GREEN,
    alpha=0.65,
    s=55,
    edgecolors="white",
    linewidth=0.5,
    label="Vitória",
    zorder=3,
)
ax11.scatter(
    der["ortg"],
    der["drtg"],
    c=RED,
    alpha=0.65,
    s=55,
    edgecolors="white",
    linewidth=0.5,
    label="Derrota",
    zorder=3,
)
ax11.set_xlabel("ORtg", fontsize=9)
ax11.set_ylabel("DRtg", fontsize=9)
ax11.legend(fontsize=9)
style_ax(ax11, "ORtg vs DRtg por Jogo")

# ── G12: TOV Jokic ────────────────────────────────────
ax12 = fig.add_subplot(gs[3, 2])
bars12 = ax12.bar(
    ["Vitória", "Derrota"],
    [tov_vit, tov_der],
    color=[GREEN, RED],
    edgecolor="white",
    width=0.5,
)
ax12.set_ylim(0, 5)
for bar, val in zip(bars12, [tov_vit, tov_der]):
    ax12.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{val:.1f}",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )
ax12.set_ylabel("TOV médio", fontsize=9)
style_ax(ax12, "Turnovers Jokic — Vitória vs Derrota")

# ── Salvar ────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = OUTPUT_DIR / "nuggets_analise.png"
plt.savefig(output_file, dpi=150, bbox_inches="tight", facecolor="#F0F4F8")
plt.show()
print(f"\n✅ Gráficos salvos em: {output_file}")
print("\n🏀 Análise completa!")
=======
def mean_by_result(df: pd.DataFrame, col: str):
    """Retorna (media_vitoria, media_derrota) para uma coluna."""
    v = df.loc[df["win"] == 1, col].mean()
    d = df.loc[df["win"] == 0, col].mean()
    return v, d


# CARREGAMENTO E PRÉ-PROCESSAMENTO
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"✅  Dataset carregado: {df.shape[0]} jogos × {df.shape[1]} colunas\n")

    # USG% proxy: (FGA + 0,44·FTA_est + TOV) / min * 36
    df["jokic_fta_est"] = df["jokic_fga"] / df["jokic_fg_pct"].replace(0, np.nan)
    df["jokic_usg_proxy"] = (
        (df["jokic_fga"] + 0.44 * df["jokic_fta_est"].fillna(0) + df["jokic_tov"])
        / df["jokic_mp"].replace(0, np.nan)
        * 36
    ).round(2)

    # Remove outliers de percentual (valores > 1,5 são erros de escala)
    pct_cols = [
        "jokic_efg_pct",
        "jokic_fg_pct",
        "jokic_3p_pct",
        "jokic_ft_pct",
        "off_efg_pct",
        "def_efg_pct",
    ]
    for col in pct_cols:
        if col in df.columns:
            df.loc[df[col] > 1.5, col] = np.nan

    # Faixas de assistências
    df["ast_faixa"] = pd.cut(
        df["jokic_ast"],
        bins=[0, 6, 10, 15, 30],
        labels=["1-6", "7-10", "11-15", "15+"],
    )

    return df


# ANÁLISE TEXTUAL
def run_analysis(df: pd.DataFrame) -> None:
    vit = df[df["win"] == 1]
    der = df[df["win"] == 0]

    sep = "=" * 60
    print(sep)
    print("  ANÁLISE DENVER NUGGETS – RELATÓRIO COMPLETO")
    print(sep)

    # 1. Ofensiva vs Defensiva
    print("\n[1] Denver perde mais por falha OFENSIVA ou DEFENSIVA?")
    print("-" * 55)
    ortg_v, ortg_d = mean_by_result(df, "ortg")
    drtg_v, drtg_d = mean_by_result(df, "drtg")
    delta_off = ortg_v - ortg_d
    delta_def = drtg_d - drtg_v
    causa = "OFENSIVA" if delta_off > delta_def else "DEFENSIVA"
    print(
        f"  ORtg — Vitórias: {ortg_v:.1f}  |  Derrotas: {ortg_d:.1f}  |  Δ = {delta_off:.1f}"
    )
    print(
        f"  DRtg — Vitórias: {drtg_v:.1f}  |  Derrotas: {drtg_d:.1f}  |  Δ = {delta_def:.1f}"
    )
    print(f"\n  → Maior diferença: {causa} (Δ {max(delta_off, delta_def):.1f} pts)")

    # 2. Pontos
    print("\n[2] Pontos — Vitórias vs Derrotas")
    print("-" * 55)
    pts_v, pts_d = mean_by_result(df, "team_pts")
    opp_v, opp_d = mean_by_result(df, "opp_pts")
    print(f"  Vitórias  → Denver: {pts_v:.1f}  |  Adversário: {opp_v:.1f}")
    print(f"  Derrotas  → Denver: {pts_d:.1f}  |  Adversário: {opp_d:.1f}")

    # 3. eFG% e TOV% coletivos
    print("\n[3] Eficiência coletiva — Vitórias vs Derrotas")
    print("-" * 55)
    for col, label in [
        ("off_efg_pct", "eFG% ofensivo"),
        ("off_tov_pct", "TOV% ofensivo"),
        ("def_efg_pct", "eFG% defensivo"),
        ("def_tov_pct", "TOV% defensivo"),
    ]:
        if col in df.columns:
            v, d = mean_by_result(df, col)
            print(
                f"  {label:<22} → Vitória: {v:.3f}  | Derrota: {d:.3f}  | Δ = {v - d:.3f}"
            )

    # 4. TOV% teste estatístico
    print("\n[4] Turnovers coletivos — teste t")
    print("-" * 55)
    tov_v, tov_d = mean_by_result(df, "off_tov_pct")
    t_stat, p_val = stats.ttest_ind(
        vit["off_tov_pct"].dropna(), der["off_tov_pct"].dropna()
    )
    sig = "✅ Significativo" if p_val < 0.05 else "⚠️  Não significativo"
    print(f"  TOV% — Vitória: {tov_v:.2f}  | Derrota: {tov_d:.2f}")
    print(f"  Teste t: p = {p_val:.4f}  {sig}")

    # 5. Casa vs Fora
    print("\n[5] Performance Casa vs Fora")
    print("-" * 55)
    for loc in ["Home", "Away"]:
        sub = df[df["home_away"] == loc]
        if len(sub):
            wr = sub["win"].mean() * 100
            print(
                f"  {loc}: {sub['win'].sum():.0f}V / {(~sub['win'].astype(bool)).sum()}D  →  Win rate: {wr:.1f}%"
            )

    # 6. Jokic — carrega mais em derrotas?
    print("\n[6] Jokic — carrega mais o time em derrotas?")
    print("-" * 55)
    for col, label in [
        ("jokic_pts", "Pontos"),
        ("jokic_ast", "Assistências"),
        ("jokic_trb", "Rebotes"),
        ("jokic_fga", "Tentativas FG"),
        ("jokic_usg_proxy", "USG% proxy"),
        ("jokic_plus_minus", "+/-"),
    ]:
        if col in df.columns:
            v, d = mean_by_result(df, col)
            flag = "↑ MAIS em derrotas" if d > v else "↑ MAIS em vitórias"
            print(f"  {label:<18} → Vitória: {v:.1f}  | Derrota: {d:.1f}  | {flag}")

    # 7. Eficiência Jokic
    print("\n[7] Eficiência Jokic — Vitórias vs Derrotas")
    print("-" * 55)
    for col, label in [
        ("jokic_efg_pct", "eFG%"),
        ("jokic_fg_pct", "FG%"),
        ("jokic_3p_pct", "3P%"),
    ]:
        if col in df.columns:
            v, d = mean_by_result(df, col)
            print(
                f"  {label:<8} → Vitória: {v:.3f}  | Derrota: {d:.3f}  | Δ = {v - d:.3f}"
            )

    # 8. AST Jokic × Resultado
    print("\n[8] AST Jokic × Resultado")
    print("-" * 55)
    corr, p = stats.pearsonr(
        df["jokic_ast"].dropna(), df.loc[df["jokic_ast"].notna(), "win"]
    )
    sig = "✅ Significativo" if p < 0.05 else "⚠️  Sem correlação significativa"
    print(f"  r = {corr:.3f}  |  p = {p:.4f}  {sig}")
    ast_win = df.groupby("ast_faixa", observed=False)["win"].mean().round(3)
    print(f"\n  Win rate por faixa de AST:\n{ast_win.to_string()}")

    # 9. TOV Jokic
    print("\n[9] TOV Jokic × Resultado")
    print("-" * 55)
    corr_tov, p_tov = stats.pearsonr(
        df["jokic_tov"].dropna(), df.loc[df["jokic_tov"].notna(), "win"]
    )
    tov_v, tov_d = mean_by_result(df, "jokic_tov")
    print(f"  r = {corr_tov:.3f}  |  p = {p_tov:.4f}")
    print(f"  TOV médio — Vitória: {tov_v:.1f}  | Derrota: {tov_d:.1f}")

    # 10. Triplo-duplo
    print("\n[10] Triplo-duplo → Win rate")
    print("-" * 55)
    td = df.groupby("triple_double")["win"].agg(["sum", "count", "mean"])
    for idx, row in td.iterrows():
        label = "Com TD " if idx == 1 else "Sem TD"
        print(
            f"  {label}: {int(row['sum'])}V / {int(row['count'] - row['sum'])}D  →  {row['mean']*100:.1f}%"
        )

    # 11. Playoffs vs Regular Season
    print("\n[11] Playoffs vs Regular Season")
    print("-" * 55)
    agg_cols = {
        "jogos": ("win", "count"),
        "win_rate": ("win", "mean"),
        "jokic_pts": ("jokic_pts", "mean"),
        "jokic_ast": ("jokic_ast", "mean"),
        "jokic_usg": ("jokic_usg_proxy", "mean"),
        "ortg": ("ortg", "mean"),
        "drtg": ("drtg", "mean"),
    }
    comp = df.groupby("season_type").agg(**agg_cols).round(2)
    print(comp.to_string())

    # 12. Correlações com vitória
    print("\n[12] Correlação de variáveis com vitória")
    print("-" * 55)
    vars_analise = [
        "ortg",
        "drtg",
        "off_efg_pct",
        "def_efg_pct",
        "off_tov_pct",
        "off_orb_pct",
        "3par",
        "jokic_pts",
        "jokic_ast",
        "jokic_efg_pct",
        "jokic_usg_proxy",
        "jokic_plus_minus",
        "triple_double",
    ]
    correlacoes = {}
    for var in vars_analise:
        if var in df.columns:
            subset = df[[var, "win"]].dropna()
            if len(subset) > 10:
                r, p = stats.pearsonr(subset[var], subset["win"])
                correlacoes[var] = {
                    "r": round(r, 3),
                    "p": round(p, 4),
                    "sig": "✅" if p < 0.05 else "⚠️ ",
                }

    corr_df = pd.DataFrame(correlacoes).T.sort_values("r", key=abs, ascending=False)
    print(corr_df.to_string())
    maior = corr_df["r"].abs().idxmax()
    confirmada = (
        "✅ CONFIRMADA" if maior == "3par" else f"❌ REFUTADA — maior fator: {maior}"
    )
    print(f"\n  → Maior correlação: '{maior}' (r = {corr_df.loc[maior, 'r']})")
    print(f"  → Hipótese 3PAr como maior fator: {confirmada}")

    return corr_df


# GRÁFICOS
def build_charts(df: pd.DataFrame, corr_df: pd.DataFrame, output_dir: Path) -> None:
    print("\n📊  Gerando gráficos...")

    vit = df[df["win"] == 1]
    der = df[df["win"] == 0]
    w = 0.32  # largura das barras agrupadas

    # Pré-cálculo de valores
    ortg_v, ortg_d = mean_by_result(df, "ortg")
    drtg_v, drtg_d = mean_by_result(df, "drtg")
    pts_v, pts_d = mean_by_result(df, "team_pts")
    opp_v, opp_d = mean_by_result(df, "opp_pts")
    tov_v, tov_d = mean_by_result(df, "jokic_tov")

    home_wr = df[df["home_away"] == "Home"]["win"].mean() * 100
    away_wr = df[df["home_away"] == "Away"]["win"].mean() * 100
    home_n = (df["home_away"] == "Home").sum()
    away_n = (df["home_away"] == "Away").sum()

    td_wr = df[df["triple_double"] == 1]["win"].mean() * 100
    ntd_wr = df[df["triple_double"] == 0]["win"].mean() * 100
    td_n = (df["triple_double"] == 1).sum()
    ntd_n = (df["triple_double"] == 0).sum()

    ast_win = df.groupby("ast_faixa", observed=False)["win"].mean() * 100

    # Correlações para o gráfico de barras horizontais
    labels_map = {
        "ortg": "ORtg",
        "drtg": "DRtg",
        "off_efg_pct": "eFG% Off",
        "def_efg_pct": "eFG% Def",
        "off_tov_pct": "TOV% Off",
        "jokic_pts": "Jokic PTS",
        "jokic_ast": "Jokic AST",
        "jokic_efg_pct": "Jokic eFG%",
        "jokic_plus_minus": "Jokic +/-",
        "triple_double": "Triplo-Duplo",
    }
    corr_vals = {}
    for var, lbl in labels_map.items():
        if var in df.columns:
            subset = df[[var, "win"]].dropna()
            if len(subset) > 10:
                r, _ = stats.pearsonr(subset[var], subset["win"])
                corr_vals[lbl] = round(r, 3)
    corr_s = pd.Series(corr_vals).sort_values(key=abs, ascending=False)

    # Layout
    fig = plt.figure(figsize=(22, 28), facecolor="#F0F4F8")
    fig.suptitle(
        "Strategic Performance Analysis – Denver Nuggets",
        fontsize=22,
        fontweight="bold",
        color=DENVER_BLUE,
        y=0.985,
    )
    gs = gridspec.GridSpec(
        4,
        3,
        figure=fig,
        hspace=0.55,
        wspace=0.38,
        top=0.95,
        bottom=0.04,
        left=0.07,
        right=0.97,
    )

    # G1 — ORtg vs DRtg
    ax1 = fig.add_subplot(gs[0, 0])
    cats = ["ORtg\nVitória", "ORtg\nDerrota", "DRtg\nVitória", "DRtg\nDerrota"]
    vals = [ortg_v, ortg_d, drtg_v, drtg_d]
    clrs = [WIN_COLOR, LOSS_COLOR, WIN_COLOR, LOSS_COLOR]
    bars = ax1.bar(cats, vals, color=clrs, edgecolor="white", linewidth=1.5, width=0.55)
    ax1.set_ylim(90, 145)
    for bar, val in zip(bars, vals):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    ax1.set_ylabel("Rating", fontsize=9)
    style_ax(ax1, "ORtg vs DRtg por Resultado")

    # G2 — Pontos
    ax2 = fig.add_subplot(gs[0, 1])
    x2 = np.arange(2)
    b1 = ax2.bar(
        x2 - w / 2,
        [pts_v, pts_d],
        w,
        label="Denver",
        color=DENVER_BLUE,
        edgecolor="white",
    )
    b2 = ax2.bar(
        x2 + w / 2,
        [opp_v, opp_d],
        w,
        label="Adversário",
        color=DENVER_GOLD,
        edgecolor="white",
    )
    ax2.set_xticks(x2)
    ax2.set_xticklabels(["Vitória", "Derrota"])
    ax2.set_ylim(90, 130)
    for bar in list(b1) + list(b2):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"{bar.get_height():.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    ax2.legend(fontsize=9)
    ax2.set_ylabel("Pontos", fontsize=9)
    style_ax(ax2, "Pontos — Vitória vs Derrota")

    # G3 — Correlações
    ax3 = fig.add_subplot(gs[0, 2])
    bar_clrs = [WIN_COLOR if v > 0 else LOSS_COLOR for v in corr_s.values]
    ax3.barh(
        corr_s.index[::-1],
        corr_s.values[::-1],
        color=bar_clrs[::-1],
        edgecolor="white",
        height=0.6,
    )
    ax3.axvline(0, color="black", linewidth=0.8)
    ax3.set_xlabel("r de Pearson", fontsize=9)
    ax3.tick_params(axis="y", labelsize=8)
    style_ax(ax3, "Correlação com Vitória")

    # G4 — Casa vs Fora
    ax4 = fig.add_subplot(gs[1, 0])
    bars4 = ax4.bar(
        ["Casa", "Fora"],
        [home_wr, away_wr],
        color=[DENVER_BLUE, DENVER_GOLD],
        edgecolor="white",
        width=0.5,
    )
    ax4.set_ylim(0, 110)
    for bar, val, n in zip(bars4, [home_wr, away_wr], [home_n, away_n]):
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{val:.1f}%\n({n} jogos)",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )
    ax4.set_ylabel("Win Rate (%)", fontsize=9)
    style_ax(ax4, "Win Rate — Casa vs Fora")

    # G5 — Jokic stats
    ax5 = fig.add_subplot(gs[1, 1])
    s_cols = ["jokic_pts", "jokic_ast", "jokic_trb"]
    s_labels = ["Pontos", "Assistências", "Rebotes"]
    vit_vals = [vit[c].mean() for c in s_cols]
    der_vals = [der[c].mean() for c in s_cols]
    x5 = np.arange(3)
    bv = ax5.bar(
        x5 - w / 2,
        vit_vals,
        w * 1.1,
        label="Vitória",
        color=WIN_COLOR,
        edgecolor="white",
    )
    bd = ax5.bar(
        x5 + w / 2,
        der_vals,
        w * 1.1,
        label="Derrota",
        color=LOSS_COLOR,
        edgecolor="white",
    )
    ax5.set_xticks(x5)
    ax5.set_xticklabels(s_labels, fontsize=9)
    for bar in list(bv) + list(bd):
        ax5.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{bar.get_height():.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    ax5.legend(fontsize=9)
    style_ax(ax5, "Jokic — Stats por Resultado")

    # G6 — Triplo-duplo
    ax6 = fig.add_subplot(gs[1, 2])
    bars6 = ax6.bar(
        ["Com\nTriplo-Duplo", "Sem\nTriplo-Duplo"],
        [td_wr, ntd_wr],
        color=[DENVER_BLUE, GRAY],
        edgecolor="white",
        width=0.5,
    )
    ax6.set_ylim(0, 110)
    for bar, val, n in zip(bars6, [td_wr, ntd_wr], [td_n, ntd_n]):
        ax6.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            f"{val:.1f}%\n({n} jogos)",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )
    ax6.set_ylabel("Win Rate (%)", fontsize=9)
    style_ax(ax6, "Win Rate — Triplo-Duplo")

    # G7 — AST faixas
    ax7 = fig.add_subplot(gs[2, 0])
    bars7 = ax7.bar(
        ast_win.index.astype(str),
        ast_win.values,
        color=DENVER_BLUE,
        edgecolor="white",
        width=0.5,
    )
    ax7.set_ylim(0, 110)
    for bar, val in zip(bars7, ast_win.values):
        if not np.isnan(val):
            ax7.text(
                bar.get_x() + bar.get_width() / 2,
                val + 1.5,
                f"{val:.0f}%",
                ha="center",
                fontsize=9,
                fontweight="bold",
                color=DENVER_BLUE,
            )
    ax7.set_xlabel("Assistências do Jokic", fontsize=9)
    ax7.set_ylabel("Win Rate (%)", fontsize=9)
    style_ax(ax7, "Win Rate por Faixa de AST")

    # G8 — eFG% histograma
    ax8 = fig.add_subplot(gs[2, 1])
    efg_v = vit["off_efg_pct"].dropna()
    efg_d = der["off_efg_pct"].dropna()
    ax8.hist(
        efg_v,
        bins=12,
        alpha=0.75,
        color=WIN_COLOR,
        label=f"Vitória (μ={efg_v.mean():.3f})",
        edgecolor="white",
    )
    ax8.hist(
        efg_d,
        bins=12,
        alpha=0.75,
        color=LOSS_COLOR,
        label=f"Derrota (μ={efg_d.mean():.3f})",
        edgecolor="white",
    )
    ax8.axvline(efg_v.mean(), color=WIN_COLOR, linestyle="--", linewidth=1.5)
    ax8.axvline(efg_d.mean(), color=LOSS_COLOR, linestyle="--", linewidth=1.5)
    ax8.set_xlabel("eFG% Ofensivo", fontsize=9)
    ax8.set_ylabel("Frequência", fontsize=9)
    ax8.legend(fontsize=8)
    style_ax(ax8, "Distribuição eFG% Ofensivo")

    # G9 — USG% boxplot
    ax9 = fig.add_subplot(gs[2, 2])
    reg_usg = df[df["season_type"] == "Regular"]["jokic_usg_proxy"].dropna()
    ply_usg = df[df["season_type"] == "Playoffs"]["jokic_usg_proxy"].dropna()
    ax9.boxplot(
        [reg_usg, ply_usg],
        labels=["Regular\nSeason", "Playoffs"],
        patch_artist=True,
        widths=0.45,
        boxprops=dict(facecolor=DENVER_BLUE, color=DENVER_BLUE, alpha=0.8),
        medianprops=dict(color=DENVER_GOLD, linewidth=2.5),
        whiskerprops=dict(color=DENVER_BLUE),
        capprops=dict(color=DENVER_BLUE),
        flierprops=dict(marker="o", color=GRAY, markersize=4),
    )
    ax9.set_ylabel("USG% (proxy)", fontsize=9)
    style_ax(ax9, "USG% Jokic — Regular vs Playoffs")

    # G10 — +/- boxplot
    ax10 = fig.add_subplot(gs[3, 0])
    pm_vit = vit["jokic_plus_minus"].dropna()
    pm_der = der["jokic_plus_minus"].dropna()
    ax10.boxplot(
        [pm_vit, pm_der],
        labels=["Vitória", "Derrota"],
        patch_artist=True,
        widths=0.45,
        boxprops=dict(facecolor=WIN_COLOR, alpha=0.8),
        medianprops=dict(color="white", linewidth=2.5),
        whiskerprops=dict(color="#555"),
        capprops=dict(color="#555"),
        flierprops=dict(marker="o", color=GRAY, markersize=4),
    )
    ax10.axhline(0, color=LOSS_COLOR, linestyle="--", linewidth=1.2)
    ax10.set_ylabel("+/-", fontsize=9)
    style_ax(ax10, "+/- Jokic por Resultado")

    # G11 — ORtg vs DRtg scatter
    ax11 = fig.add_subplot(gs[3, 1])
    ax11.scatter(
        vit["ortg"],
        vit["drtg"],
        c=WIN_COLOR,
        alpha=0.65,
        s=55,
        edgecolors="white",
        linewidth=0.5,
        label="Vitória",
        zorder=3,
    )
    ax11.scatter(
        der["ortg"],
        der["drtg"],
        c=LOSS_COLOR,
        alpha=0.65,
        s=55,
        edgecolors="white",
        linewidth=0.5,
        label="Derrota",
        zorder=3,
    )
    ax11.set_xlabel("ORtg", fontsize=9)
    ax11.set_ylabel("DRtg", fontsize=9)
    ax11.legend(fontsize=9)
    style_ax(ax11, "ORtg vs DRtg por Jogo")

    # G12 — TOV Jokic
    ax12 = fig.add_subplot(gs[3, 2])
    bars12 = ax12.bar(
        ["Vitória", "Derrota"],
        [tov_v, tov_d],
        color=[WIN_COLOR, LOSS_COLOR],
        edgecolor="white",
        width=0.5,
    )
    ax12.set_ylim(0, 5)
    for bar, val in zip(bars12, [tov_v, tov_d]):
        ax12.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.05,
            f"{val:.1f}",
            ha="center",
            fontsize=11,
            fontweight="bold",
        )
    ax12.set_ylabel("TOV médio", fontsize=9)
    style_ax(ax12, "Turnovers Jokic — Vitória vs Derrota")

    # Salvar
    out_file = output_dir / "nuggets_analise.png"
    plt.savefig(out_file, dpi=150, bbox_inches="tight", facecolor="#F0F4F8")
    plt.show()
    print(f"\n✅  Gráficos salvos em: {out_file}")


# MAIN
def parse_args():
    parser = argparse.ArgumentParser(
        description="Strategic Performance Analysis – Denver Nuggets"
    )
    parser.add_argument(
        "--input",
        "-i",
        default="denver_nuggets_clean.csv",
        help="Caminho para o CSV de entrada (padrão: denver_nuggets_clean.csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="Diretório de saída para os gráficos (padrão: output/)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        print(f"❌  Arquivo não encontrado: {input_path}")
        print("   Coloque o CSV na pasta")
        sys.exit(1)

    df = load_data(str(input_path))
    corr_df = run_analysis(df)
    build_charts(df, corr_df, output_dir)
    print("\n🏀  Análise completa!")


if __name__ == "__main__":
    main()
>>>>>>> 428fafe (script principal com análise estatística)
