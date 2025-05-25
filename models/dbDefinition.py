import psycopg2 as sql

# conexão com o banco de dados
connection = sql.connect(
    dbname="",
    user="",
    password="",
    host="",
    port=""
)
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS public.origem CASCADE;
DROP TABLE IF EXISTS public.produto CASCADE;
DROP TABLE IF EXISTS public.gas CASCADE;
DROP TABLE IF EXISTS public.emissao CASCADE;
DROP TABLE IF EXISTS public.localizacao CASCADE;
DROP TABLE IF EXISTS public.area CASCADE;
DROP TABLE IF EXISTS public.municipio CASCADE;
DROP TABLE IF EXISTS public.microrregiao_bioma CASCADE;
DROP TABLE IF EXISTS public.microrregiao CASCADE;
DROP TABLE IF EXISTS public.bioma CASCADE;
DROP TABLE IF EXISTS public.estado CASCADE;
DROP TABLE IF EXISTS public.regiao CASCADE;

CREATE TABLE IF NOT EXISTS public.regiao
(
    cod_reg integer NOT NULL,
    nome_reg text NOT NULL,
    PRIMARY KEY (cod_reg)
);

CREATE TABLE IF NOT EXISTS public.estado
(
    cod_uf integer NOT NULL,
    nome_uf text NOT NULL,
    uf text NOT NULL,
    uf_cod_reg integer NOT NULL,
    PRIMARY KEY (cod_uf)
);

CREATE TABLE IF NOT EXISTS public.microrregiao
(
    cod_mi integer NOT NULL,
    nome_mi text NOT NULL,
    mi_cod_uf integer NOT NULL,
    PRIMARY KEY (cod_mi)
);

CREATE TABLE IF NOT EXISTS public.municipio
(
    cod_mu integer NOT NULL,
    nome_mu text NOT NULL,
    area_total integer NOT NULL,
    num_imoveis integer NOT NULL,
    mu_cod_mi integer NOT NULL,
    mu_cod_bio integer NOT NULL,
    PRIMARY KEY (cod_mu)
);

CREATE TABLE IF NOT EXISTS public.area
(
    cod_area integer NOT NULL,
    tipo_area text NOT NULL,
    tam_area integer NOT NULL,
    area_cod_mu integer NOT NULL,
    PRIMARY KEY (cod_area)
);

CREATE TABLE IF NOT EXISTS public.bioma
(
    cod_bio integer NOT NULL,
    nome_bio text NOT NULL,
    PRIMARY KEY (cod_bio)
);

CREATE TABLE IF NOT EXISTS public.origem
(
    cod_origem integer NOT NULL,
    tipo_origem text NOT NULL,
    setor_origem text NOT NULL,
    categoria_origem text NOT NULL,
    subcategoria_origem text NOT NULL,
    PRIMARY KEY (cod_origem)
);

CREATE TABLE IF NOT EXISTS public.produto
(
    cod_produto integer NOT NULL,
    nome_produto text NOT NULL,
    detalhamento_produto text NOT NULL,
    recorte_produto text NOT NULL,
    atvgeral_produto text NOT NULL,
    PRIMARY KEY (cod_produto)
);

CREATE TABLE IF NOT EXISTS public.gas
(
    cod_gas integer NOT NULL,
    nome_gas text NOT NULL,
    caracteristica_gas text,
    PRIMARY KEY (cod_gas)
);

CREATE TABLE IF NOT EXISTS public.emissao
(
    cod_em text NOT NULL,
    ano_em date NOT NULL,
    qtd_em real NOT NULL,
    em_cod_loc integer NOT NULL,
    em_cod_origem integer NOT NULL,
    em_cod_produto integer NOT NULL,
    em_cod_gas integer NOT NULL,
    PRIMARY KEY (cod_em)
);

CREATE TABLE IF NOT EXISTS public.localizacao
(
    cod_loc integer NOT NULL,
    loc_cod_uf integer,
    loc_cod_bio integer,
    PRIMARY KEY (cod_loc)
);

