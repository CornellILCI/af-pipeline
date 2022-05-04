--liquibase formatted sql

--changeset postgres:add_asreml_r_analysis_configuration_data context:template splitStatements:false rollbackSplitStatements:false
--comment: BA2-44 Add analysis configuration data for Asreml-R engine 20022


-- config_20022.cfg
WITH analysis_config AS (
	INSERT INTO af.property(
		code, "name", "label", description, "type", data_type
	) VALUES (
		'config_20022.cfg', 'Multi-Exp 2-stage analysis - 1st Stage - RCBD & Aug RCBD - fix model',
		'Multi-Exp 2-stage analysis - 1st Stage - RCBD & Aug RCBD - fix model', 
		'Executes the first stage of a two stage analysis for RCBD experiments, genotype as fixed, no spatial adjustment', 
		'catalog_item', 'character varying'
	) RETURNING id
)
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id,
	is_void, property_id, config_property_id, is_layout_variable
) VALUES (
	1, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'analysis_config'), 
	(SELECT id FROM analysis_config), false
);


-- add loc as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	1, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'loc' AND data_type = 'factor'), false
);


-- add expt as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'expt' AND data_type = 'factor'), false
);

-- add germplasm as stat factor
INSERT INTO af.property_config(
	order_number, creation_timestamp, creator_id, is_void,property_id,
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'ge' AND data_type = 'factor'), false
);

-- add plot as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'plot' AND data_type = 'factor'), false
);

-- add col as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'col' AND data_type = 'factor'), false
);


-- add row as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'row' AND data_type = 'factor'), false
);

-- add rep as stat factor
INSERT INTO af.property_config (
	order_number, creation_timestamp, creator_id, is_void,property_id, 
	config_property_id, is_layout_variable
) VALUES (
	2, 'now()', '1', false, 
	(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
	(SELECT id FROM af.property WHERE code = 'rep' AND data_type = 'factor'), false
);

-- add config_20022 metadata
WITH analysis_config AS (
	SELECT id FROM af.property WHERE code = 'config_20022.cfg'
)
INSERT INTO af.property_meta(code,value,property_id) VALUES
	('config_version', '1', (SELECT id FROM analysis_config)),
	('date', '11-March-2022', (SELECT id FROM analysis_config)),
	('author', 'Pedro Barbosa', (SELECT id FROM analysis_config)),
	('email', 'p.medeiros@cgiar.org', (SELECT id FROM analysis_config)),
	('engine', 'ASREML-R', (SELECT id FROM analysis_config)),
    	('design',  'RCBD', (SELECT id FROM analysis_config)),
    	('design',  'Augmented-RCB', (SELECT id FROM analysis_config)),
	('trait_level', 'plot', (SELECT id FROM analysis_config)),
    	('analysis_objective', 'prediction', (SELECT id FROM analysis_config)),
    	('exp_analysis_pattern', 'multi', (SELECT id FROM analysis_config)),
    	('loc_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('year_analysis_pattern', 'single', (SELECT id FROM analysis_config)),
    	('trait_pattern', 'univariate', (SELECT id FROM analysis_config));


-- add formula to config_20022
DO $$
	DECLARE 
		formula_id INTEGER;
		formula_code TEXT := 'formula_opt1';
		formula_name TEXT := 'Analysis with genotype as fixed - BLUEs. RCBD';
		formula_statement TEXT := 'fixed = {trait_name} ~ rep + ge';

	BEGIN
		SELECT id FROM af.property WHERE code=formula_code
			AND name=formula_name
			AND statement=formula_statement INTO formula_id;

		IF formula_id IS NULL THEN
			WITH config_formula AS (
				INSERT INTO af.property(
					type, data_type, code, "name", "label", "statement"
				) VALUES (
					'catalog_item', 'character varying', 
					formula_code, formula_name, 
					formula_name, formula_statement
				) RETURNING id
			),
			config_formula_property_config_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code='formula'), 
					formula_id, false
				)
			),
			config_formula_config_20022_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
					formula_id, false
				)
			
			)
			SELECT * FROM config_formula;
		ELSE
			INSERT INTO af.property_config(
				order_number, creation_timestamp, creator_id,
				is_void, property_id, config_property_id, is_layout_variable
			) VALUES (
				1, 'now()', '1', false,
				(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
				formula_id, false
			);
		END IF;
	END $$	

-- add residual:Univariate homogeneous variance model to config_20022

DO $$
	DECLARE 
		residual_id INTEGER;
		residual_code TEXT := 'residual_opt1';
		residual_name TEXT := 'Univariate homogeneous variance model';
		residual_statement := '~id(units)'
	BEGIN
		SELECT id FROM af.property WHERE code=residual_code
			AND name=residual_name
			AND statement=residual_statement INTO residual_id;

		IF residual_id IS NULL THEN
			WITH config_residual AS (
				INSERT INTO af.property(
					type, data_type, code, "name", "label", "statement"
				) VALUES (
					'catalog_item', 'character varying', 
					residual_code, residual_name, 
					residual_name, residual_statement
				) RETURNING id
			),
			config_residual_property_config_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code='residual'), 
					residual_id, false
				)
			),
			config_residual_config_20022_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
					residual_id, false
				)
			),
			SELECT * FROM config_residual;
		ELSE:
			INSERT INTO af.property_config(
				order_number, creation_timestamp, creator_id,
				is_void, property_id, config_property_id, is_layout_variable
			) VALUES (
				1, 'now()', '1', false,
				(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
				residual_id, false
			);
		END IF;
	END $$



-- add prediction to config_20022

DO $$
	DECLARE 
		prediction_id INTEGER;
		prediction_code TEXT := 'g';
		prediction_name TEXT := 'G';
		prediction_statement := 'ge'
	BEGIN
		SELECT id FROM af.property WHERE code=prediction_code
			AND name=prediction_name
			AND statement=prediction_statement INTO prediction_id;
		IF prediction_id IS NULL THEN
			WITH config_prediction AS (
				INSERT INTO af.property(
					type, data_type, code, "name", "statement"
				) VALUES (
					'catalog_item', 'character varying',
					prediction_code, prediction_name,
					prediction_statement
				) RETURNING id
			),
			config_prediction_property_config_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code='prediction'), 
					prediction_id, false
				)
			),
			config_prediction_config_20022_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false,
					(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
					prediction_id, false
				)
			
			)
			SELECT * FROM config_prediction;
		ELSE:
			INSERT INTO af.property_config(
				order_number, creation_timestamp, creator_id,
				is_void, property_id, config_property_id, is_layout_variable
			) VALUES (
				1, 'now()', '1', false,
				(SELECT id FROM af.property WHERE code = 'config_20022.cfg'),
				prediction_id, false
			);
		END IF;
	END $$



