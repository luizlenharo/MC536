--  Evolução da (emissão agropecuária/área rural) e (emissão indústria/área urbana) ao longo dos anos

WITH EMISSAO_SETOR AS (
    -- Emissão de origem industrial e agropecuária
    SELECT
        CAST(EXTRACT(YEAR FROM e.ANO_EM) AS INTEGER) AS ANO,
        SETOR_ORIGEM AS SETOR,
        SUM (QTD_EM) AS EMISSAO
    FROM EMISSAO e
        JOIN ORIGEM o
            ON e.EM_COD_ORIGEM = o.COD_ORIGEM
        JOIN LOCALIZACAO l
            ON e.EM_COD_LOC = l.COD_LOC
    WHERE (SETOR_ORIGEM = 'Processos Industriais' OR SETOR_ORIGEM = 'Agropecuária')
    GROUP BY (ANO, SETOR)
    ORDER BY (SETOR)
), AREA AS (
    -- Área rural e urbana do país
    SELECT 
        SUM (TAM_AREA) AS AREA_RURAL,
        SUM (AREA_TOTAL) - SUM (TAM_AREA) AS AREA_URBANA
    FROM MUNICIPIO mu
        JOIN AREA a
            ON a.AREA_COD_MU = mu.COD_MU
        JOIN MICRORREGIAO mi
            ON mu.MU_COD_MI = mi.COD_MI
        JOIN ESTADO uf
            ON mi.MI_COD_UF = uf.COD_UF
    WHERE a.TIPO_AREA = 'RURAL'
), EM_PARCIAL AS (
    SELECT 
        e.ANO,
        SUM(CASE 
                WHEN e.SETOR = 'Agropecuária' THEN e.EMISSAO / a.AREA_RURAL 
                ELSE 0 
            END) AS EMISSAO_POR_AREA_RURAL,
        SUM(CASE 
                WHEN e.SETOR = 'Processos Industriais' THEN e.EMISSAO / a.AREA_URBANA 
                ELSE 0 
            END) AS EMISSAO_POR_AREA_URBANA,
        SUM(CASE 
                WHEN e.SETOR = 'Processos Industriais' THEN e.EMISSAO / a.AREA_URBANA 
                ELSE 0 
            END) /
        NULLIF(SUM(CASE 
                WHEN e.SETOR = 'Agropecuária' THEN e.EMISSAO / a.AREA_RURAL 
                ELSE 0 
            END), 0) AS PROPORCAO_URB_RUR
    FROM 
        EMISSAO_SETOR e
    CROSS JOIN 
        AREA a
    GROUP BY e.ANO
    ORDER BY e.ANO
)
SELECT * FROM EM_PARCIAL