CREATE TABLE IF NOT EXISTS public.microrregiao_bioma
(
    cod_mi integer NOT NULL,
    cod_bio integer NOT NULL
);

ALTER TABLE IF EXISTS public.estado
    DROP CONSTRAINT IF EXISTS uf_cod_reg;
	
ALTER TABLE IF EXISTS public.estado
    ADD CONSTRAINT uf_cod_reg FOREIGN KEY (uf_cod_reg)
    REFERENCES public.regiao (cod_reg) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.microrregiao
    DROP CONSTRAINT IF EXISTS mi_cod_uf;

ALTER TABLE IF EXISTS public.microrregiao
    ADD CONSTRAINT mi_cod_uf FOREIGN KEY (mi_cod_uf)
    REFERENCES public.estado (cod_uf) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.municipio
    DROP CONSTRAINT IF EXISTS mu_cod_mi;

ALTER TABLE IF EXISTS public.municipio
    ADD CONSTRAINT mu_cod_mi FOREIGN KEY (mu_cod_mi)
    REFERENCES public.microrregiao (cod_mi) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.municipio
    DROP CONSTRAINT IF EXISTS mu_cod_bio;

ALTER TABLE IF EXISTS public.municipio
    ADD CONSTRAINT mu_cod_bio FOREIGN KEY (mu_cod_bio)
    REFERENCES public.bioma (cod_bio) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.area
    DROP CONSTRAINT IF EXISTS area_cod_mu;

ALTER TABLE IF EXISTS public.area
    ADD CONSTRAINT area_cod_mu FOREIGN KEY (area_cod_mu)
    REFERENCES public.municipio (cod_mu) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE emissao
ALTER COLUMN cod_em TYPE TEXT;

ALTER TABLE IF EXISTS public.emissao
    DROP CONSTRAINT IF EXISTS em_cod_loc;

ALTER TABLE IF EXISTS public.emissao
    ADD CONSTRAINT em_cod_loc FOREIGN KEY (em_cod_loc)
    REFERENCES public.localizacao (cod_loc) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.emissao
    DROP CONSTRAINT IF EXISTS em_cod_origem;

ALTER TABLE IF EXISTS public.emissao
    ADD CONSTRAINT em_cod_origem FOREIGN KEY (em_cod_origem)
    REFERENCES public.origem (cod_origem) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.emissao
    DROP CONSTRAINT IF EXISTS em_cod_produto;
	
ALTER TABLE IF EXISTS public.emissao
    ADD CONSTRAINT em_cod_produto FOREIGN KEY (em_cod_produto)
    REFERENCES public.produto (cod_produto) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.emissao
    DROP CONSTRAINT IF EXISTS em_cod_gas;

ALTER TABLE IF EXISTS public.emissao
    ADD CONSTRAINT em_cod_gas FOREIGN KEY (em_cod_gas)
    REFERENCES public.gas (cod_gas) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.localizacao
    DROP CONSTRAINT IF EXISTS loc_cod_uf;

ALTER TABLE IF EXISTS public.localizacao
    ADD CONSTRAINT loc_cod_uf FOREIGN KEY (loc_cod_uf)
    REFERENCES public.estado (cod_uf) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.localizacao
    DROP CONSTRAINT IF EXISTS loc_cod_bio;

ALTER TABLE IF EXISTS public.localizacao
    ADD CONSTRAINT loc_cod_bio FOREIGN KEY (loc_cod_bio)
    REFERENCES public.bioma (cod_bio) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.microrregiao_bioma
    DROP CONSTRAINT IF EXISTS cod_mi;

ALTER TABLE IF EXISTS public.microrregiao_bioma
    ADD CONSTRAINT cod_mi FOREIGN KEY (cod_mi)
    REFERENCES public.microrregiao (cod_mi) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.microrregiao_bioma
    DROP CONSTRAINT IF EXISTS cod_bio;
	
ALTER TABLE IF EXISTS public.microrregiao_bioma
    ADD CONSTRAINT cod_bio FOREIGN KEY (cod_bio)
    REFERENCES public.bioma (cod_bio) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;""")

connection.commit()
cursor.close()
connection.close()