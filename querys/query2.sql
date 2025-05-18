--  Evolução da (emissão agropecuária/ área rural) e (emissão indústria/ área urbana) em determinados anos

WITH EMISSAO_SETOR AS (
	-- Emissão de origem industrial e agropecuária
	SELECT
		ANO_EM AS ANO,
		SETOR_ORIGEM AS SETOR,
		SUM (QTD_EM) AS EMISSAO
	FROM EMISSAO e
		JOIN ORIGEM o
			ON e.EM_COD_ORIGEM = o.COD_ORIGEM
		JOIN LOCALIZACAO l
			ON e.EM_COD_LOC = l.COD_LOC
	WHERE (SETOR_ORIGEM = 'Processos Industriais' OR SETOR_ORIGEM = 'Agropecuária') AND (ANO_EM = '2020-01-01' OR ANO_EM = '1970-01-01')
	GROUP BY (ANO, SETOR)
),
AREA AS (
	-- Área rural e urbana do país
	SELECT 
		SUM (TAM_AREA) AS AREA_RURAL,
		SUM (AREA_TOTAL) - SUM (TAM_AREA) AS AREA_URBANA
	FROM MUNICIPIO mu
		JOIN AREA a
			ON a.AREA_COD_MU = mu.COD_MU
		JOIN MICRORREGIAO mi
			ON mu.MU_COD_MI = mi.COD_MI
		JOIN ESTADO uf
			ON mi.MI_COD_UF = uf.COD_UF
	WHERE a.TIPO_AREA = 'RURAL'
)

SELECT 
	e.ANO,
	SUM(CASE 
			WHEN e.SETOR = 'Agropecuária' THEN e.EMISSAO / a.AREA_RURAL 
			ELSE 0 
		END) AS emissao_por_area_rural,
	SUM(CASE 
			WHEN e.SETOR = 'Processos Industriais' THEN e.EMISSAO / a.AREA_URBANA 
			ELSE 0 
		END) AS emissao_por_area_urbana
FROM 
	EMISSAO_SETOR e
CROSS JOIN 
	AREA a
GROUP BY e.ANO
ORDER BY e.ANO

-- Resultados:
--"ano"	        "emissao_por_area_rural"	"emissao_por_area_urbana"
--"1970-01-01"	0.5757051627545174	        1.905508662471919
--"2020-01-01"	0.8566739058197737	        10.491481993668481