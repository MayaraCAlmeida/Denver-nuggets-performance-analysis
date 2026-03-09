--- TABELAS

SELECT * FROM denver_nuggets LIMIT 10;

ALTER TABLE denver_nuggets
    ALTER COLUMN ts_pct            TYPE NUMERIC(10,4) USING ts_pct::NUMERIC(10,4),
    ALTER COLUMN off_efg_pct       TYPE NUMERIC(10,4) USING off_efg_pct::NUMERIC(10,4),
    ALTER COLUMN def_efg_pct       TYPE NUMERIC(10,4) USING def_efg_pct::NUMERIC(10,4),
    ALTER COLUMN ftr               TYPE NUMERIC(10,4) USING ftr::NUMERIC(10,4),
    ALTER COLUMN "3par"            TYPE NUMERIC(10,4) USING "3par"::NUMERIC(10,4),
    ALTER COLUMN jokic_efg_pct     TYPE NUMERIC(10,4) USING jokic_efg_pct::NUMERIC(10,4),
    ALTER COLUMN jokic_fg_pct      TYPE NUMERIC(10,4) USING jokic_fg_pct::NUMERIC(10,4),
    ALTER COLUMN jokic_3p_pct      TYPE NUMERIC(10,4) USING jokic_3p_pct::NUMERIC(10,4),
    ALTER COLUMN jokic_ft_pct      TYPE NUMERIC(10,4) USING jokic_ft_pct::NUMERIC(10,4);

ALTER TABLE denver_nuggets
    ALTER COLUMN game_num          TYPE INT USING game_num::INT,
    ALTER COLUMN season_type       TYPE VARCHAR(10),
    ALTER COLUMN opponent          TYPE VARCHAR(50),
    ALTER COLUMN home_away         TYPE VARCHAR(5),
    ALTER COLUMN win               TYPE SMALLINT USING win::SMALLINT,
    ALTER COLUMN team_pts          TYPE INT USING team_pts::INT,
    ALTER COLUMN opp_pts           TYPE INT USING opp_pts::INT,
    ALTER COLUMN point_diff        TYPE INT USING point_diff::INT,
    ALTER COLUMN wins              TYPE INT USING wins::INT,
    ALTER COLUMN losses            TYPE INT USING losses::INT,
    ALTER COLUMN ortg              TYPE NUMERIC(7,2) USING ortg::NUMERIC(7,2),
    ALTER COLUMN drtg              TYPE NUMERIC(7,2) USING drtg::NUMERIC(7,2),
    ALTER COLUMN pace              TYPE NUMERIC(7,2) USING pace::NUMERIC(7,2),
    ALTER COLUMN off_tov_pct       TYPE NUMERIC(6,2) USING off_tov_pct::NUMERIC(6,2),
    ALTER COLUMN off_orb_pct       TYPE NUMERIC(6,2) USING off_orb_pct::NUMERIC(6,2),
    ALTER COLUMN def_tov_pct       TYPE NUMERIC(6,2) USING def_tov_pct::NUMERIC(6,2),
    ALTER COLUMN team_ast_pct      TYPE NUMERIC(6,2) USING team_ast_pct::NUMERIC(6,2),
    ALTER COLUMN team_trb_pct      TYPE NUMERIC(6,2) USING team_trb_pct::NUMERIC(6,2),
    ALTER COLUMN jokic_pts         TYPE NUMERIC(5,1) USING jokic_pts::NUMERIC(5,1),
    ALTER COLUMN jokic_ast         TYPE NUMERIC(5,1) USING jokic_ast::NUMERIC(5,1),
    ALTER COLUMN jokic_trb         TYPE NUMERIC(5,1) USING jokic_trb::NUMERIC(5,1),
    ALTER COLUMN jokic_tov         TYPE NUMERIC(5,1) USING jokic_tov::NUMERIC(5,1),
    ALTER COLUMN jokic_plus_minus  TYPE NUMERIC(6,1) USING jokic_plus_minus::NUMERIC(6,1),
    ALTER COLUMN jokic_fga         TYPE NUMERIC(5,1) USING jokic_fga::NUMERIC(5,1),
    ALTER COLUMN jokic_fg          TYPE NUMERIC(5,1) USING jokic_fg::NUMERIC(5,1),
    ALTER COLUMN jokic_mp          TYPE NUMERIC(5,2) USING jokic_mp::NUMERIC(5,2),
    ALTER COLUMN jokic_gmsc        TYPE NUMERIC(7,1) USING jokic_gmsc::NUMERIC(7,1),
    ALTER COLUMN jokic_stl         TYPE NUMERIC(5,1) USING jokic_stl::NUMERIC(5,1),
    ALTER COLUMN jokic_blk         TYPE NUMERIC(5,1) USING jokic_blk::NUMERIC(5,1),
    ALTER COLUMN jokic_pf          TYPE NUMERIC(5,1) USING jokic_pf::NUMERIC(5,1),
    ALTER COLUMN jokic_3p          TYPE NUMERIC(5,1) USING jokic_3p::NUMERIC(5,1),
    ALTER COLUMN jokic_3pa         TYPE NUMERIC(5,1) USING jokic_3pa::NUMERIC(5,1),
    ALTER COLUMN triple_double     TYPE SMALLINT USING triple_double::SMALLINT;

