--liquibase formatted sql

--changeset postgres:config-clean context:template splitStatements:false rollbackSplitStatements:false
--comment: config-clean



update af.property_config set is_required = false where config_property_id in (72, 73);

delete from af.request_parameter rp where id <= 59;
delete from af.request where id <= 15;

select setval('af.request_parameter_id_seq',max(id)) from af.request_parameter;
select setval('af.property_id_seq',max(id)) from af.property;
select setval('af.property_config_id_seq',max(id)) from af.property_config;
select setval('af.property_rule_id_seq',max(id)) from af.property_rule;
select setval('af.property_ui_id_seq',max(id)) from af.property_ui;
select setval('af.request_id_seq',max(id)) from af.request;