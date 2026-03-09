# Strategic Performance Analysis – Denver Nuggets

Análise estratégica do desempenho do Denver Nuggets com foco na correlação entre métricas individuais de Nikola Jokic e os resultados coletivos da equipe. O projeto cobre coleta, limpeza, armazenamento em banco de dados relacional, análise exploratória em Python e visualização no Power BI.

---

## Resumo Executivo

O Denver Nuggets perde por falha coletiva, nao por falha de Jokic. Essa e a descoberta central de uma analise com 13 hipoteses, cobrindo temporada regular e playoffs entre 2022 e 2024.

O Game Score de Jokic se mantem estavel independentemente do resultado — ele performa no mesmo nivel em vitorias e derrotas. O que muda e o time ao redor dele: a eficiencia defensiva (DRtg) cai com clareza nos jogos perdidos, o eFG% coletivo recua e o volume de turnovers ofensivos sobe. Quando Jokic distribui bem — jogos com mais de 11 assistencias ou com triple-double — a taxa de vitoria aumenta de forma expressiva, pois o coletivo arremessa melhor quando ele esta no controle do jogo.

Nos playoffs, o padrao se aprofunda: Jokic eleva seu nivel, mas a defesa coletiva piora diante de adversarios mais qualificados, tornando o time ainda mais dependente de uma performance individual de elite para vencer.

A principal alavanca identificada pelos dados e a defesa coletiva. O ataque tem capacidade — falta consistencia defensiva e reducao de erros ofensivos para converter o talento de Jokic em mais vitorias.

---

## Estrutura do Projeto

```
denver-nuggets-analysis/
│
├── cleaning.py                   # Limpeza e padronização do CSV bruto
├── verification.py               # Verificação rápida do CSV gerado
├── import_postgres.py            # Importação do CSV para PostgreSQL
├── queries.sql                   # Queries analíticas em SQL puro
├── queries_python.py             # Execução das queries e exportação para CSV/Excel
├── analytical_script.py          # Análise exploratória e geração de gráficos em Python
├── denver_nuggets_clean.csv      # Dataset limpo e pronto para uso
├── denver_nuggets_theme.json     # Tema visual do Power BI (cores oficiais dos Nuggets)
├── DASHBOARD.pbix                # Dashboard interativo no Power BI
└── requeriments.txt              # Dependências Python
```

---

## Problema de Negócio

O projeto investiga **o que diferencia as vitórias das derrotas do Denver Nuggets**: falhas ofensivas, defensivas, dependência excessiva de Jokic ou fatores coletivos como turnovers e eficiência de três pontos. A análise busca responder 13 hipóteses específicas sobre padrões de desempenho, tanto na temporada regular quanto nos playoffs.

---

## Dados Analisados

- **Fonte:** Basketball-Reference (estatísticas por jogo)
- **Variáveis coletivas:** ORtg, DRtg, eFG%, 3PAr, TOV%, ORB%, pace, pontos marcados e sofridos
- **Variáveis individuais (Jokic):** pontos, assistências, rebotes, eFG%, FG%, 3P%, FT%, plus/minus, Game Score, minutos, turnovers, triple-doubles
- **Segmentações:** resultado (vitória/derrota), local (casa/fora), tipo de jogo (temporada regular/playoffs)

---

## Análise Realizada

### Hipóteses Investigadas

1. Denver perde mais por falha ofensiva ou defensiva?
2. Media de pontos em vitorias vs derrotas
3. eFG% e taxa de tentativas de tres pontos em vitorias vs derrotas
4. Turnovers coletivos e resultado
5. Performance em casa vs fora
6. Jokic carrega mais o time em derrotas?
7. TS%/eFG% do Jokic em vitorias vs derrotas
8. Assistencias altas do Jokic estao associadas a mais vitorias?
9. TOV do Jokic sao decisivos?
10. Triple-double implica em maior taxa de vitoria?
11. Playoffs vs Temporada Regular — diferencas de desempenho
12. 3P% coletivo e o maior fator de resultado?
13. USG% calculado (FGA + FTA + TOV) por resultado

