-- WXT530 Table --

CREATE TABLE IF NOT EXISTS wxt530 (
	data timestamp NOT NULL,
	pressao_atmosferica float4 NULL, -- Pressao atmosferica medida em bar
	temperatura float4 NULL, -- Temperatura do ar em celciuls
	umidade_ar float4 NULL, -- Umidade relativa do ar (%)
	precipitacao float4 NULL, -- Precipitação (mm)
	velocidade_vento float4 NULL, -- Velocidade do vento (m/s)
	direcao_vento float4 NULL, -- Direção do vento (˚)
	bateria float4 NULL, -- Bateria equipamento (V)

	CONSTRAINT wxt530_pkey PRIMARY KEY ("data"),
	CONSTRAINT wxt530_unique UNIQUE ("data")
);
-- Column comments

COMMENT ON COLUMN wxt530.pressao_atmosferica IS 'Pressão atmosférica (bar)';
COMMENT ON COLUMN wxt530.temperatura IS 'Temperatura do ar (°C)';
COMMENT ON COLUMN wxt530.umidade_ar IS 'Umidade relativa do ar (%)';
COMMENT ON COLUMN wxt530.precipitacao IS 'Precipitação (mm)';
COMMENT ON COLUMN wxt530.velocidade_vento IS 'Velocidade do vento (m/s)';
COMMENT ON COLUMN wxt530.direcao_vento IS 'Direção do vento (˚)';
COMMENT ON COLUMN wxt530.bateria IS 'Bateria do aparelho (v)';

-- Timescale hypertable
SELECT create_hypertable('wxt530', by_range('data'), if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS ix_wxt530_time ON wxt530 (data ASC);

ALTER TABLE wxt530 SET (
  timescaledb.compress
);

SELECT add_compression_policy('wxt530', compress_after => INTERVAL '365d', if_not_exists => TRUE);

-- Linigrafos Table --

CREATE TABLE IF NOT EXISTS posicoes (
	nome bpchar(12) NOT NULL,
	latitude float4 NULL,
	longitude float4 NULL,
	sensor_mac bpchar(12) NULL,

	CONSTRAINT one_pos_mac UNIQUE (sensor_mac),
	CONSTRAINT posicoes_pk PRIMARY KEY (nome)
);


INSERT INTO posicoes (nome,latitude,longitude) VALUES
	 ('soter',-20.43788,-54.58097),
	 ('hemosul',-20.46824,-54.60931),
	 ('rq30',-20.4648,-54.59733),
	 ('segredo',-20.4349,-54.62027),
	 ('segredo2',-20.4588,-54.6219),
	 ('bandeira',-20.50256,-54.60454)
	ON CONFLICT DO NOTHING;


CREATE TABLE IF NOT EXISTS linigrafos (
	data_leitura timestamptz NOT NULL,
	mac bpchar(12) NOT NULL,
	valor_leitura float4 NOT NULL,
	sub_id_disp bpchar(12) NULL,
	canal int8 NOT NULL,

	CONSTRAINT linigrafos_pkey PRIMARY KEY (mac, data_leitura),
	FOREIGN KEY (sub_id_disp) REFERENCES posicoes(nome)
);

-- Timescale hypertable
SELECT create_hypertable('linigrafos', by_range('data_leitura'), if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS ix_linigrafos_time ON linigrafos (mac, data_leitura ASC);

ALTER TABLE linigrafos SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'mac'
);
SELECT add_compression_policy('linigrafos', compress_after => INTERVAL '365d', if_not_exists => TRUE);

-- sub_id_disp nullify

CREATE OR REPLACE FUNCTION posicao_or_null()
RETURNS  TRIGGER
LANGUAGE PLPGSQL
AS
$$
BEGIN
	IF (SELECT nome FROM posicoes WHERE posicoes.nome = NEW.sub_id_disp) IS NULL THEN
	   NEW.sub_id_disp = (SELECT nome FROM posicoes WHERE posicoes.sensor_mac = NEW.mac);
	END IF;
	RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER valid_posicao
BEFORE INSERT
ON linigrafos
FOR EACH ROW
EXECUTE FUNCTION posicao_or_null();

-- Update Log table
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE TABLE IF NOT EXISTS tables_infos (
	   table_name TEXT PRIMARY KEY,
	   last_update TIMESTAMPTZ NULL,
	   attr hstore
	   );

INSERT INTO tables_infos(table_name)
VALUES
	('linigrafos'),
	('wxt530')
ON CONFLICT DO NOTHING;

CREATE OR REPLACE FUNCTION stamp_update_log()
RETURNS  TRIGGER
LANGUAGE PLPGSQL
AS
$$
BEGIN
	UPDATE tables_infos
	SET last_update = CURRENT_TIMESTAMP
	WHERE table_name = TG_TABLE_NAME;
	RETURN NEW;
END
$$;

CREATE OR REPLACE TRIGGER linigrafos_update_log
AFTER INSERT ON linigrafos
FOR EACH STATEMENT
EXECUTE PROCEDURE stamp_update_log();


CREATE OR REPLACE TRIGGER wxt530_update_log
AFTER INSERT ON wxt530
FOR EACH STATEMENT
EXECUTE PROCEDURE stamp_update_log();
