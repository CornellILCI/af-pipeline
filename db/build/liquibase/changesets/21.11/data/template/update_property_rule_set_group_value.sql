--liquibase formatted sql

--changeset postgres:update_property_rule_set_group_value context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-808 Update af.property_rule set group = 0 where group is null



update af.property_rule set "group"= 0 where "group"  is null;


--Revert changes
--rollback update af.property_rule set "group"= null where id >= 79;