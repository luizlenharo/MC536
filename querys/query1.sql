 Porcentagem da emissão de área explorável sobre emissão 
 total em um estado em determinado ano


SELECT
    (SUM(CASE WHEN a.TIPO_AREA = 'RURAL' THEN e.QTD_EM ELSE 0 END) * 100.0) / 
    NULLIF(SUM(e.QTD_EM), 0) AS porcentagem_exploravel
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
    uf.NOME_UF = 'DISTRITO FEDERAL' AND
    e.ANO_EM = '2020-01-01';