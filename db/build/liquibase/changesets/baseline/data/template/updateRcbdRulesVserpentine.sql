--liquibase formatted sql

--changeset postgres:updateRcbdRulesVserpentine context:template splitStatements:false rollbackSplitStatements:false
--comment: updateRcbdRulesVserpentine



update af.property_rule set property_config_id = 165 where id in(76,77);
delete from af.property_rule where id = 40;