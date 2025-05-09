import psycopg2 as sql
import pandas as pd

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

    # filtragem dos dados e população do banco de dados
    embrapa_dataset = pd.read_csv("./dataset/cidadesPreserv.csv")

    regiao = embrapa_dataset['nm_regiao'].drop_duplicates()
    regiao = list(zip([5, 3, 2, 4, 1], list(map(lambda x: x.upper(), regiao))))

    cursor.executemany("INSERT INTO regiao (cod_reg, nome_reg)"
                       "VALUES (%s, %s)", regiao)

    bioma = embrapa_dataset['mu_bio'].drop_duplicates()
    bioma = list(zip(range(1, 7), list(map(lambda x: x.upper(), bioma))))
    bioma_dict = {nome: cod for cod, nome in bioma}
    bioma_dict["NA"] = 0

    cursor.executemany("INSERT INTO bioma (cod_bio, nome_bio)"
                       "VALUES (%s, %s)", bioma)

    estado = embrapa_dataset[['nm_estado_', 'sigla', 'cd_geocuf_']].drop_duplicates()
    estado = list(zip(estado['nm_estado_'], estado['sigla'], estado['cd_geocuf_'], list(map(lambda x: int(str(x)[0]), estado['cd_geocuf_']))))
    estado_dict = {nome: cod for nome, _, cod, _ in estado}
    estado_dict["NÃO ALOCADO"] = 0

    cursor.executemany("INSERT INTO estado (nome_uf, uf, cod_uf, uf_cod_reg)"
                       "VALUES (%s, %s, %s, %s)", estado)

    microrregiao = embrapa_dataset[['cd_geocmi', 'nm_micro']].drop_duplicates()
    microrregiao = list(zip(microrregiao['cd_geocmi'], microrregiao['nm_micro'], list(map(lambda x: int(str(x)[:2]), microrregiao['cd_geocmi']))))

    cursor.executemany("INSERT INTO microrregiao (cod_mi, nome_mi, mi_cod_uf)"
                       "VALUES (%s, %s, %s)", microrregiao)

    bioma_micro = embrapa_dataset[['cd_geocmi', 'mi_bio']].drop_duplicates()
    bioma_micro = list(zip(bioma_micro['cd_geocmi'], list(map(lambda x: bioma_dict[x.upper()], bioma_micro['mi_bio']))))

    cursor.executemany("INSERT INTO microrregiao_bioma (cod_mi, cod_bio)"
                       "VALUES (%s, %s)", bioma_micro)
   
    municipio = embrapa_dataset[['cd_mun', 'nm_municip', 'munic_ha', 'n_imrur', 'mu_bio', 'cd_geocmi']]
    municipio['munic_ha'] = list(map(lambda x: float(x)/1000000, municipio['munic_ha']))
    municipio = list(zip(municipio['cd_mun'], municipio['nm_municip'], municipio['munic_ha'], municipio['n_imrur'], municipio['cd_geocmi'], list(map(lambda x: bioma_dict[x.upper()], municipio['mu_bio']))))

    cursor.executemany("INSERT INTO municipio (cod_mu, nome_mu, area_total, num_imoveis, mu_cod_mi, mu_cod_bio)"
                       "VALUES (%s, %s, %s, %s, %s, %s)", municipio)

    area_rural = embrapa_dataset[['cd_mun', 'imrur_ha']]
    area_rural = list(zip(
        list(map(lambda x: int(str(x) + "1"), area_rural['cd_mun'])),
        list(map(lambda _: 'RURAL', area_rural['imrur_ha'])),
        list(map(lambda x: float(x)/1000000, area_rural['imrur_ha'])),
        area_rural['cd_mun']))

    cursor.executemany("INSERT INTO area (cod_area, tipo_area, tam_area, area_cod_mu)"
                       "VALUES (%s, %s, %s, %s)", area_rural)

    area_protegida = embrapa_dataset[['cd_mun', 'uctia_ha']]
    area_protegida = list(zip(
        list(map(lambda x: int(str(x) + "2"), area_protegida['cd_mun'])),
        list(map(lambda _: 'PROT', area_protegida['uctia_ha'])),
        list(map(lambda x: float(x)/1000000, area_protegida['uctia_ha'])),
        area_protegida['cd_mun']))

    cursor.executemany("INSERT INTO area (cod_area, tipo_area, tam_area, area_cod_mu)"
                       "VALUES (%s, %s, %s, %s)", area_protegida)

    area_preservada = embrapa_dataset[['cd_mun', 'adpv_ha']]
    area_preservada = list(zip(
        list(map(lambda x: int(str(x) + "3"), area_preservada['cd_mun'])),
        list(map(lambda _: 'PRESERV', area_preservada['adpv_ha'])),
        list(map(lambda x: float(x)/1000000, area_preservada['adpv_ha'])),
        area_preservada['cd_mun']))
   
    cursor.executemany("INSERT INTO area (cod_area, tipo_area, tam_area, area_cod_mu)"
                       "VALUES (%s, %s, %s, %s)", area_preservada)

    area_ProPre = embrapa_dataset[['cd_mun', 'propre_ha']]
    area_ProPre = list(zip(
        list(map(lambda x: int(str(x) + "4"), area_ProPre['cd_mun'])),
        list(map(lambda _: 'PROPRE', area_ProPre['propre_ha'])),
        list(map(lambda x: float(x)/1000000, area_ProPre['propre_ha'])),
        area_ProPre['cd_mun']))

    cursor.executemany("INSERT INTO area (cod_area, tipo_area, tam_area, area_cod_mu)"
                       "VALUES (%s, %s, %s, %s)", area_ProPre)

    area_exploravel = embrapa_dataset[['cd_mun', 'im_di_ha']]
    area_exploravel = list(zip(
        list(map(lambda x: int(str(x) + "5"), area_exploravel['cd_mun'])),
        list(map(lambda _: 'EXP', area_exploravel['im_di_ha'])),
        list(map(lambda x: float(x)/1000000, area_exploravel['im_di_ha'])),
        area_exploravel['cd_mun']))

    cursor.executemany("INSERT INTO area (cod_area, tipo_area, tam_area, area_cod_mu)"
                       "VALUES (%s, %s, %s, %s)", area_exploravel)
   

    seeg_entidades_dataset = pd.read_csv("./dataset/gasesEE-entidades.csv", keep_default_na=False)

    origem = seeg_entidades_dataset[['Emissão/Remoção/Bunker', 'Setor de emissão',  'Categoria emissora', 'Sub-categoria emissora']].drop_duplicates()  
    origem = list(zip(range(113), origem['Emissão/Remoção/Bunker'], origem['Setor de emissão'], origem['Categoria emissora'], origem['Sub-categoria emissora']))
    origem_dict = {(tipo, setor, cat, subcat): cod for cod, tipo, setor, cat, subcat in origem}

    cursor.executemany("INSERT INTO origem (cod_origem, tipo_origem, setor_origem, categoria_origem, subcategoria_origem)"
                       "VALUES (%s, %s, %s, %s, %s)", origem)

    produto = seeg_entidades_dataset[['Produto ou sistema', 'Detalhamento',  'Recorte', 'Atividade geral']].drop_duplicates()
    produto = list(zip(range(1467), produto['Produto ou sistema'], produto['Detalhamento'], produto['Recorte'], produto['Atividade geral']))
    produto_dict = {(prod, det, rec, atv): cod for cod, prod, det, rec, atv in produto}

    cursor.executemany("INSERT INTO produto (cod_produto, nome_produto, detalhamento_produto, recorte_produto, atvgeral_produto)"
                       "VALUES (%s, %s, %s, %s, %s)", produto)

    gas = seeg_entidades_dataset['Gás'].drop_duplicates()
    gas = list(zip(range(26),
        list(map(lambda x: x[:4] if x[:4] == 'CO2e' else x, gas)),
        list(map(lambda x: x[5:] if x[:4] == 'CO2e' else None, gas))))
    gas_dict = {(nome + ' ' + carac if carac != None else nome): cod for cod, nome, carac in gas}

    cursor.executemany("INSERT INTO gas (cod_gas, nome_gas, caracteristica_gas)"
                       "VALUES (%s, %s, %s)", gas)

    localizacao = seeg_entidades_dataset[['Estado', 'Bioma']].drop_duplicates()
    localizacao = list(zip(list(map(lambda x, y: 10*estado_dict[x.upper()] + bioma_dict[y.upper()], localizacao['Estado'], localizacao['Bioma'])),
        list(map(lambda x: estado_dict[x.upper()] if estado_dict[x.upper()] != 0 else None, localizacao['Estado'])),
        list(map(lambda x: bioma_dict[x.upper()] if bioma_dict[x.upper()] != 0 else None, localizacao['Bioma']))))


    cursor.executemany("INSERT INTO localizacao (cod_loc, loc_cod_uf, loc_cod_bio)"
                       "VALUES (%s, %s, %s)", localizacao)


    seeg_medicoes_dataset = pd.read_csv("./dataset/gasesEE-medicoes_C1.csv", chunksize=10000, keep_default_na=False)

    i = 1

    for chunk in seeg_medicoes_dataset:
        for ano in range(1970, 2024):
            aux = chunk[['Emissão/Remoção/Bunker', 'Setor de emissão',  'Categoria emissora', 'Sub-categoria emissora',
                         'Produto ou sistema', 'Detalhamento',  'Recorte', 'Atividade geral',
                         'Gás',
                         'Estado', 'Bioma',
                         str(ano)]]
            cod_loc = list(map(lambda x, y: f'{10*estado_dict[x.upper()] + bioma_dict[y.upper()]:03d}', aux['Estado'], aux['Bioma']))
            cod_origem = list(map(lambda w, x, y, z: f'{origem_dict[(w, x, y, z)]:03d}', aux['Emissão/Remoção/Bunker'], aux['Setor de emissão'],  aux['Categoria emissora'], aux['Sub-categoria emissora']))
            cod_produto = list(map(lambda w, x, y, z: f'{produto_dict[(w, x, y, z)]:04d}', aux['Produto ou sistema'], aux['Detalhamento'], aux['Recorte'], aux['Atividade geral']))
            cod_gas = list(map(lambda x: f'{gas_dict[(x)]:02d}', aux['Gás']))
            cod_emissao = list(map(lambda w, x, y, z: f'{w}.{x}.{y}.{z}-{str(ano)}', cod_loc, cod_origem, cod_produto, cod_gas))
           
            emissao = list(zip(cod_emissao,
                [str(ano)+'-01-01'] * len(aux),
                list(map(lambda x: (float(x.replace(',', '.')) if len(x) > 0 else 0.0) if type(x) == str else x, aux[str(ano)])),
                list(map(int, cod_loc)),
                list(map(int, cod_origem)),
                list(map(int, cod_produto)),
                list(map(int, cod_gas))))

            cursor.executemany("INSERT INTO emissao (cod_em, ano_em, qtd_em, em_cod_loc, em_cod_origem, em_cod_produto, em_cod_gas)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", emissao)
           
            print(f'ano {ano}. chunk {i} inserida com sucesso')
        i += 1

    seeg_medicoes_dataset = pd.read_csv("./dataset/gasesEE-medicoes_C2.csv", chunksize=10000, keep_default_na=False)

    for chunk in seeg_medicoes_dataset:
        for ano in range(1970, 2024):
            aux = chunk[['Emissão/Remoção/Bunker', 'Setor de emissão',  'Categoria emissora', 'Sub-categoria emissora',
                         'Produto ou sistema', 'Detalhamento',  'Recorte', 'Atividade geral',
                         'Gás',
                         'Estado', 'Bioma',
                         str(ano)]]
            cod_loc = list(map(lambda x, y: f'{10*estado_dict[x.upper()] + bioma_dict[y.upper()]:03d}', aux['Estado'], aux['Bioma']))
            cod_origem = list(map(lambda w, x, y, z: f'{origem_dict[(w, x, y, z)]:03d}', aux['Emissão/Remoção/Bunker'], aux['Setor de emissão'],  aux['Categoria emissora'], aux['Sub-categoria emissora']))
            cod_produto = list(map(lambda w, x, y, z: f'{produto_dict[(w, x, y, z)]:04d}', aux['Produto ou sistema'], aux['Detalhamento'], aux['Recorte'], aux['Atividade geral']))
            cod_gas = list(map(lambda x: f'{gas_dict[(x)]:02d}', aux['Gás']))
            cod_emissao = list(map(lambda w, x, y, z: f'{w}.{x}.{y}.{z}-{str(ano)}', cod_loc, cod_origem, cod_produto, cod_gas))
           
            emissao = list(zip(cod_emissao,
                [str(ano)+'-01-01'] * len(aux),
                list(map(lambda x: (float(x.replace(',', '.')) if len(x) > 0 else 0.0) if type(x) == str else x, aux[str(ano)])),
                list(map(int, cod_loc)),
                list(map(int, cod_origem)),
                list(map(int, cod_produto)),
                list(map(int, cod_gas))))

            cursor.executemany("INSERT INTO emissao (cod_em, ano_em, qtd_em, em_cod_loc, em_cod_origem, em_cod_produto, em_cod_gas)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", emissao)
           
            print(f'ano {ano}. chunk {i} inserida com sucesso')
        i += 1
    
    seeg_medicoes_dataset = pd.read_csv("./dataset/gasesEE-medicoes_C3.csv", chunksize=10000, keep_default_na=False)

    for chunk in seeg_medicoes_dataset:
        for ano in range(1970, 2024):
            aux = chunk[['Emissão/Remoção/Bunker', 'Setor de emissão',  'Categoria emissora', 'Sub-categoria emissora',
                         'Produto ou sistema', 'Detalhamento',  'Recorte', 'Atividade geral',
                         'Gás',
                         'Estado', 'Bioma',
                         str(ano)]]
            cod_loc = list(map(lambda x, y: f'{10*estado_dict[x.upper()] + bioma_dict[y.upper()]:03d}', aux['Estado'], aux['Bioma']))
            cod_origem = list(map(lambda w, x, y, z: f'{origem_dict[(w, x, y, z)]:03d}', aux['Emissão/Remoção/Bunker'], aux['Setor de emissão'],  aux['Categoria emissora'], aux['Sub-categoria emissora']))
            cod_produto = list(map(lambda w, x, y, z: f'{produto_dict[(w, x, y, z)]:04d}', aux['Produto ou sistema'], aux['Detalhamento'], aux['Recorte'], aux['Atividade geral']))
            cod_gas = list(map(lambda x: f'{gas_dict[(x)]:02d}', aux['Gás']))
            cod_emissao = list(map(lambda w, x, y, z: f'{w}.{x}.{y}.{z}-{str(ano)}', cod_loc, cod_origem, cod_produto, cod_gas))
           
            emissao = list(zip(cod_emissao,
                [str(ano)+'-01-01'] * len(aux),
                list(map(lambda x: (float(x.replace(',', '.')) if len(x) > 0 else 0.0) if type(x) == str else x, aux[str(ano)])),
                list(map(int, cod_loc)),
                list(map(int, cod_origem)),
                list(map(int, cod_produto)),
                list(map(int, cod_gas))))

            cursor.executemany("INSERT INTO emissao (cod_em, ano_em, qtd_em, em_cod_loc, em_cod_origem, em_cod_produto, em_cod_gas)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", emissao)
           
            print(f'ano {ano}. chunk {i} inserida com sucesso')
        i += 1

    seeg_medicoes_dataset = pd.read_csv("./dataset/gasesEE-medicoes_C4.csv", chunksize=10000, keep_default_na=False)

    for chunk in seeg_medicoes_dataset:
        for ano in range(1970, 2024):
            aux = chunk[['Emissão/Remoção/Bunker', 'Setor de emissão',  'Categoria emissora', 'Sub-categoria emissora',
                         'Produto ou sistema', 'Detalhamento',  'Recorte', 'Atividade geral',
                         'Gás',
                         'Estado', 'Bioma',
                         str(ano)]]
            cod_loc = list(map(lambda x, y: f'{10*estado_dict[x.upper()] + bioma_dict[y.upper()]:03d}', aux['Estado'], aux['Bioma']))
            cod_origem = list(map(lambda w, x, y, z: f'{origem_dict[(w, x, y, z)]:03d}', aux['Emissão/Remoção/Bunker'], aux['Setor de emissão'],  aux['Categoria emissora'], aux['Sub-categoria emissora']))
            cod_produto = list(map(lambda w, x, y, z: f'{produto_dict[(w, x, y, z)]:04d}', aux['Produto ou sistema'], aux['Detalhamento'], aux['Recorte'], aux['Atividade geral']))
            cod_gas = list(map(lambda x: f'{gas_dict[(x)]:02d}', aux['Gás']))
            cod_emissao = list(map(lambda w, x, y, z: f'{w}.{x}.{y}.{z}-{str(ano)}', cod_loc, cod_origem, cod_produto, cod_gas))
           
            emissao = list(zip(cod_emissao,
                [str(ano)+'-01-01'] * len(aux),
                list(map(lambda x: (float(x.replace(',', '.')) if len(x) > 0 else 0.0) if type(x) == str else x, aux[str(ano)])),
                list(map(int, cod_loc)),
                list(map(int, cod_origem)),
                list(map(int, cod_produto)),
                list(map(int, cod_gas))))

            cursor.executemany("INSERT INTO emissao (cod_em, ano_em, qtd_em, em_cod_loc, em_cod_origem, em_cod_produto, em_cod_gas)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)", emissao)
           
            print(f'ano {ano}, chunk {i} inserida com sucesso')
        i += 1
   
    connection.commit()
    cursor.close()
    connection.close()
   
    return 0

main()