--liquibase formatted sql

--changeset postgres:update_residual_formulas_without_tilde context:template splitStatements:false rollbackSplitStatements:false
--comment: BA2-85 fix

UPDATE af.property SET statement = '~ ar1(row):ar1(col)' WHERE statement = 'ar1(row):ar1(col)';                         
                                                                                                                        
UPDATE af.property SET statement = '~ ar1(row):id(col)' WHERE statement = 'ar1(row):id(col)';                           
                                                                                                                        
UPDATE af.property SET statement = '~ id(row):ar1(col)' WHERE statement = 'id(row):ar1(col)'; 