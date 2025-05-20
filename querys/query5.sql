-- Top10 anos com maior indice qtd_em / qtd_rem
SELECT 
WITH EM_GEE AS (
	-- Quantidade emitida e removida de gases causadores do efeito estufa (GEE) em determinado ano
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
	WHERE NOME_GAS = 'CO2e' 
	GROUP BY (ANO, NOME_GAS)
)
-- 10 anos com maior indice qtd_em / qtd_rem
SELECT 
	e.*,
	(CASE 
		WHEN e.QTD_REM <> 0 
			THEN 
				ROUND ((e.QTD_EM / e.QTD_REM * -1) :: numeric, 2) 
		ELSE
			0
	END)
	AS COMPARACAO 
FROM EM_GEE e
ORDER BY (COMPARACAO) DESC
LIMIT 10