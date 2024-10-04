
--liquibase formatted sql

--changeset postgres:add_sommer_mmec context:template splitStatements:false rollbackSplitStatements:false
--comment: Hand hacked because I can - JDLS


-- Creates an analysis configuration record. This hangs all the other objects off its stringly typed config_code name
-- Example: SELECT * FROM add_analysis_config('config_110005.cfg','Scenario 2 - sommer mmec', 'Scenario 2 - sommer mmec','From course example', 'sommer-mmec',6);
CREATE OR REPLACE FUNCTION add_analysis_config(conf_code text, conf_name text, conf_label text, conf_description text, conf_statement text, order_number int) RETURNS VOID AS $$
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type,"statement"
	) VALUES (
		conf_code, conf_name, 
		conf_label, conf_description, 
		'catalog_item', 'character varying',conf_statement
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id,
	is_void, property_id, config_property_id, is_layout_variable
) VALUES (
	order_number, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config'), 
	(SELECT id FROM analysis_config), false
)
$$ LANGUAGE SQL;



--
-- Example: add_config_formula('config_110005.cfg',4,'formula_opt1','Pheno from loc with variety','Pheno from loc with variety', 'fixed = phenotype~loc, random = ~vsc(isc(variety),Gu=GT)')
CREATE OR REPLACE FUNCTION add_config_formula(config_link text,order_number int, formula_code text, formula_name text, label text, formula_statement text) RETURNS int
	AS $$
	WITH config_formula AS (
		INSERT INTO af.property(
			type, data_type, code, "name", "label", "statement"
		) VALUES (
			'catalog_item', 'character varying', formula_code, 
			 formula_name, 
			label, 
			formula_statement
		) RETURNING id
		),
		config_formula_property_config_link AS (
		INSERT INTO af.property_config(
			order_number, creation_timestamp, creator_id,
			is_void, property_id, config_property_id, is_layout_variable
		) VALUES (
			order_number, 'now()', '1', false,
			(SELECT id FROM af.property WHERE code='formula' LIMIT 1), 
			(SELECT id FROM config_formula), false
		)
		),
		config_formula_config_link AS (
		INSERT INTO af.property_config(
			order_number, creation_timestamp, creator_id,
			is_void, property_id, config_property_id, is_layout_variable
		) VALUES (
			order_number, 'now()', '1', false,
			(SELECT id FROM af.property WHERE code = config_link LIMIT 1),
			(SELECT id FROM config_formula), false
		)

	)
	SELECT * FROM config_formula $$
	LANGUAGE SQL;

CREATE OR REPLACE FUNCTION add_config_residual(config_link text, order_number int, res_code text, res_name text, res_label text, res_statement text) RETURNS int
	AS $$
WITH config_residual AS (
     INSERT INTO af.property(
		type, data_type, code, "name", "label", "statement"
	) VALUES (
		'catalog_item', 'character varying', res_code, 
		res_name, 
		res_label, 
		res_statement
	) RETURNING id
),
config_residual_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		order_number, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='residual' LIMIT 1), 
		(SELECT id FROM config_residual LIMIT 1), false
	)
),
config_residual_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		order_number, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = config_link LIMIT 1),
		(SELECT id FROM config_residual LIMIT 1), false
	)

)
SELECT * FROM config_residual
$$ LANGUAGE SQL;


CREATE OR REPLACE FUNCTION add_config_prediction(config_link text, order_number int, pre_code text, pre_name text,pre_statement text) RETURNS int
	AS $$
WITH config_prediction AS (
	INSERT INTO af.property(
		type, data_type, code, "name", "statement"
	) VALUES (
		'catalog_item', 'character varying', pre_code, pre_name, pre_statement
	) RETURNING id
),
config_prediction_property_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		order_number, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code='prediction' LIMIT 1) , 
		(SELECT id FROM config_prediction LIMIT 1), false
	)
),
config_prediction_config_link AS (
	INSERT INTO af.property_config(
		order_number, creation_timestamp, creator_id,
		is_void, property_id, config_property_id, is_layout_variable
	) VALUES (
		order_number, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = config_link LIMIT 1),
		(SELECT id FROM config_prediction LIMIT 1), false
	)

) SELECT * from config_prediction
$$ LANGUAGE SQL;