### Pipeline Tecnico

**1. Limpeza (`cleaning.py`)**
Padronizacao de nomes de colunas, remocao de duplicatas, conversao de tempo de jogo (MM:SS para minutos decimais), tratamento de nulos com mediana e garantia de tipos corretos. Saida salva em UTF-8-BOM para compatibilidade com Excel e Power BI.

**2. Verificacao (`verification.py`)**
Inspecao rapida do shape e das primeiras linhas do CSV gerado.

**3. Importacao (`import_postgres.py`)**
Carga do CSV limpo para uma tabela `denver_nuggets` no PostgreSQL via SQLAlchemy. A tabela e substituida a cada execucao (`if_exists="replace"`).

**4. Queries SQL (`queries.sql`)**
13 queries analiticas cobrindo todas as hipoteses, com agrupamentos por resultado, tipo de temporada e local de jogo. Inclui ajuste de tipos das colunas para NUMERIC e INT conforme necessidade de precisao.

**5. Exportacao Python (`queries_python.py`)**
Executa todas as queries no Postgres, salva cada resultado como CSV individual e consolida tudo em um unico arquivo Excel com abas separadas por analise.

**6. Analise Exploratoria (`analytical_script.py`)**
Gera visualizacoes estatisticas com matplotlib e seaborn, incluindo comparativos de metricas por resultado, distribuicoes, e o grafico de Game Score do Jokic — que evidencia que sua performance individual se mantem estavel independentemente do resultado do jogo.

