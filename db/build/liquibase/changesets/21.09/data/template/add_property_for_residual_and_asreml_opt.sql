--liquibase formatted sql

--changeset postgres:add_property_for_residual_and_asreml_opt context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-696 Add property for residual and asreml option



INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, creator_id, is_void, tenant_id, "statement")
VALUES('residual_opt8', 'No spatial adjustment - heterogeneous error variance across locations', 'No spatial adjustment - heterogeneous error variance across locations', 'No spatial adjustment - heterogeneous error variance across locations, block diagonal', 'catalog_item', 'character varying', now(), '1', false, 1, 'sat(loc).idv(units)add');


INSERT INTO af.property
(code, "name", "label", description, "type", data_type, creation_timestamp, modification_timestamp, creator_id, modifier_id, is_void, tenant_id,"statement")
VALUES('asrmel_opt2', NULL, NULL, NULL, 'catalog_item', 'character varying', now(), NULL, '1', NULL, false, 1, ' !CSV !SKIP 1 !AKAIKE !NODISPLAY !SECTION loc !ROWFACTOR row !COLUMNFACTOR col !MVINCLUDE !MAXIT 250 !EXTRA 10 !TXTFORM 1 !FCON !SUM !OUTLIER');


--Revert Changes
--rollback DELETE FROM af.property WHERE code='residual_opt8';
--rollback DELETE FROM af.property WHERE code='asrmel_opt2';