-- add stat factor
CREATE OR REPLACE FUNCTION add_stat_factor(config_link text, order_number int, stat_code text, stat_definition text) RETURNS int
	AS $$
WITH stat_factor AS (
	INSERT INTO af.property (code, type) VALUES  (stat_code, 'catalog_item') RETURNING id
),
stat_factor_config AS (
	INSERT INTO af.property_config (order_number, creation_timestamp, creator_id,is_void, 
		property_id, config_property_id, is_layout_variable
	) VALUES(
		order_number, 'now()', '1', false,
		(SELECT id FROM af.property WHERE code = 'analysis_module_fields' LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
), 
stat_factor_meta AS (
	INSERT INTO af.property_meta(code,value,property_id) 
	VALUES(
		'definition', stat_definition, (SELECT id FROM stat_factor LIMIT 1)
	)
),
stat_factor_config_link AS (
	INSERT INTO af.property_config (
		order_number, creation_timestamp, creator_id, is_void,property_id, 
		config_property_id, is_layout_variable
	) VALUES (
		5, 'now()', '1', false, 
		(SELECT id FROM af.property WHERE code = config_link LIMIT 1),
		(SELECT id FROM stat_factor LIMIT 1), false
	)
)
SELECT id AS stat_factor_id FROM stat_factor LIMIT 1
$$ LANGUAGE SQL;



-- BEGIN config_110005.cfg
SELECT * FROM add_analysis_config('config_110005.cfg',
'Scenario 2 - sommer mmec', 'Scenario 2 - sommer mmec',
'From course example', 'sommer-mmec',6);

-- add config_110005 meta data
-- No, I don't know why we're doing this 'select id' stuff  - JDLS
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_110005.cfg' LIMIT 1
)
INSERT INTO af.property_meta(code,value,property_id) VALUES 
	('config_version', '2', (SELECT id FROM analysis_config)),
	('date', '13-Nov-2021', (SELECT id FROM analysis_config)),
	('author', 'Josh L.S.', (SELECT id FROM analysis_config)),
	('email', 'jdl232@cornell.edu', (SELECT id FROM analysis_config)),
	('engine', 'sommer - mmec', (SELECT id FROM analysis_config)),
    ('design',  'RCBD', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    ('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    ('exp_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    ('trait_pattern', 'univariate', (SELECT id FROM analysis_config));
-- END config_110005.cfg


SELECT * FROM add_config_formula('config_110005.cfg',4,'formula_opt2',
'Trait from geno with AMat','Trait from geno with AMat', 
'fixed = {trait_name} ~ genotype, random = ~vsc(isc(sample),Gu=GT)');

SELECT * FROM add_config_formula('config_110005.cfg',2, 'formula_opt1',
'Pheno from loc with variety','Pheno from loc with variety',
'fixed = phenotype~loc, random = ~vsc(isc(variety),Gu=GT)');


SELECT * FROM add_config_residual('config_110005.cfg',1,'residual_opt1','Units','Units','~ units');


--Note: anything you predict on needs to be in the output data set, so should be a factor as well
SELECT * FROM add_config_prediction('config_110005.cfg',6,'Yield','Yield','YLDPLOT');

--Stat definition - the internal name of the 'stat'
SELECT * FROM add_stat_factor('config_110005.cfg',6,'trial','trialDbId');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'plot', 'observationUnitDbId');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'genotype','germplasmDbId');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'sample','sampleDbId'); --Adding one for sample - JDLS
SELECT * FROM add_stat_factor('config_110005.cfg',6,'rep','replicate');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'loc','locationDbId');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'col','positionCoordinateX');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'row','positionCoordinateY');
SELECT * FROM add_stat_factor('config_110005.cfg',6,'Yield','YLDPLOT');