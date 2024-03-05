--liquibase formatted sql

--changeset postgres:modify_formula_rcbd_names_labels context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-923 Add the entry effect in the formula name of RCBD SEML model

UPDATE af.property 
SET name='RCBD SESL Univariate, genotype as random',
    label='RCBD SESL Univariate, genotype as random'
WHERE id=148 and code='formula_opt1';


UPDATE af.property 
SET name='RCBD SEML Univariate, genotype as random',
    label='RCBD SEML Univariate, genotype as random'
WHERE id=149 and code='formula_opt2';

