# Strategic Performance Analysis — Denver Nuggets

## Visão Geral

Este projeto realiza uma análise estratégica do desempenho do Denver Nuggets com foco na correlação entre as métricas individuais de Nikola Jokic e os resultados coletivos da equipe. Cobre coleta, limpeza, armazenamento em banco de dados relacional, análise exploratória em Python e visualização no Power BI.

### Descoberta Central

O Denver Nuggets perde por falha coletiva, não por falha de Jokic. Essa é a conclusão de uma análise com **13 hipóteses**, cobrindo a temporada regular e os playoffs de 22-23.

O Game Score de Jokic se mantém estável independentemente do resultado — ele performa no mesmo nível em vitórias e derrotas. O que muda é o time ao redor dele: a eficiência defensiva (DRtg) cai com clareza nos jogos perdidos, o eFG% coletivo recua e o volume de turnovers ofensivos sobe. Quando Jokic distribui bem — jogos com mais de 11 assistências ou com triple-double — a taxa de vitória aumenta de forma expressiva.

Nos playoffs, o padrão se aprofunda: Jokic eleva seu nível, mas a defesa coletiva piora diante de adversários mais qualificados, tornando o time ainda mais dependente de uma performance individual de elite para vencer.

**A principal alavanca identificada pelos dados é a defesa coletiva.** O ataque tem capacidade — falta consistência defensiva e redução de erros ofensivos para converter o talento de Jokic em mais vitórias.

### Hipóteses Investigadas

| # | Hipótese | Dimensão |
|---|---|---|
| 1–3 | Eficiência defensiva (DRtg) em vitórias vs. derrotas | Defensiva |
| 4–5 | eFG% coletivo e taxa de turnovers ofensivos | Ofensiva |
| 6–7 | Game Score de Jokic por resultado | Individual |
| 8–9 | Impacto de jogos com 11+ assistências e triple-doubles | Individual |
| 10–11 | Comparativo casa/fora e temporada regular/playoffs | Segmentação |
| 12–13 | USG% de Jokic e dependência coletiva | Coletiva |

---

## Estrutura do Projeto

```plaintext
denver-nuggets-performance-analysis/
│
├── denver_nuggets_analysis.csv       # Dataset bruto original
├── denver_nuggets_clean.csv          # Dataset limpo e pronto para uso
│
├── cleaning.py                       # 1. Limpeza e padronização do CSV bruto
├── verification.py                   # 2. Verificação rápida do CSV gerado
├── import_postgres.py                # 3. Importação do CSV para PostgreSQL
├── queries.sql                       # 4. Queries analíticas em SQL puro
├── queries_python.py                 # 5. Execução das queries e exportação CSV/Excel
├── analytical_script.py              # 6. Análise exploratória e geração de gráficos
│
├── create_tables.sql                 # Estrutura das tabelas do banco de dados
├── denver_nuggets_theme.json         # Tema visual do Power BI (cores dos Nuggets)
├── DASHBOARD.pbix                    # Dashboard interativo no Power BI
│
├── run.bat                           # Atalho para rodar o analytical_script no Windows
├── requeriments.txt                  # Dependências Python
└── .env                              # Variáveis de ambiente (não versionado)
```

---

## Dados Analisados

- **Fonte:** Basketball-Reference (estatísticas por jogo)
- **Cobertura:** Temporada regular 22-23 + playoffs

| Dimensão | Variáveis |
|---|---|
| **Coletiva** | ORtg, DRtg, eFG%, 3PAr, TOV%, ORB%, pace, pontos marcados e sofridos |
| **Individual (Jokic)** | Pontos, assistências, rebotes, eFG%, FG%, 3P%, FT%, plus/minus, Game Score, minutos, turnovers, triple-doubles |
| **Segmentações** | Resultado (vitória/derrota), local (casa/fora), tipo (temporada regular/playoffs) |

---

## Pipeline Técnico

### Fluxo de Processamento

