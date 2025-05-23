# MC536 - Projeto 1 – Banco de Dados: Análise das emissões de gases no Brasil 

## SUmário
* [Sobre o projeto](#sobre-o-projeto)
* [Modelagem do Banco de Dados](#modelagem-do-banco-de-dados)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Datasets](#datasets)
* [Consultas Geradas](#consultas-geradas)

## Sobre o projeto
Autores:
* [Luiz Felipe Lenharo](https://github.com/luizlenharo) (237896)
* [Henrique Cazarim Meirelles Alves](https://github.com/cazarimh) (244763)
* [Gustavo Marcelino Rodrigues](https://github.com/gustavomrodrigues) (238183)

<br>Esse projeto foi desenvolvido durante a disciplina MC536 - Banco de Dados: Teoria e Prática. O objetivo deste projeto consiste em realizar consultas 
à respeito dos gases emitidos no Brasil desde o ano de 1970. A partir dele, é possível concretizar análises relacionadas às emissões gasosas, com a finalidade de propor soluções para o desenvolvimento sustentável e aquecimento global.

## Modelagem do Banco de Dados
### Imagem 1: Modelo Conceitual (Diagrama MER)
![](https://github.com/luizlenharo/MC536/blob/main/models/modeloConceitual.jpg)

### Imagem 2: Modelo Relacional
![](https://github.com/luizlenharo/MC536/blob/main/models/modeloRelacional.png)

## Tecnologias utilizadas
* **Banco de dados:** `PostgreSQL`  
* **Linguagem de Programação:** `Python`  
* **Bibliotecas:** `pandas, psycopg2`  
* **Ferramentas de modelagem**: `pgAdmin4`

## Datasets
### SEEG (Sistema de Estimativas de Emissões e Remoções de Gases de Efeito Estufa)
* Os dados estão diretamente atrelados aos setores de Processos Industriais e Resíduos, Mudança de uso da Terra, Energia e Agropecuária.
* A plataforma do [`SEEG`](https://seeg.eco.br/dados/) disponibiliza dados detalhados sobre emissão por município, estado, região e setor.
* O SEEG é fundamental para o monitoramento das mudanças climáticas e construção de medidas políticas voltadas para a redução da emissão dos gases de efeito estufa (GEE).

### EMBRAPA (Empresa Brasileira de Pesquisa Agropecuária)
* Os dados estão diretamente relacionados com as áreas preservadas do Brasil, sendo elas: 
    * Propriedades Rurais
    * Unidades de Conservação
    * Terras Indígenas
    * Áreas Devolutas, Relevos e Águas Interiores.

* A [`EMBRAPA`](https://geoinfo.dados.embrapa.br/metadados/srv/por/catalog.search#/metadata/61e66efd-7757-4d78-84b9-c3047a8bbc70) realiza desenvolve pesquisas e tecnologias direcionadas à gestão sustentável de recursos naturais e o desenvolvimento sustentável.

### Pré-Processamento 
#### SEEG
1. Deixamos apenas a página da planilha de dados.
2. Selecionamos apenas as colunas referentes à origem, produto, gás e localização.
3. Salvamos a planilha resultante em [`gasesEE-entidades.csv`](https://github.com/luizlenharo/MC536/blob/main/dataset/gasesEE-entidades.csv)
4. Retornamos para a planilha original (planilha de dados).
5. Separamos a planilha de dados em 4 chunks de tamanho semelhante.
6. Salvamos cada uma das partes em [`gasesEE-medicoes_Ci.csv`](https://github.com/luizlenharo/MC536/tree/main/dataset), sendo i o número de cada chunk

#### EMBRAPA
1. Excluimos as colunas A, B, C, D, H, W, X e Y pois que possuíam informações desnecessárias para nossa utilização.
2. Salvamos a planilha resultado em [cidadesPreserv.csv](https://github.com/luizlenharo/MC536/blob/main/dataset/cidadesPreserv.csv)

#### SCRIPT
1. Utilizamos as planilhas resultantes para popular o banco

## Consultas Geradas

1. Porcentagem da emissão de área rural sobre emissão total em um estado em determinado ano.

2. Comparação entre `(emissão agropecuária/área rural)` e `(emissão indústria/área urbana)` em determinado ano ou evolução ao longo dos anos.

3. Evolução da emissão de um determinado estado em relação aos outros em um período `(A evolução do estado X foi 2 vezes maior que a evolução média dos estados)`

4. Porcentagem de emissão dos top 5 produtos mais emissores na agropecuária

5. Top 10 anos com maior indice `(qtd_em/qtd_rem)` de gases causadores do efeito estufa (GEE)