**7. Dashboard (`DASHBOARD.pbix`)**
Painel interativo no Power BI com o tema visual oficial dos Nuggets (dourado #FFC72C e azul #1D428A sobre fundo escuro), conectado ao dataset limpo.

---

## Conclusao

A analise cobre 13 hipoteses e produz um retrato detalhado de como o Denver Nuggets ganha e perde. Os achados sao apresentados abaixo organizados por tema.

### Falha ofensiva ou defensiva?

A queda defensiva e a principal causa das derrotas. O DRtg sobe significativamente nos jogos perdidos, enquanto o ORtg cai em menor magnitude. O net rating — diferenca entre ataque e defesa — e o indicador que melhor separa os dois resultados. Quando o Denver perde, o problema nao e marcar pontos: e impedir o adversario de marcar.

### Pontuacao e eficiencia coletiva

Em vitorias, o time marca mais pontos e sofre menos, com diferencas de placar expressivas. Mais relevante do que o volume de pontos e o eFG% ofensivo: em derrotas, a eficiencia de arremesso cai de forma consistente, indicando que o time errou mais tentativas ou dependeu menos de arremessos de alto valor. A taxa de tentativas de tres pontos (3PAr) tambem e maior nas vitorias, sugerindo que o Denver vence quando consegue impor seu estilo de jogo com mais volume de longa distancia.

### Turnovers coletivos

O TOV% ofensivo e relevante, mas nao e o fator dominante. Em derrotas, a taxa de turnovers sobe, porem a amplitude da variacao e menor do que a observada nas metricas defensivas. O impacto dos turnovers nas derrotas e real, mas secundario em relacao ao colapso defensivo.

### Casa e fora

O Denver tem desempenho superior em casa, com win rate e metricas ofensivas e defensivas melhores. Jogando fora, o DRtg piora sensivelmente, o que reforça que a defesa e o lado mais sensivel ao contexto do jogo. O ORtg tambem cai fora de casa, mas em proporcao menor.

### Nikola Jokic: carga e eficiencia

O dado mais contraintuitivo da analise esta no Game Score do Jokic: ele performa de forma muito parecida em vitorias e em derrotas. Seus pontos, assistencias e rebotes por jogo sao proximos nos dois cenarios, e seu eFG% e FG% nao apresentam quedas expressivas nas derrotas. Isso indica que Jokic nao e o problema nas derrotas — e tambem que o time nao consegue converter o desempenho dele em resultado coletivo quando os outros jogadores nao entregam.

O USG% calculado mostra que Jokic assume carga ligeiramente maior em derrotas (mais tentativas e maior participacao nas posses), o que e consistente com o papel de carregador que assume quando o time nao flui — sem que isso se traduza em vitorias.

### Assistencias e triple-doubles

Jogos com maior volume de assistencias do Jokic estao associados a maior taxa de vitorias. A faixa acima de 11 assistencias concentra os melhores resultados, indicando que quando Jokic distribui bem, o time como um todo arremessa melhor — o que reforca a leitura de que o problema nas derrotas e o time ao redor dele, nao o proprio Jokic.

Triple-doubles tambem estao positivamente associados a vitorias. A taxa de vitoria em jogos com triple-double e consideravelmente superior a media geral, ainda que o numero absoluto de ocorrencias limite conclusoes mais definitivas.

### Turnovers do Jokic

Os turnovers individuais do Jokic nao sao determinantes. A diferenca na media de turnovers entre vitorias e derrotas e pequena e pouco consistente — o que rejeita a hipotese de que os erros dele sao decisivos para o resultado. Os turnovers coletivos importam mais do que os dele individualmente.

### Playoffs vs Temporada Regular

Nos playoffs, Jokic eleva seu nivel: pontos, assistencias e plus/minus aumentam. O ORtg do time tambem melhora. Porem, o DRtg piora em relacao a temporada regular — adversarios mais qualificados exploram as fragilidades defensivas coletivas com mais eficiencia. O resultado e que a vantagem competitiva do Denver nos playoffs depende ainda mais da genialidade individual de Jokic, ja que a defesa coletiva se torna o gargalo principal.

### Sintese

O Denver Nuggets ganha quando defende bem e quando o coletivo arremessa com eficiencia, especialmente de tres pontos. Jokic e consistente independentemente do resultado — o que torna o time vulneravel sempre que os outros jogadores nao aparecem. A principal alavanca de melhoria identificada pelos dados esta na defesa coletiva, seguida pela reducao de turnovers ofensivos e pelo aumento da eficiencia de arremesso dos jogadores complementares.

---

## Como Executar

### Requisitos

```bash
pip install -r requeriments.txt
pip install sqlalchemy psycopg2
```

### Passo a Passo

```bash
# 1. Limpar o CSV bruto
python cleaning.py --input denver_nuggets_analysis.csv --output denver_nuggets_clean.csv

# 2. Verificar o resultado
python verification.py --input denver_nuggets_clean.csv

# 3. Importar para o PostgreSQL
#    Edite a senha e o caminho do arquivo em import_postgres.py antes de executar
python import_postgres.py

# 4. Executar as queries e exportar resultados
python queries_python.py --password SUA_SENHA --output ./resultados

# 5. Gerar os graficos analiticos
python analytical_script.py --input denver_nuggets_clean.csv --output ./reports
```

### Banco de Dados

O projeto utiliza **PostgreSQL** com banco nomeado `DenverNuggets` e usuario `postgres` na porta `5432`. Certifique-se de que o banco exista antes de rodar `import_postgres.py`.

### Power BI

Abra `DASHBOARD.pbix` no Power BI Desktop. Para aplicar o tema visual, acesse **Exibicao > Temas > Procurar temas** e selecione `denver_nuggets_theme.json`.

---

## Dependencias

| Biblioteca   | Versao Minima | Uso                                  |
|--------------|---------------|--------------------------------------|
| pandas       | 2.0           | Manipulacao de dados                 |
| numpy        | 1.24          | Calculos numericos                   |
| matplotlib   | 3.7           | Visualizacoes                        |
| seaborn      | 0.12          | Graficos estatisticos                |
| scipy        | 1.10          | Testes estatisticos                  |
| sqlalchemy   | —             | Conexao com PostgreSQL               |
| psycopg2     | —             | Driver PostgreSQL                    |
| openpyxl     | —             | Exportacao Excel via pandas          |
