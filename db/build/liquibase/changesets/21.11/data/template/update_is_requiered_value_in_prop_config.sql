--liquibase formatted sql

--changeset postgres:update_is_requiered_value_in_prop_config context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-853 Update is_requiered value in property_config 2


update af.property_config set is_required = false where id in(289,292,293); 


--Revert CHanges
--rollback update af.property_config set is_required = true where id in(289,292,293); 