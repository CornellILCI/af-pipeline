--liquibase formatted sql

--changeset postgres:add_is_layout_variable_data context:template splitStatements:false rollbackSplitStatements:false
--comment: add_is_layout_variable_data



 UPDATE af.property_config SET is_layout_variable=true WHERE id in(132,133,134,148,149,150,151,164,165,166,80,81,82,86,65,66,67);
