-- Porcentagem de emissao dos top 5 produtos mais emissores na agropecuária

WITH EM_PRODUTO AS (
	-- Emissão por produto agropecuário em determinado ano e regiao
	SELECT
		NOME_PRODUTO AS PRODUTO,
		SUM (QTD_EM) AS QTD_EM
	FROM EMISSAO e 
		JOIN ORIGEM o
			ON e.EM_COD_ORIGEM = o.COD_ORIGEM
		JOIN PRODUTO p 
			ON e.EM_COD_PRODUTO = p.COD_PRODUTO
		JOIN LOCALIZACAO l
			ON e.EM_COD_LOC = l.COD_LOC
		JOIN ESTADO uf
			ON l.LOC_COD_UF = uf.COD_UF
		JOIN REGIAO r
			ON uf.UF_COD_REG = r.COD_REG
	WHERE (e.ANO_EM = '2005-01-01') AND (o.TIPO_ORIGEM = 'Emissão') AND (o.SETOR_ORIGEM = 'Agropecuária') AND (r.NOME_REG = 'SUDESTE')
	GROUP BY (PRODUTO)
), TOTAL AS (
    -- Quantidade total de emissão dos produtos agropecuários baseado na tabela EM_PRODUTO
	SELECT
		SUM (QTD_EM) AS TOTAL_EM
	FROM EM_PRODUTO
)
SELECT 
	PRODUTO,
	QTD_EM,
	ROUND((QTD_EM * 100 / TOTAL.TOTAL_EM) :: numeric, 2) AS PORCENTAGEM
FROM EM_PRODUTO, TOTAL
ORDER BY PORCENTAGEM DESC
LIMIT 5