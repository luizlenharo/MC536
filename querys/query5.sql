-- Quantidade de árvore plantadas por hectar nescessária para anular a emissão de gases do Efeito Estufa

WITH EM_EF_ESTUFA AS (
	-- Quantidade emitida de gases causadores do efeito estufa (GEE) em determinado ano
	SELECT
		ANO_EM AS ANO,
		NOME_GAS, 
		SUM (QTD_EM) AS QTD_EM
	FROM EMISSAO e
		JOIN GAS g
			ON e.EM_COD_GAS = g.COD_GAS
	WHERE NOME_GAS = 'CO2e' AND ANO_EM = '2023-01-01'
	GROUP BY (ANO, NOME_GAS)
), AREA AS (
	-- Área total do país em hectares
	SELECT 
		SUM (AREA_TOTAL) :: real AS AREA_TOTAL
	FROM MUNICIPIO
), EM_AREA AS (
	-- Emissão de GEE por hectar
	SELECT
		e.ANO,
		ROUND((e.QTD_EM / a.AREA_TOTAL) :: numeric, 2) AS TON_GEE_POR_HEC
	FROM AREA a, EM_EF_ESTUFA e 
)
-- Quantidade de árvores para anular a emissão de GEE, usando uma média de 7.14 árvores por tonelada de GEE
SELECT 
	ea.*,
	ROUND((ea.TON_GEE_POR_HEC * 7.14) :: numeric, 2) AS ARVORES_EQUIVAL
FROM EM_AREA ea