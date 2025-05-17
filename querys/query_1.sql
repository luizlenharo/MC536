--Porcentagem da emissão de área explorável sobre emissão total em um estado em determinado ano

SELECT
	ANO_EM AS ANO,
	NOME_UF AS ESTADO,	
	TIPO_AREA,
	SUM(QTD_EM) AS EMITIDO_EXP,
	ROUND (
        SUM(QTD_EM) * 100.0 /
        (
            SELECT SUM(e2.QTD_EM)
            FROM EMISSAO e2
				JOIN LOCALIZACAO l2
					ON e2.EM_COD_LOC = l2.COD_LOC
				JOIN ESTADO uf2
					ON l2.LOC_COD_UF = uf2.COD_UF
				JOIN MICRORREGIAO mi2
					ON mi2.MI_COD_UF = uf2.COD_UF
				JOIN MUNICIPIO mu2
					ON mu2.MU_COD_MI = mi2.COD_MI
				JOIN AREA a2
					ON a2.AREA_COD_MU = mu2.COD_MU
            WHERE 
				uf2.NOME_UF = 'SÃO PAULO' AND
				e2.ANO_EM = '2020-01-01'
        )
    ) AS porcentagem_sobre_total
FROM EMISSAO e
	JOIN LOCALIZACAO l
		ON e.EM_COD_LOC = l.COD_LOC
	JOIN ESTADO uf
		ON l.LOC_COD_UF = uf.COD_UF
	JOIN MICRORREGIAO mi
		ON mi.MI_COD_UF = uf.COD_UF
	JOIN MUNICIPIO mu
		ON mu.MU_COD_MI = mi.COD_MI
	JOIN AREA a
		ON a.AREA_COD_MU = mu.COD_MU
WHERE
	uf.NOME_UF = 'SÃO PAULO' AND
	a.TIPO_AREA = 'EXP' AND
	e.ANO_EM = '2020-01-01'
GROUP BY(
	ANO, ESTADO, TIPO_AREA
)