--liquibase formatted sql

--changeset postgres:update_data_type_and_is_catalogue_values context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-803 Update data type and is_catalogue values


--P-REP changes
--formula for nFieldrow
INSERT INTO af.property_rule ("type","expression","group",is_void,property_config_id,order_number) VALUES
	 ('allowed-value','factor(totalPlots)',0,false,280,1);
	
--nFieldrow
update af.property_ui set is_catalogue = true where id = 83;

--field order in P-rep
update af.property set data_type = 'character varying' where id = 171;
update af.property_ui set is_catalogue = true where id = 84;

--Augmented Design
--for pCheck
update af.property set data_type = 'character varying' where id = 175;
update af.property_ui set is_catalogue = true where id = 91;

--for nFieldCol
update af.property_ui set is_catalogue = true where id = 90;


--Revert Changes
--rollback DELETE FROM af.property_rule WHERE "expression"= 'factor(totalPlots)';
--rollback update af.property_ui set is_catalogue = false where id = 83;
--rollback update af.property set data_type = 'enumeration' where id = 171;
--rollback update af.property_ui set is_catalogue = false where id = 84;
--rollback update af.property set data_type = 'enumeration' where id = 175;
--rollback update af.property_ui set is_catalogue = false where id = 91;
--rollback update af.property_ui set is_catalogue = false where id = 90;
--rollback select setval('af.property_rule_id_seq',max(id)) from af.property_rule;