--liquibase formatted sql

--changeset postgres:update_model_name context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-1119 Update model name 



update af.property set label = 'P-rep CRD w/ diagonal systematic checks' where id=173;

update af.property_meta set value = 'P-rep CRD w/ diagonal systematic checks' where id=145;

update af.property_meta set value = '2' where id=146;