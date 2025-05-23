-- Aumento da emissão de gases em São Paulo e em outros estados no período de 1970 - 2020 e comparação entre aumento de SP e média dos outros estados

WITH EMISSAO AS (
	-- Emissão de São Paulo e emissão média dos outros estados em determinados anos
	SELECT
		ANO_EM AS ANO,
		SUM (CASE WHEN uf.NOME_UF = 'SÃO PAULO' THEN QTD_EM ELSE 0 END) AS EMISSAO_SAO_PAULO,
		SUM (CASE WHEN UF.NOME_UF <> 'SÃO PAULO' THEN QTD_EM ELSE 0 END)/26 :: real AS EMISSAO_MEDIA_GERAL
	FROM EMISSAO e
		JOIN LOCALIZACAO l
			ON e.EM_COD_LOC = l.COD_LOC
		JOIN ESTADO uf
			ON l.LOC_COD_UF = uf.COD_UF
	WHERE (ANO_EM = '2020-01-01' OR ANO_EM = '1970-01-01')
	GROUP BY (ANO)
), AUMENTO AS (
	-- Aumento da emissão de gases em São Paulo e em outros estados no período de 1970 - 2020
	SELECT
		(
		SELECT 
			EMISSAO_SAO_PAULO
		FROM EMISSAO
		WHERE ANO = '2020-01-01')/(
		SELECT 
			EMISSAO_SAO_PAULO
		FROM EMISSAO
		WHERE ANO = '1970-01-01'
		) AS AUMENTO_SP,
		(
		SELECT 
		EMISSAO_MEDIA_GERAL
		FROM EMISSAO
		WHERE ANO = '2020-01-01')/(
		SELECT 
			EMISSAO_MEDIA_GERAL
		FROM EMISSAO
		WHERE ANO = '1970-01-01'
		) AS AUMENTO_MEDIO
)
-- Comparação entre aumento de SP e média dos outros estados
SELECT 
	AUMENTO.*,
	(AUMENTO_SP/AUMENTO_MEDIO) AS AUMENTO_RELACIONAL
FROM AUMENTO