--liquibase formatted sql

--changeset postgres:disable-layout-variable-rand1 context:template splitStatements:false rollbackSplitStatements:false
--comment: disable-layout-variable-rand1



update af.property_config  set is_layout_variable =false where id = 150;