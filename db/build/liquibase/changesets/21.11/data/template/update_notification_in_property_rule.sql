--liquibase formatted sql

--changeset postgres:update_notification_in_property_rule context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-858 Update notification in af.proeprty_rule



update af.property_rule set notification ='At least 20% of the test entries shoulde have at least 2 number of replicates.' where id = 83;


--Revert Changes
--rollback update af.property_rule set notification ='At least 20% of the test entries shoulde have at most 2 number of replicates.' where id = 83;