---- QUERIES ANALITICAS

-- Q1: Denver perde mais por falha OFENSIVA ou DEFENSIVA?
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(ortg), 1)         AS ortg_medio,
    ROUND(AVG(drtg), 1)         AS drtg_medio,
    ROUND(AVG(ortg - drtg), 1)  AS net_rating,
    COUNT(*)                    AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;
--- valores de ORTG e DRTG estavam fugindo do padrão
-- Deveriam ficar entre 100 e 125 e tavam dando mais de 800 --

SELECT MIN(ortg), MAX(ortg), MIN(drtg), MAX(drtg) FROM denver_nuggets;
-- outliers absurdos (1388, 1420 não fazem sentido nenhum para rating de basquete)

SELECT game_num, opponent, ortg, drtg 
FROM denver_nuggets 
WHERE ortg > 200 OR drtg > 200
ORDER BY ortg DESC;

--- O problema ficou claro — 
-- os valores corretos de ortg e drtg estão na casa de 100-125, mas a maioria foi importada sem o ponto decimal
--- virando 1009, 1216, 121.1 em vez de 100.9, 121.6, 121.1. devido o script de limpeza


-- resolvendo:
UPDATE denver_nuggets
SET 
    ortg = ortg / 10,
    drtg = drtg / 10
WHERE ortg > 200 OR drtg > 200;

--- confirmando
SELECT MIN(ortg), MAX(ortg), MIN(drtg), MAX(drtg) FROM denver_nuggets;
---------


-- Q2: Média de pontos — Vitórias vs Derrotas
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(team_pts), 1)   AS denver_pts,
    ROUND(AVG(opp_pts), 1)    AS adversario_pts,
    ROUND(AVG(point_diff), 1) AS diferenca_media,
    COUNT(*)                  AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q3: eFG% e eficiência coletiva por resultado
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(off_efg_pct), 4)  AS efg_ofensivo,
    ROUND(AVG(def_efg_pct), 4)  AS efg_defensivo,
    ROUND(AVG(off_tov_pct), 2)  AS tov_ofensivo,
    ROUND(AVG(ts_pct), 4)       AS ts_pct,
    ROUND(AVG("3par"), 4)       AS taxa_3pts_tentativas
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q4: Turnovers coletivos vs Resultado
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(off_tov_pct), 2)  AS tov_pct_medio,
    ROUND(MIN(off_tov_pct), 2)  AS tov_pct_min,
    ROUND(MAX(off_tov_pct), 2)  AS tov_pct_max,
    COUNT(*)                    AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q5: Performance — Casa vs Fora
SELECT
    home_away,
    COUNT(*)                              AS jogos,
    SUM(win)                              AS vitorias,
    COUNT(*) - SUM(win)                   AS derrotas,
    ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct,
    ROUND(AVG(team_pts), 1)               AS pts_media,
    ROUND(AVG(ortg), 1)                   AS ortg_medio,
    ROUND(AVG(drtg), 1)                   AS drtg_medio
FROM denver_nuggets
GROUP BY home_away
ORDER BY home_away;

