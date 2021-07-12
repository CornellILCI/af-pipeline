--liquibase formatted sql

--changeset postgres:change_label_exp_design context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-72 Change the label of Experimental Design Model



UPDATE af.property
SET "label"='Alpha-Lattice | CIMMYT'
WHERE id=118;

UPDATE af.property
SET "label"='IWIN Design'
WHERE id=119;

UPDATE af.property
SET "label"='RCBD | CIMMYT'
WHERE id=120;

UPDATE af.property
SET "label"='RCBD'
WHERE id=8;

UPDATE af.property
SET "label"='Alpha-Lattice'
WHERE id=9;

UPDATE af.property
SET "label"='Row-Column'
WHERE id=38;

UPDATE af.property
SET "label"='Augmented RCB'
WHERE id=39;