import psycopg2 as sql

def query1(cursor):
    """Porcentagem da emissão da agropecuária sobre emissão total em um estado em determinado ano"""

    cursor.execute("""SELECT
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
)""")

    return cursor.fetchall()

def query2(cursor):
    """Evolução da (emissão agropecuária/área rural) e (emissão indústria/área urbana) ao longo dos anos"""

    cursor.execute("""WITH EMISSAO_SETOR AS (
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
    WHERE (SETOR_ORIGEM = 'Processos Industriais' OR SETOR_ORIGEM = 'Agropecuária')
    GROUP BY (ANO, SETOR)
    ORDER BY (SETOR)
), AREA AS (
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
), EM_PARCIAL AS (
    SELECT 
        e.ANO,
        SUM(CASE 
                WHEN e.SETOR = 'Agropecuária' THEN e.EMISSAO / a.AREA_RURAL 
                ELSE 0 
            END) AS EMISSAO_POR_AREA_RURAL,
        SUM(CASE 
                WHEN e.SETOR = 'Processos Industriais' THEN e.EMISSAO / a.AREA_URBANA 
                ELSE 0 
            END) AS EMISSAO_POR_AREA_URBANA
    FROM 
        EMISSAO_SETOR e
    CROSS JOIN 
        AREA a
    GROUP BY e.ANO
    ORDER BY e.ANO
)
SELECT 
    ep.*,
    (ep.EMISSAO_POR_AREA_URBANA / ep.EMISSAO_POR_AREA_RURAL) AS PROPORCAO_URB_RUR
FROM EM_PARCIAL ep""")

    return cursor.fetchall()

def query3(cursor):
    """Aumento da emissão de gases em São Paulo e nos outros estados no período de 1970 - 2023 e comparação entre aumento de SP e média dos outros estados
[aumento relativo mostra a intensidade do crescimento de São Paulo em relação ao resto do Brasil]"""

    cursor.execute("""WITH EMISSAO AS (
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
    WHERE (ANO_EM = '2023-01-01' OR ANO_EM = '1970-01-01')
    GROUP BY (ANO)
), AUMENTO AS (
    -- Aumento da emissão de gases em São Paulo e em outros estados no período de 1970 - 2023
    SELECT
        (
        SELECT 
            EMISSAO_SAO_PAULO
        FROM EMISSAO
        WHERE ANO = '2023-01-01')/(
        SELECT 
            EMISSAO_SAO_PAULO
        FROM EMISSAO
        WHERE ANO = '1970-01-01'
        ) AS AUMENTO_SP,
        (
        SELECT 
        EMISSAO_MEDIA_GERAL
        FROM EMISSAO
        WHERE ANO = '2023-01-01')/(
        SELECT 
            EMISSAO_MEDIA_GERAL
        FROM EMISSAO
        WHERE ANO = '1970-01-01'
        ) AS AUMENTO_MEDIO
)
-- Comparação entre aumento de SP e média dos outros estados
SELECT 
    AUMENTO.*,
    (AUMENTO_SP/AUMENTO_MEDIO) AS AUMENTO_RELATIVO
FROM AUMENTO""")

    return cursor.fetchall()

def query4(cursor):
    """Porcentagem de emissao dos top 5 produtos mais emissores na agropecuária"""

    cursor.execute("""WITH EM_PRODUTO AS (
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
LIMIT 5""")

    return cursor.fetchall()

def query5(cursor):
    """Top 10 anos com maior balanço qtd_em + qtd_rem no século 21"""

    cursor.execute("""WITH EM_GEE AS (
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
LIMIT 10""")

    return cursor.fetchall()

def main():

    # conexão com o banco de dados
    connection = sql.connect(
        dbname="",
        user="",
        password="",
        host="",
        port=""
    )
    cursor = connection.cursor()

    print("\n========================== Query1 ==========================\n")
    print(query1(cursor))
    print("\n========================== Query2 ==========================\n")
    print(query2(cursor))
    print("\n========================== Query3 =========================\n")
    print(query3(cursor))
    print("\n========================== Query4 ==========================\n")
    print(query4(cursor))
    print("\n========================== Query5 ==========================\n")
    print(query5(cursor))

    connection.commit()
    cursor.close()
    connection.close()

    return

main()