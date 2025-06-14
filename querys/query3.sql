-- Aumento da emissão de gases em São Paulo e nos outros estados no período de 1970 - 2023 e comparação entre aumento de SP e média dos outros estados
-- [aumento relativo mostra a intensidade do crescimento de São Paulo em relação ao resto do Brasil]

WITH EMISSAO AS (
    -- Emissão de São Paulo e emissão média dos outros estados em determinados anos
    SELECT
        CAST(EXTRACT(YEAR FROM e.ANO_EM) AS INTEGER) AS ANO,
        SUM (CASE WHEN uf.NOME_UF = 'SÃO PAULO' THEN QTD_EM ELSE 0 END) AS EMISSAO_SAO_PAULO,
        SUM (CASE WHEN UF.NOME_UF <> 'SÃO PAULO' THEN QTD_EM ELSE 0 END)/26 :: real AS EMISSAO_MEDIA_GERAL
    FROM EMISSAO e
        JOIN LOCALIZACAO l
            ON e.EM_COD_LOC = l.COD_LOC
        JOIN ESTADO uf
            ON l.LOC_COD_UF = uf.COD_UF
    WHERE EXTRACT(YEAR FROM e.ANO_EM) IN (1970, 2023)
    GROUP BY (ANO)
), AUMENTO AS (
    -- Aumento da emissão de gases em São Paulo e em outros estados no período de 1970 - 2023
    SELECT
        (SELECT EMISSAO_SAO_PAULO FROM EMISSAO WHERE ANO = 2023) /
        NULLIF((SELECT EMISSAO_SAO_PAULO FROM EMISSAO WHERE ANO = 1970), 0) AS AUMENTO_SP,

        (SELECT EMISSAO_MEDIA_GERAL FROM EMISSAO WHERE ANO = 2023) /
        NULLIF((SELECT EMISSAO_MEDIA_GERAL FROM EMISSAO WHERE ANO = 1970), 0) AS AUMENTO_MEDIO
)
-- Comparação entre aumento de SP e média dos outros estados
SELECT 
    AUMENTO.*,
    (AUMENTO_SP/AUMENTO_MEDIO) AS AUMENTO_RELATIVO
FROM AUMENTO