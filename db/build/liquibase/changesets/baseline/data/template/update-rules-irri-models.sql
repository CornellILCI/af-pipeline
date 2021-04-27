--liquibase formatted sql

--changeset postgres:update-rules-irri-models context:template splitStatements:false rollbackSplitStatements:false
--comment: update-rules-irri-models



-- PROP DESCRIPTIONS
update af.property set description = 'Plot arrangement' where id = 71;

-- ALPHA-LATTICE IRRI
update af.property_meta  set value  = '23-Oct-2020' where id = 28;
update af.property_rule set expression = 'totalEntries>=6' where order_number=2 and property_config_id=77;

-- AUGMENTED RCBD IRRI
update af.property_meta  set value  = '23-Oct-2020' where id = 58;
update af.property_rule set expression = 'value>=((12/(nCheck-1))+1)' where order_number = 3 and property_config_id = 112;

-- RCBD IRRI
update af.property_meta  set value  = '26-Oct-2020' where id = 39;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','totalEntries>30','Total number of entries is too large for a RCBD. Consider selecting a more appropriate design.','warning',62);

delete from af.property_rule where order_number=2 and property_config_id=66;
update af.property_rule set expression='factor(nRep)*nRowPerRep' where order_number=1 and property_config_id=65;
delete from af.property_rule where id in (59,60,61) and property_config_id=65;

-- ROW COLUMN IRRI
update af.property_meta  set value  = '23-Oct-2020' where id = 47;
update af.property_rule set expression='totalEntries>=9' where order_number=2 and property_config_id=95;
update af.property_rule set expression='value<totalEntries' where order_number=3 and property_config_id=99;

update af.property_rule set expression='if(Vserpentine){value<=(nFieldRow)}' where id in (70,74,77);  