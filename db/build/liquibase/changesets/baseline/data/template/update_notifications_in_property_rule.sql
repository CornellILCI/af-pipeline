--liquibase formatted sql

--changeset postgres:uBA-1 Correct Property rulepdate_notifications_in_property_rule context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-1 Correct Property rule



UPDATE af.property_rule
SET notification='Number of entries should be at least 6.'
WHERE id=48;

UPDATE af.property_rule
SET notification='The error degrees of freedom associated with number of check entries should be at least 12.'
WHERE id=56;

UPDATE af.property_rule
SET notification='Number of entries should be at least 9.'
WHERE id=63;

UPDATE af.property_rule
SET notification='Number of occurrences should be a factor of the number of test entries.'
WHERE id=54;