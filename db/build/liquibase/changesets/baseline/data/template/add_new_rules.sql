--liquibase formatted sql

--changeset postgres:add_new_rules context:template splitStatements:false rollbackSplitStatements:false
--comment: add_new_rules


-- set properties visible
with T(id) as (
	select UI.ID
	from af.property_config pc
	inner join af.property_ui ui on pc.property_ui_id = ui.id
	inner join af.property p on pc.config_property_id = p.id
	where p.code in ('genLayout','serpentine','Vserpentine')
	order by p.code
)update af.property_ui as ui set
  is_visible = true
from T where T.id = ui.id;

--set as Catalog-Type properties
with T(id) as (
	select ui.id
	from af.property_config pc
	inner join af.property p on pc.config_property_id = p.id
	inner join af.property p2 on pc.property_id = p2.id
	inner join af.property_ui ui on ui.id = pc.property_ui_id
	where pc.config_property_id <> pc.property_id
	  and p."type" = 'input'
	  and ((p2.code='randRCBDirri' and p.code in ('nFieldRow', 'nRowPerRep')) or 
	      (p2.code='randROWCOLUMNirri' and p.code in ('nFieldRow', 'nRowBlk')) or
	      (p2.code='randAUGMENTEDRCBDirri' and p.code in ('nFieldRow', 'nRowPerRep')) or
	      (p2.code='randALPHALATTICEirri' and p.code in ('nBlk', 'nRowPerBlk', 'nFieldRow', 'nRowPerRep')) or
	      (p2.code='randRCBDcimmyt' and p.code in ('nFieldRow', 'nPlotBarrier')) or
	      (p2.code in('randALPHALATTICEcimmyt','randALPHALATTICEcimmytWHEAT') and p.code in ('sBlk', 'nFieldRow', 'nPlotBarrier')))
)update af.property_ui as ui set 
  is_catalogue = true
from T where T.id = ui.id;

--remove unused rules
DELETE FROM af.property_rule WHERE id in(2,3,4,26,27);

--add new rules
insert into af.property_rule(property_config_id,type, expression, "group",property_id, is_void,creation_timestamp) values
(65,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(66,'allowed-value,', 'factor(nFieldRow)',2,69,false,now()),
(98,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(99,'allowed-value,', 'factor(nFieldRow)',2,69,false,now()),
(114,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(115,'allowed-value,', 'factor(nFieldRow)',2,69,false,now()),
(85,'allowed-value,', 'factor(totalEntries)',2,null,false,now()),
(86,'allowed-value,', 'factor(nBlk)',2,110,false,now()),
(81,'allowed-value,', 'factor(totalEntries) divisible-by(nBlk)',2,110,false,now()),
(80,'allowed-value,', 'factor(totalPlots) divisible-by(nRowPerRep)',2,70,false,now()),
(164,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(165,'allowed-value,', 'between(totalEntries)',2,null,false,now()),
(132,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(133,'allowed-value,', 'between(totalEntries)',2,null,false,now()),
(130,'allowed-value,', 'factor(totalEntries)',2,null,false,now()),
(148,'allowed-value,', 'factor(totalPlots)',2,null,false,now()),
(149,'allowed-value,', 'between(totalEntries)',2,null,false,now()),
(146,'allowed-value,', 'factor(totalEntries)',2,null,false,now());