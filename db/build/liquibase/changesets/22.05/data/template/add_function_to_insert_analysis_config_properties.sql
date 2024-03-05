--liquibase formatted sql

--changeset postgres:add_function_to_insert_properties context:template splitStatements:false rollbackSplitStatements:false

-- For example, if you want to add a formula to existing analysis config named config_007,
-- you run add_analysis_config_property('foo', 'bar', 'bar', 'foobar', 'formula', 'config_007').
-- Current property types are 'formula', 'residual', 'prediction', though there is no constraint availble in
-- database to restrict only these types. This was a drawback of how tables were designed.

CREATE OR REPLACE FUNCTION af.add_analysis_config_property(
	_property_code TEXT, _property_name TEXT, _property_label TEXT, 
	_property_statement TEXT, _property_type TEXT, _analysis_config_name TEXT
) 
RETURNS INTEGER AS $$
	DECLARE 
		_property_id INTEGER;
		_property_type_id INTEGER;
		_analysis_config_id INTEGER;
		_property_config_property_id INTEGER;
	BEGIN
		SELECT id FROM af.property WHERE code=_property_code
			AND name=_property_name
			AND statement=_property_statement INTO _property_id;

		SELECT id FROM af.property WHERE code=_property_type INTO _property_type_id;

		SELECT id FROM af.property WHERE code=_analysis_config_name INTO _analysis_config_id;
		
		-- check property type is valid
		IF _property_type_id IS NULL THEN
			RAISE 'Nonexistant property type: %', _property_type;
		END IF;

		-- check analysis config name is valid
		IF _analysis_config_id IS NULL THEN
			RAISE 'Nonexistant analysis config: %', _analysis_config_name;
		END IF;
	
		IF _property_id IS NULL THEN
			WITH config_property AS (
				INSERT INTO af.property(
					type, data_type, code, "name", "label", "statement"
				) VALUES (
					'catalog_item', 'character varying', 
					_property_code, _property_name, 
					_property_label, _property_statement
				) RETURNING id
			),
			config__property_config_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false, _property_type_id,
					(SELECT id FROM config_property), false
				)
			),
			config_property_analysis_config_link AS (
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false, _analysis_config_id, 
					(SELECT id FROM config_property), false
				)
			
			)
			SELECT id FROM config_property INTO _property_id;
		ELSE
			-- since there is no unique constraint for property_id and config_property_id
			-- adding a check to avoid adding duplicates.
			
			SELECT id FROM af.property_config WHERE property_id=_analysis_config_id AND 
				config_property_id=_property_id INTO _property_config_property_id;

			IF _property_config_property_id IS NULL THEN
				INSERT INTO af.property_config(
					order_number, creation_timestamp, creator_id,
					is_void, property_id, config_property_id, is_layout_variable
				) VALUES (
					1, 'now()', '1', false, _analysis_config_id, _property_id, false
				);
			END IF;
		END IF;
		RETURN _property_id;
	END $$ LANGUAGE plpgsql;

