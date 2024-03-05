--liquibase formatted sql

--changeset postgres:update_property_statements context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-849 correct property statement for analysis model residuals.

UPDATE af.property 
SET statement = 'sat(loc).ar1(row).ar1(col)' 
WHERE code = 'residual_opt5' AND label = '(AR1row x AR1col) by location';

UPDATE af.property 
SET statement = 'sat(loc).idv(row).ar1(col)' 
WHERE code = 'residual_opt6' AND name = '(IDrow x AR1col) by location';

UPDATE af.property 
SET statement = 'sat(loc).idv(units)' 
WHERE code = 'residual_opt8' AND name = 'No spatial adjustment - heterogeneous error variance across locations';

