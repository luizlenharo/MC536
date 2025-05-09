 Porcentagem da emissão de área explorável sobre emissão 
 total em um estado em determinado ano


SELECT
    (SUM(CASE WHEN a.Tipo = 'EXP' THEN e.Qtd_Emitida ELSE 0 END) * 100.0) / 
    NULLIF(SUM(e.Qtd_Emitida), 0) AS porcentagem_exploravel
FROM
    Emissao e
JOIN
    Localizacao l ON e.Localizacao_id = l.id
JOIN
    Estado est ON l.Estado_id = est.id
JOIN
    Municipio m ON l.Municipio_id = m.id
JOIN
    Area a ON m.id = a.Municipio_id
WHERE
    est.Nome = 'NomeDoEstadoDesejado' AND
    e.Ano = 2023;
