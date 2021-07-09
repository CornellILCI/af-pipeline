--liquibase formatted sql

--changeset postgres:update_default_value_of_ntrial_for_iwin_design context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-424 Update in AFDb the default value of nTrial for IWIN Design


UPDATE af.property_ui
SET  "default" = 2
WHERE id=56;


UPDATE af.property
SET description='Number of occurrences within the experiment'
WHERE id=65;


--Revert Changes
--rollback UPDATE af.property_ui SET  "default" = NULL WHERE id=56;
--rollback UPDATE af.property SET description='Number of occurrances within the experiment' WHERE id=65;