```
denver_nuggets_analysis.csv
           │
           ▼
      cleaning.py
  (limpeza + padronização)
           │
           ▼
  verification.py
  (inspeção rápida)
           │
           ▼
  import_postgres.py
  (carga no PostgreSQL)
           │
    ┌──────┴──────┐
    ▼             ▼
queries_python.py  analytical_script.py
(CSV + Excel)      (12 gráficos matplotlib)
                        │
                        ▼
                  DASHBOARD.pbix
                  (Power BI)
```

### Etapas

**1. Limpeza (`cleaning.py`)**
Padronização de nomes de colunas, remoção de duplicatas, conversão de tempo de jogo (MM:SS para minutos decimais), tratamento de nulos com mediana e garantia de tipos corretos. Saída salva em UTF-8-BOM para compatibilidade com Excel e Power BI.

**2. Verificação (`verification.py`)**
Inspeção rápida do shape e das primeiras linhas do CSV gerado.

**3. Importação (`import_postgres.py`)**
Carga do CSV limpo para a tabela `denver_nuggets` no PostgreSQL via SQLAlchemy. A tabela é substituída a cada execução com `DROP CASCADE` para lidar com views dependentes.

**4. Queries SQL (`queries.sql`)**
13 queries analíticas cobrindo todas as hipóteses, com agrupamentos por resultado, tipo de temporada e local de jogo.

**5. Exportação Python (`queries_python.py`)**
Executa todas as queries no PostgreSQL, salva cada resultado como CSV individual e consolida tudo em um único arquivo Excel com abas separadas por análise.

**6. Análise Exploratória (`analytical_script.py`)**
Gera 12 visualizações estatísticas com matplotlib, incluindo comparativos de métricas por resultado, distribuições de eFG%, boxplots de USG% e +/-, e scatter de ORtg vs DRtg.

---

## Como Executar

### Requisitos

- Python 3.9+
- PostgreSQL rodando localmente ou em nuvem

```bash
pip install -r requeriments.txt
pip install sqlalchemy psycopg2 python-dotenv
```

### 1. Configurar o banco de dados

Crie o banco `DenverNuggets` no PostgreSQL e configure o arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://postgres:SUASENHA@localhost:5432/DenverNuggets
```

### 2. Executar o pipeline

```bash
# 1. Limpar o CSV bruto
python cleaning.py --input denver_nuggets_analysis.csv

# 2. Verificar o resultado
python verification.py --input denver_nuggets_clean.csv

# 3. Importar para o PostgreSQL
python import_postgres.py

# 4. Executar as queries e exportar resultados
python queries_python.py

# 5. Gerar os gráficos analíticos
python analytical_script.py
```

### 3. Power BI

Abra `DASHBOARD.pbix` no Power BI Desktop. Para aplicar o tema visual dos Nuggets, acesse **Exibição > Temas > Procurar temas** e selecione `denver_nuggets_theme.json`.

---

## Dependências

| Biblioteca | Versão Mínima | Uso |
|---|---|---|
| `pandas` | 1.5.0 | Manipulação de dados |
| `numpy` | 1.23.0 | Cálculos numéricos |
| `matplotlib` | 3.6.0 | Visualizações |
| `seaborn` | 0.12.0 | Gráficos estatísticos |
| `scipy` | 1.9.0 | Testes estatísticos |
| `sqlalchemy` | — | Conexão com PostgreSQL |
| `psycopg2` | — | Driver PostgreSQL |
| `python-dotenv` | — | Variáveis de ambiente |
| `openpyxl` | — | Exportação Excel via pandas |

---

## Conclusão

O Denver Nuggets ganha quando defende bem e quando o coletivo arremessa com eficiência, especialmente de três pontos. Jokic é consistente independentemente do resultado — o que torna o time vulnerável sempre que os outros jogadores não aparecem. A principal alavanca de melhoria identificada pelos dados está na defesa coletiva, seguida pela redução de turnovers ofensivos e pelo aumento da eficiência de arremesso dos jogadores complementares.

---

*Dados extraídos do Basketball-Reference. Este projeto não tem vínculo com o Denver Nuggets nem com a NBA.*

---

## Responsável Técnica

Desenvolvido por: **Mayara C. Almeida** | Analista de Dados
