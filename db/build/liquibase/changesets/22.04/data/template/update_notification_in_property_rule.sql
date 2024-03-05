--liquibase formatted sql

--changeset postgres:update_notification_in_property_rule context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-1118 Update notification in af.property_rule



update af.property_rule set notification = 'Number of replicates should be a factor of the number of test entries.' where id=54;