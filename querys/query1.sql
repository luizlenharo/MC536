--Porcentagem da emissão da agropecuária sobre emissão total em um estado em determinado ano

SELECT
	CAST(EXTRACT(YEAR FROM e.ANO_EM) AS INTEGER) AS ANO,
	uf.NOME_UF AS ESTADO,	
	SUM(e.QTD_EM) AS EMITIDO_AGRO,
	(
		SUM(e.QTD_EM) * 100.0 /
		(
			SELECT SUM(e2.QTD_EM)
			FROM EMISSAO e2
				JOIN LOCALIZACAO l2 ON e2.EM_COD_LOC = l2.COD_LOC
				JOIN ESTADO uf2 ON l2.LOC_COD_UF = uf2.COD_UF
			WHERE 
				uf2.NOME_UF = %s AND
				e2.ANO_EM BETWEEN %s AND %s
		)
	) AS porcentagem_sobre_total
    FROM EMISSAO e
        JOIN ORIGEM o ON e.EM_COD_ORIGEM = o.COD_ORIGEM
        JOIN LOCALIZACAO l ON e.EM_COD_LOC = l.COD_LOC
        JOIN ESTADO uf ON l.LOC_COD_UF = uf.COD_UF
    WHERE
        uf.NOME_UF = %s AND
        e.ANO_EM BETWEEN %s AND %s AND
        o.SETOR_ORIGEM = 'Agropecuária'
    GROUP BY
        EXTRACT(YEAR FROM e.ANO_EM), uf.NOME_UF

-- A ordem associada aos valores %s é: (estado, data_i, data_f, estado, data_i, data_f)
	-- estado e ano são valores passados como parâmetros na função 
	-- Datas de início e fim do ano passado como parâmetro: 
		--data_i = f"{ano}-01-01"
		--data_f = f"{ano}-12-31"
	