-- Q6: Jokic — Carrega mais em derrotas?
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(jokic_pts), 1)          AS pts_medio,
    ROUND(AVG(jokic_ast), 1)          AS ast_medio,
    ROUND(AVG(jokic_trb), 1)          AS trb_medio,
    ROUND(AVG(jokic_fga), 1)          AS fga_medio,
    ROUND(AVG(jokic_plus_minus), 1)   AS plus_minus_medio,
    ROUND(AVG(jokic_gmsc), 1)         AS game_score_medio,
    COUNT(*)                          AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;


-- Q7: Eficiência do Jokic por resultado
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(jokic_efg_pct), 4)  AS efg_pct,
    ROUND(AVG(jokic_fg_pct), 4)   AS fg_pct,
    ROUND(AVG(jokic_3p_pct), 4)   AS tres_p_pct,
    ROUND(AVG(jokic_ft_pct), 4)   AS ft_pct
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q8: Assistências do Jokic por faixa × Win Rate
SELECT
    CASE
        WHEN jokic_ast BETWEEN 0 AND 6   THEN '1. Baixa (1-6)'
        WHEN jokic_ast BETWEEN 7 AND 10  THEN '2. Média (7-10)'
        WHEN jokic_ast BETWEEN 11 AND 15 THEN '3. Alta (11-15)'
        ELSE '4. Elite (15+)'
    END AS faixa_ast,
    COUNT(*)                              AS jogos,
    SUM(win)                              AS vitorias,
    ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct
FROM denver_nuggets
GROUP BY faixa_ast
ORDER BY faixa_ast;

-- Q9: TOV do Jokic vs Resultado
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(jokic_tov), 2)   AS tov_medio,
    ROUND(MIN(jokic_tov), 0)   AS tov_min,
    ROUND(MAX(jokic_tov), 0)   AS tov_max,
    COUNT(*)                   AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q10: Triplo-Duplo → Taxa de Vitória
SELECT
    CASE WHEN triple_double = 1 THEN 'Com Triplo-Duplo' ELSE 'Sem Triplo-Duplo' END AS td,
    COUNT(*)                              AS jogos,
    SUM(win)                              AS vitorias,
    ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct,
    ROUND(AVG(jokic_pts), 1)              AS pts_medio,
    ROUND(AVG(jokic_ast), 1)              AS ast_medio,
    ROUND(AVG(jokic_trb), 1)              AS trb_medio
FROM denver_nuggets
GROUP BY triple_double
ORDER BY triple_double DESC;

-- Q11: Playoffs vs Regular Season
SELECT
    season_type,
    COUNT(*)                              AS jogos,
    SUM(win)                              AS vitorias,
    ROUND(AVG(win::NUMERIC) * 100, 1)     AS win_rate_pct,
    ROUND(AVG(jokic_pts), 1)              AS jokic_pts,
    ROUND(AVG(jokic_ast), 1)              AS jokic_ast,
    ROUND(AVG(jokic_trb), 1)              AS jokic_trb,
    ROUND(AVG(jokic_plus_minus), 1)       AS plus_minus,
    ROUND(AVG(ortg), 1)                   AS ortg,
    ROUND(AVG(drtg), 1)                   AS drtg,
    ROUND(AVG(off_efg_pct), 4)            AS off_efg_pct
FROM denver_nuggets
GROUP BY season_type
ORDER BY season_type;

-- Q12: Ranking de correlação visual — top métricas por win
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(ortg), 1)                               AS ortg,
    ROUND(AVG(drtg), 1)                               AS drtg,
    ROUND(AVG(off_efg_pct), 4)                        AS off_efg_pct,
    ROUND(AVG(def_efg_pct), 4)                        AS def_efg_pct,
    ROUND(AVG("3par"), 4)                             AS taxa_3pts,
    ROUND(AVG(jokic_pts), 1)                          AS jokic_pts,
    ROUND(AVG(jokic_plus_minus), 1)                   AS jokic_pm,
    ROUND(AVG(triple_double::NUMERIC) * 100, 1)       AS pct_triplo_duplo
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

-- Q13: USG% calculado (FGA + FTA) por resultado
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    ROUND(AVG(jokic_fga), 1)                                        AS fga_medio,
    ROUND(AVG(jokic_3pa), 1)                                        AS fta_estimado,
    ROUND(AVG(jokic_fga + 0.44 * jokic_3pa + jokic_tov), 1)        AS usg_numerador,
    ROUND(AVG((jokic_fga + 0.44 * jokic_3pa + jokic_tov)
        / NULLIF(jokic_mp, 0) * 36), 2)                             AS usg_proxy,
    COUNT(*)                                                         AS jogos
