--liquibase formatted sql

--changeset postgres:update_is_requiered_value_in_property_config context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-851 Update is_requiered value in property_config



update af.property_config set is_required = false where id in(275,276,277,282,283);


--Revert Changes
--rollback update af.property_config set is_required = true where id in(275,276,277,282,283);