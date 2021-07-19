--liquibase formatted sql

--changeset postgres:update-design-rules context:template splitStatements:false rollbackSplitStatements:false
--comment: update-design-rules



update af.property_rule set expression = 'totalEntries<=30' where property_config_id=62 and order_number=1;  
update af.property_rule set expression = 'totalEntries<=30' where property_config_id=161 and order_number=1;  
update af.property_rule set type = 'allowed-value' where property_config_id=114 and order_number=1;  
update af.property_rule set expression = 'factor(nRep)*nRowBlk' where property_config_id=98 and order_number=1;  
update af.property_rule set expression = 'min(factor(nEntries)) > 1' where property_config_id=112 and order_number=2;