FROM denver_nuggets
GROUP BY win
ORDER BY win DESC;

---- VIEW PRO POWERBI
--- VIEW 1 - Resumo por resultado
CREATE OR REPLACE VIEW vw_resultado_resumo AS
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    season_type,
    home_away,
    COUNT(*)                              AS jogos,
    ROUND(AVG(team_pts), 1)               AS pts_denver,
    ROUND(AVG(opp_pts), 1)                AS pts_adversario,
    ROUND(AVG(ortg), 1)                   AS ortg,
    ROUND(AVG(drtg), 1)                   AS drtg,
    ROUND(AVG(off_efg_pct), 4)            AS off_efg_pct,
    ROUND(AVG(off_tov_pct), 2)            AS off_tov_pct,
    ROUND(AVG("3par"), 4)                 AS taxa_3pts
FROM denver_nuggets
GROUP BY win, season_type, home_away;

--- VIEW 2 - Performance Jokic por resultado e temporada
CREATE OR REPLACE VIEW vw_jokic_performance AS
SELECT
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    season_type,
    triple_double,
    COUNT(*)                              AS jogos,
    ROUND(AVG(jokic_pts), 1)              AS pts,
    ROUND(AVG(jokic_ast), 1)              AS ast,
    ROUND(AVG(jokic_trb), 1)              AS trb,
    ROUND(AVG(jokic_tov), 1)              AS tov,
    ROUND(AVG(jokic_plus_minus), 1)       AS plus_minus,
    ROUND(AVG(jokic_efg_pct), 4)          AS efg_pct,
    ROUND(AVG(jokic_gmsc), 1)             AS game_score,
    ROUND(AVG(jokic_fga), 1)              AS fga
FROM denver_nuggets
GROUP BY win, season_type, triple_double;

---- VIEW 3 - Game-level completo para scatter
CREATE OR REPLACE VIEW vw_game_detail AS
SELECT
    game_num,
    season_type,
    opponent,
    home_away,
    win,
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    team_pts,
    opp_pts,
    point_diff,
    ortg,
    drtg,
    off_efg_pct,
    def_efg_pct,
    off_tov_pct,
    "3par"               AS taxa_3pts,
    jokic_pts,
    jokic_ast,
    jokic_trb,
    jokic_tov,
    jokic_plus_minus,
    jokic_efg_pct,
    jokic_gmsc,
    triple_double,
    ROUND(ortg - drtg, 1) AS net_rating,
    CASE
        WHEN win = 0 AND ortg < 110 AND drtg >= 110 THEN 'Falha Ofensiva'
        WHEN win = 0 AND drtg > 115 AND ortg >= 110 THEN 'Falha Defensiva'
        WHEN win = 0 THEN 'Ambas'
        ELSE '-'
    END AS causa_derrota
FROM denver_nuggets;

--- VIEW 4 - Visão por adversários
CREATE OR REPLACE VIEW vw_por_adversario AS
SELECT
    opponent,
    COUNT(*)                          AS jogos,
    SUM(win)                          AS vitorias,
    ROUND(AVG(win::NUMERIC) * 100, 1) AS win_rate_pct,
    ROUND(AVG(point_diff), 1)         AS diff_media,
    ROUND(AVG(jokic_pts), 1)          AS jokic_pts,
    ROUND(AVG(jokic_ast), 1)          AS jokic_ast
FROM denver_nuggets
GROUP BY opponent
ORDER BY win_rate_pct DESC;
-------------------------------------------------
ALTER TABLE denver_nuggets
ADD PRIMARY KEY (game_num, season_type);

-- Drop views
DROP VIEW IF EXISTS vw_game_detail;
DROP VIEW IF EXISTS vw_resultado_resumo;
DROP VIEW IF EXISTS vw_jokic_performance;
DROP VIEW IF EXISTS vw_por_adversario;

ALTER TABLE denver_nuggets
ADD PRIMARY KEY (game_num, season_type);

SELECT constraint_name, column_name
FROM information_schema.key_column_usage
WHERE table_name = 'denver_nuggets';

