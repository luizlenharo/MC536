-- Top 10 anos com maior balanço qtd_em + qtd_rem no século 21

WITH EM_GEE AS (
	-- Quantidade emitida e removida de gases causadores do efeito estufa (GEE) após 2000
	SELECT
		ANO_EM AS ANO,
		NOME_GAS,
		SUM (CASE WHEN TIPO_ORIGEM = 'Emissão' THEN QTD_EM ELSE 0 END) AS QTD_EM,
		SUM (CASE WHEN TIPO_ORIGEM = 'Remoção' THEN QTD_EM ELSE 0 END) AS QTD_REM
	FROM EMISSAO e
		JOIN GAS g
			ON e.EM_COD_GAS = g.COD_GAS
		JOIN ORIGEM o
			ON e.EM_COD_ORIGEM = o.COD_ORIGEM
	WHERE CARACTERISTICA_GAS LIKE '%GWP%' AND ANO_EM >= '2000-01-01'
	GROUP BY (ANO, NOME_GAS)
)
-- Filtra 10 anos com maior balanço qtd_em + qtd_rem no século atual
SELECT 
	e.*,
	(e.QTD_EM + e.QTD_REM) AS QTD_EM_LIQUIDA 
FROM EM_GEE e
ORDER BY (QTD_EM_LIQUIDA) DESC
LIMIT 10