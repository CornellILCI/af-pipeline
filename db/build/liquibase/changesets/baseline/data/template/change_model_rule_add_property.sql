--liquibase formatted sql

--changeset postgres:change_model_rule_add_property context:template splitStatements:false rollbackSplitStatements:false
--comment: change_model_rule_add_property



INSERT INTO af.property (id,code,"name","label",description,"type",data_type,creation_timestamp,is_void)
	VALUES (133,'RandOcc','RAND_OCC','Randomize each occurrence','Whether run a randomization for each occurrence or use the same randomization for all of them','input','boolean','now()',false);

INSERT INTO af.property_ui (id, is_visible,"default",is_disabled,is_multiple,is_catalogue,creation_timestamp,creator_id)
	VALUES (77,true,'true',false,false,false,'now()','1');

INSERT INTO af.property_config (is_required,order_number,creation_timestamp,creator_id,is_void,property_id,config_property_id,property_ui_id,is_layout_variable)
	VALUES (true,9,'now()','1',false,119,133,77,false);

update af.property_config set order_number = order_number + 1 where id in (151,152,153);
update af.property_rule set expression = 'factor(totalEntries)' where id=32;

select setval('af.property_ui_id_seq',max(id)) from af.property_ui;
select setval('af.property_id_seq',max(id)) from af.property;