CREATE OR REPLACE VIEW vw_jokic_triple_double AS
SELECT
    triple_double,
    COUNT(*) AS jogos,
    ROUND(AVG(jokic_pts), 1) AS pts,
    ROUND(AVG(jokic_ast), 1) AS ast,
    ROUND(AVG(jokic_trb), 1) AS trb,
    ROUND(AVG(win::NUMERIC) * 100, 1) AS win_rate_pct
FROM denver_nuggets
GROUP BY triple_double;

SELECT MIN(jokic_efg_pct), MAX(jokic_efg_pct), AVG(jokic_efg_pct) 
FROM denver_nuggets;

UPDATE denver_nuggets
SET jokic_efg_pct = jokic_efg_pct / 10000
WHERE jokic_efg_pct > 1;

SELECT MIN(jokic_efg_pct), MAX(jokic_efg_pct), AVG(jokic_efg_pct) 
FROM denver_nuggets;

SELECT MIN(jokic_gmsc), MAX(jokic_gmsc), AVG(jokic_gmsc) 
FROM denver_nuggets;

UPDATE denver_nuggets
SET jokic_gmsc = jokic_gmsc / 10
WHERE jokic_gmsc > 50;

SELECT MIN(jokic_gmsc), MAX(jokic_gmsc), AVG(jokic_gmsc) 
FROM denver_nuggets;

SELECT causa_derrota, COUNT(*) 
FROM vw_game_detail 
WHERE win = 0
GROUP BY causa_derrota;

SELECT season_type, causa_derrota, COUNT(*) 
FROM vw_game_detail 
WHERE win = 0
GROUP BY season_type, causa_derrota;

SELECT COUNT(*) FROM vw_game_detail;

ALTER TABLE denver_nuggets ADD COLUMN id SERIAL;

DROP VIEW vw_game_detail;

CREATE OR REPLACE VIEW vw_game_detail AS
SELECT
    ROW_NUMBER() OVER (ORDER BY game_num, season_type) AS id,
    game_num,
    season_type,
    opponent,
    home_away,
    win,
    CASE WHEN win = 1 THEN 'Vitória' ELSE 'Derrota' END AS resultado,
    team_pts,
    opp_pts,
    point_diff,
    ortg,
    drtg,
    off_efg_pct,
    def_efg_pct,
    off_tov_pct,
    "3par"               AS taxa_3pts,
    jokic_pts,
    jokic_ast,
    jokic_trb,
    jokic_tov,
    jokic_plus_minus,
    jokic_efg_pct,
    jokic_gmsc,
    triple_double,
    ROUND(ortg - drtg, 1) AS net_rating,
    CASE
        WHEN win = 0 AND ortg < 110 AND drtg >= 110 THEN 'Falha Ofensiva'
        WHEN win = 0 AND drtg > 115 AND ortg >= 110 THEN 'Falha Defensiva'
        WHEN win = 0 THEN 'Ambas'
        ELSE '-'
    END AS causa_derrota
FROM denver_nuggets;

SELECT DISTINCT win, pg_typeof(win) FROM denver_nuggets;

SELECT win, COUNT(*) FROM denver_nuggets GROUP BY win;

SELECT CASE WHEN win = 1::smallint THEN 'Vitória' ELSE 'Derrota' END AS resultado
FROM denver_nuggets
LIMIT 5;

SELECT id, net_rating FROM vw_game_detail ORDER BY net_rating DESC LIMIT 10;

DROP VIEW vw_game_detail;

SELECT MIN(ortg), MAX(ortg), AVG(ortg) FROM denver_nuggets;
SELECT MIN(net_rating), MAX(net_rating), AVG(net_rating) 
FROM vw_game_detail;

UPDATE denver_nuggets
SET ortg = ortg * 10
WHERE ortg < 80;

SELECT MIN(net_rating), MAX(net_rating), AVG(net_rating) 
FROM vw_game_detail;

SELECT COUNT(*) FROM denver_nuggets WHERE drtg > 130;]

SELECT MIN(drtg), MAX(drtg), AVG(drtg) FROM denver_nuggets;

UPDATE denver_nuggets
SET drtg = drtg * 10
WHERE drtg < 80;

SELECT MIN(drtg), MAX(drtg), AVG(drtg) FROM denver_nuggets;

SELECT CASE WHEN win = 1::smallint THEN 'Vitória' ELSE 'Derrota' END AS resultado
FROM denver_nuggets
LIMIT 5;


