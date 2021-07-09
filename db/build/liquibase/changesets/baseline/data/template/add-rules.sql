--liquibase formatted sql

--changeset postgres:add-rules context:template splitStatements:false rollbackSplitStatements:false
--comment: add-rules



-- UPDATE TABLE: RULES

ALTER TABLE af.property_rule ALTER COLUMN "expression" TYPE varchar(100) USING "expression"::varchar;
ALTER TABLE af.property_rule ADD order_number int4 NULL;
ALTER TABLE af.property_rule ADD notification varchar(255) NULL;
ALTER TABLE af.property_rule ADD "action" varchar(50) NULL;

-- CLEAR UNUSED VALUES
delete from af.property_rule where type = 'required-if';
update af.property_rule set type = 'allowed-value' where type = 'allowed-value,';
update af.property_rule set "group" = 0, property_id=null where id>0;

-- PROP DESCRIPTIONS
update af.property set data_type = 'string' where id = 66;
update af.property set description = 'Block size, it is the number of plots per block. Consider using several small blocks instead of a few large blocks' where id = 121;
UPDATE af.property 	SET description='Define rows and columns along with the design',"label"='Define Shape/Dimension' WHERE id=68;
UPDATE af.property	SET description='Number of plots until turn the serpentine, it will follow the same direction of the serpentine (horizontal or vertical)' WHERE id=122;


-- ALPHA-LATTICE IRRI
update af.property_meta  set value  = 'Total number of plots per Occurrence should not exceed 1,500.' where id = 37;
update af.property_meta  set value  = '19-Oct-2020' where id = 28;
insert into af.property_meta (code,value, tenant_id ,creation_timestamp ,property_id )values('note2','Total number of entries should not be a prime number.',1,now(),9);

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','!prime(totalEntries)','Total number of entries should not be a prime number.','error',77);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'validation-design','(totalEntries)>=6','Number of entries should be at most 6.','error',77);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','value<=(1500/totalEntries)','Total number of experimental units should not exceed 1,500.','error',78);
update af.property_rule set order_number=1 where id = 35;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','value>1',null,null,85);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'allowed-value','value<(totalEntries)',null,null,85);
update af.property_rule set order_number=1, expression='factor(totalEntries/nBlk)' where id = 36;
update af.property_rule set order_number=1, expression='factor(nBlk)*nRowPerBlk' where id = 37;
update af.property_rule set order_number=1, expression='factor(nRep)*nRowPerRep' where id = 38;
delete from af.property_rule where id = 29;

update af.property_ui set "default" = 1 where id=16;
update af.property_ui set "default" = 2 where id=18;
update af.property_ui set minimum = null, maximum = null where id in(19,21,22,23);

-- AUGMENTED RCBD IRRI
update af.property_meta  set value  = '19-Oct-2020' where id = 58;

update af.property_ui set "default" = 1 where id=36;
update af.property_ui set minimum = null where id=39;
update af.property_ui set "default" = null where id=41;

UPDATE af.property_config SET order_number=6 WHERE id=115;
UPDATE af.property_config SET order_number=7 WHERE id=114;

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','nCheck>1','Number of check entries should be greater than 1.','error',119);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'validation-design','nEntries>1','Number of test entries should be greater than 1.','error',119);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','factor(nEntries)','Should be a factor of the number of test entries.','error',112);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'default-value','min(factor(Entries))>1',null,null,112);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'validation-design','value>=(12/(nCheck-1)+1)','The error degrees of freedom associated with number of check entries should be at most 12.','warning',112);
update af.property_rule set order_number=1, "expression"='factor(nCheck+(nEntries/nRep))' where id = 34;
update af.property_rule set order_number=1, "type"='validation-design', "expression"='factor(nRep)*nRowPerRep' where id = 33;


-- RCBD IRRI
update af.property_meta  set value  = '10-Oct-2020' where id = 39;

update af.property_rule set order_number=1, "expression" ='factor(totalEntries)' where id = 30;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','max=totalEntries',null,null,66);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'allowed-value','min = nRowPerRep',null,null,65);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','divisible by nRowPerRep',null,null,65);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'allowed-value','quotient nFieldRow/nRowPerRep should be a factor of nRep',null,null,65);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(4,'allowed-value','max=nRowPerRep*nRep',null,null,65);

UPDATE af.property_config SET order_number=6 WHERE id=65;
UPDATE af.property_config SET order_number=5 WHERE id=66;

