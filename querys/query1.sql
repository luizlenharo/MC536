-- Porcentagem da emissão da agropecuária sobre emissão total em um estado em determinado ano

SELECT
	ANO_EM AS ANO,
	NOME_UF AS ESTADO,	
	SUM(QTD_EM) AS EMITIDO_AGRO,
	(
        SUM(QTD_EM) * 100.0 /
        (
            SELECT SUM(e2.QTD_EM)
            FROM EMISSAO e2
				JOIN LOCALIZACAO l2
					ON e2.EM_COD_LOC = l2.COD_LOC
				JOIN ESTADO uf2
					ON l2.LOC_COD_UF = uf2.COD_UF
            WHERE 
				uf2.NOME_UF = 'MATO GROSSO' AND
				e2.ANO_EM = '2023-01-01'
        )
    ) AS porcentagem_sobre_total
FROM EMISSAO e
	JOIN ORIGEM o
		ON e.EM_COD_ORIGEM = o.COD_ORIGEM
	JOIN LOCALIZACAO l
		ON e.EM_COD_LOC = l.COD_LOC
	JOIN ESTADO uf
		ON l.LOC_COD_UF = uf.COD_UF
WHERE
	uf.NOME_UF = 'MATO GROSSO' AND
	e.ANO_EM = '2023-01-01' AND
	o.SETOR_ORIGEM = 'Agropecuária'
GROUP BY(
	ANO, ESTADO
)