-- ROW COLUMN IRRI
insert into af.property_meta (code,value, tenant_id ,creation_timestamp ,property_id )values('note2','Total number of entries should not be a prime number.',1,now(),38);
update af.property_meta  set value  = '19-Oct-2020' where id = 47;

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','!prime(totalEntries)','Total number of entries should not be a prime number.','error',95);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'validation-design','(totalEntries)>=9','Number of entries should be at most 9.','error',95);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','value<=(1500/totalEntries)','Total number of plots should not exceed 1,500.','error',96);
update af.property_rule set order_number=1 where id = 32;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','value>1',null,null,99);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'allowed-value','value<(totalEntries)',null,null,99);
update af.property_rule set order_number=1, "expression" ='factor(nRep)*nRowPerBlk' where id = 31;

update af.property_ui set "default" = 1 where id=27;
update af.property_ui set "default" = 2 where id=29;
update af.property_ui set minimum = null, maximum = null where id in(30,32);

-- ALPHA LATTICE CIMMYT
update af.property_meta  set value  = '15-Oct-2020' where id = 2;

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','!prime(totalEntries)','Total number of entries should not be a prime number. Kindly update the entry list or select an appropriated design','error',128);
update af.property_rule set order_number=1 where id = 43;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','value>1',null,null,130);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'allowed-value','value<(totalEntries)',null,null,130);
update af.property_rule set order_number=1, "expression" = 'factor(totalEntries*nRep)' where id = 41;
update af.property_rule set order_number=1, "expression" = 'if(!Vserpentine){value<=((totalEntries*nRep)/nFieldRow)}' where id = 42;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','if(vSerpentine){value<=(nFieldRow)}',null,null,133);

update af.property_ui set "default" = 1 where id=46;
update af.property_ui set "default" = 2 where id=48;
update af.property_ui set minimum = null, maximum = null where id = 49;
update af.property_ui set maximum = null where id=51;
update af.property_ui set minimum = null, maximum = null where id = 52;
update af.property_config set order_number = 8 WHERE id=133;
update af.property_config set order_number = 7 WHERE id=134;

-- ALPHA LATTICE CIMMYT wheat
update af.property_meta  set value  = '15-Oct-2020' where id = 11;

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','!prime(totalEntries)','Total number of entries should not be a prime number. Kindly update the entry list or select an appropriated design','error',144);
update af.property_rule set order_number=1 where id = 46;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','value>1',null,null,146);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(3,'allowed-value','value<(totalEntries)',null,null,146);
update af.property_rule set order_number=1, "expression" = 'factor(totalEntries*nRep)' where id = 44;
update af.property_rule set order_number=1, "expression" = 'if(!Vserpentine){value<=((totalEntries*nRep)/nFieldRow)}' where id = 45;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','if(vSerpentine){value<=(nFieldRow)}',null,null,149);

update af.property_ui set "default" = 2 where id=58;
update af.property_ui set minimum=null, maximum = null where id=59;
update af.property_ui set maximum = null where id=61;
update af.property_ui set minimum = null where id=62;
update af.property_config set order_number = 7 WHERE id=147;
update af.property_config set order_number = 8 WHERE id=148;
update af.property_config set order_number = 10 WHERE id=149;
update af.property_config set order_number = 5 WHERE id=150;
update af.property_config set order_number = 6 WHERE id=178;
update af.property_config set order_number = 9 WHERE id=151;

-- RCBD CIMMYT
update af.property_meta  set value  = '15-Oct-2020' where id = 20;

insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'validation-design','totalEntries>30','Total number of entries is too large for a RCBD. Consider selecting a more appropriate design','warning',161);
update af.property_rule set order_number=1, "expression" ='factor(totalEntries*nRep)' where id = 39;
update af.property_rule set order_number=1, "expression"='value<=((totalEntries*nRep)/nFieldRow)' where id = 40;
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(1,'allowed-value','if(!Vserpentine){value<=((totalEntries*nRep)/nFieldRow)}',null,null,166);
insert into af.property_rule (order_number,"type","expression", notification, "action", property_config_id ) values(2,'allowed-value','if(vSerpentine){value<=(nFieldRow)}',null,null,166);

UPDATE af.property_ui SET "default"='1' WHERE id=67;
UPDATE af.property_ui SET "default"='2'	WHERE id=69;
UPDATE af.property_ui SET minimum=NULL WHERE id=72;
UPDATE af.property_config SET order_number=7 WHERE id=165;
UPDATE af.property_config SET order_number=6 WHERE id=166;

ALTER TABLE af.property_rule ALTER COLUMN order_number SET NOT NULL;